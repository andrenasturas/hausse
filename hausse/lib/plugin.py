from abc import ABC, abstractmethod
from pathlib import Path
from typing import Iterable, Union

from hausse.utils import Defaults
from .selector import Selector, AllSelector


class Plugin(ABC):
    """
    Hausse plugin structure
    """

    @abstractmethod
    def __init__(self):
        """Plugin initialisation"""
        raise NotImplementedError

    @abstractmethod
    def __call__(self, elements: list, metadata: dict, settings: dict):
        """Plugin work"""
        raise NotImplementedError


class SelectorPlugin(Plugin):
    """
    Plugin template with a Selector parameter.

    Selector can be a file path pattern, an iterator over an Elements list, or any other Selector object.
    """

    def __init__(self, selector: Union[str, Iterable, Selector]):
        self.selector = Selector(selector)


class LayoutPlugin(Plugin):
    """
    Hausse layout plugin structure
    """

    def __init__(self, directory: str = Defaults.LAYOUTS, default: str = None, selector: Union[str, Iterable, Selector] = None, options: dict = None, **kwargs):
        """
        # TODO: Update documentation
        Parameters
        ----------
        directory: str
            Layouts folder path
        default: str
            Default layout file that should be used if none is specified
        pattern: str
            Matching pattern for the elements to be processed
        options: dict
            Options passed to the layout engine
        **kwargs: dict
            Additional options passed to the layout engine
        """
        self.default = default
        self.directory = Path(directory)
        self.selection = Selector(selector) if selector else AllSelector()
        self.options = options or dict() | kwargs