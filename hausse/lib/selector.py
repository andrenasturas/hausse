from abc import ABC, abstractmethod
from inspect import isclass
from typing import Iterable

from .project import Project


class BaseSelector(ABC):
    @abstractmethod
    def __init__(self):
        """Plugin initialisation"""
        raise NotImplementedError

    @abstractmethod
    def __call__(self, project: Project):
        """Plugin work"""
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.selection})"

    def __eq__(self, other) -> bool:
        return self.__class__ == other.__class__ and self.selection == other.selection

    def save(self) -> dict:
        """Plugin str serialization"""
        return {self.__class__.__name__.lower(): self.selection}


class Pattern(BaseSelector):
    def __init__(self, pattern):
        self.selection = pattern

    def __call__(self, project: Project):
        return (
            element
            for element in project.elements
            if element._path.match(self.selection)
        )


class Extensions(BaseSelector):
    def __init__(self, *extensions):
        # As we compare filename extensions, we can rely on `.lower()` without
        # considering special unicode combinaisons
        self.selection = list(map(lambda x: x.lstrip(".").lower(), extensions))

    def __call__(self, project: Project):
        return (
            element
            for element in project.elements
            if element._path.suffix.lstrip(".").lower() in self.selection
        )


class Elements(BaseSelector):
    def __init__(self, elements):
        self.selection = elements

    def __call__(self, project: Project):
        return iter(self.selection)


class Collection(BaseSelector):
    def __init__(self, collection):

        self.selection = collection

    def __call__(self, project: Project):
        return iter(project.settings["collections"][self.selection])


class All(BaseSelector):
    def __init__(self, _=None):
        self.selection = "all"  # Used only for json save

    def __call__(self, project: Project):
        return iter(project.elements)


selectors = {
    k.lower(): v
    for k, v in globals().items()
    if isclass(v) and v.__module__ == "hausse.lib.selector" and k != "BaseSelector"
}


def Selector(selection) -> BaseSelector:

    if isinstance(selection, BaseSelector):
        # Selector(Selector()) == Selector()
        return selection

    if isinstance(selection, dict):
        # TODO: Support selectors unions
        selector = list(selection.keys())[0]
        if selector.lower() in selectors:
            return selectors[selector](selection[selector])

    if hasattr(selection, "_get_selector"):
        # This case can accept a Collection object, and will return a selector
        # over the current Collection members
        return selection._get_selector()

    if isinstance(selection, str):
        # If selection is a string, assuming that it is a filepath pattern
        return Pattern(selection)

    if isinstance(selection, Iterable):
        # If selection is a non-string iterable, assuming it is an iterable
        # over already chosen Elements
        return Elements(selection)
