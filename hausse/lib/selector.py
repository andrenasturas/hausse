from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable


class BaseSelector(ABC):
    @abstractmethod
    def __init__(self):
        """Plugin initialisation"""
        raise NotImplementedError

    @abstractmethod
    def __call__(self, elements: list, metadata: dict, settings: dict):
        """Plugin work"""
        raise NotImplementedError


class PathPatternSelector(BaseSelector):
    def __init__(self, pattern):
        self.pattern = pattern

    def __call__(self, elements: list, metadata: dict, settings: dict):
        return (element for element in elements if element._path.match(self.pattern))


class ExtensionSelector(BaseSelector):
    def __init__(self, *extensions):
        # TODO: Reddit Unicode ocmparaisons https://stackoverflow.com/questions/319426/how-do-i-do-a-case-insensitive-string-comparison
        # As we compare filename extensions, we can rely on `.lower()` without considering special unicode combinaisons
        self.extensions = list(map(lambda x: x.lstrip(".").lower(), extensions))

    def __call__(self, elements: list, metadata: dict, settings: dict):
        return (
            element
            for element in elements
            if element._path.suffix.lstrip(".").lower() in self.extensions
        )


class ElementsSelector(BaseSelector):
    def __init__(self, elements):
        self.elements = elements

    def __call__(self, elements: list, metadata: dict, settings: dict):
        return iter(self.elements)


class CollectionSelector(BaseSelector):
    def __init__(self, collection):
        self.collection = collection
    
    def __call__(self, elements: list, metadata: dict, settings: dict):
        return iter(settings['collections'][self.collection])


class AllSelector(BaseSelector):
    def __init__(self):
        pass
    
    def __call__(self, elements: list, metadata: dict, settings: dict):
        return iter(elements)


def Selector(selection) -> BaseSelector:

    if isinstance(selection, BaseSelector):
        # Selector(Selector()) == Selector()
        return selection

    if isinstance(selection, str):
        # If selection is a string, assuming that it is a filepath pattern
        return PathPatternSelector(selection)

    if isinstance(selection, Iterable):
        # If selection is a non-string iterable, assuming it is an iterable
        # over already choosen Elements
        # This case can accept a Collection object, and will return a selector
        # over the current Collection members
        return ElementsSelector(selection)