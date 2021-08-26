from abc import ABC, abstractmethod
from inspect import Parameter, signature
from pathlib import Path
from typing import Iterable, Optional, Union

from ..utils import Defaults
from .project import Project
from .selector import All, BaseSelector, Selector


class Plugin(ABC):
    """
    Hausse plugin structure
    """

    @abstractmethod
    def __init__(self):
        """Initialize plugin."""
        raise NotImplementedError

    @abstractmethod
    def __call__(self, project: Project):
        """Do the plugin task."""
        raise NotImplementedError

    def save(self):
        """Return a JSON-like dict representing the plugin instance config.

        This method is called by `Hausse.save()`.
        """
        defaults = {
            k: v.default
            for k, v in signature(self.__init__).parameters.items()
            if v.default is not Parameter.empty
        }
        # Return all key-values from the plugin except
        # - technic internal keys (identified by leading underscore)
        # - default values (identified by plugin init signature inspection)
        # - and empty values corresponding to None defaults (empty lists)
        return {
            k: v
            for k, v in self.__dict__.items()
            if not k.startswith("_") and v != defaults.get(k) and (v or defaults.get(k))
        }


class SelectorPlugin(Plugin):
    """
    Plugin template with a Selector parameter.

    Selector can be a file path pattern, an iterator over an Elements list, or
    any other Selector object.
    """

    def __init__(
        self, selector: Union[str, Iterable, BaseSelector], selector_by_default=None
    ):
        self.selector = Selector(selector or selector_by_default)
        self._selector_by_default = selector_by_default

    def save(self):
        d = super().save()
        if self.selector == self._selector_by_default:
            del d["selector"]
        else:
            d["selector"] = d["selector"].save()
        return d


class PathPlugin(Plugin):
    """
    Plugin template with a Path parameter.

    PathPlugin should be used when manipulating files outside of source folder.
    """

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

    def save(self) -> dict:
        d = super().save()
        d["path"] = str(d["path"])
        if d["path"] == signature(self.__init__).parameters["path"].default:
            del d["path"]
        return d


class LayoutPlugin(PathPlugin, SelectorPlugin):
    """
    Hausse layout plugin structure
    """

    def __init__(
        self,
        path: str = Defaults.LAYOUTS,
        default: str = None,
        selector: Union[str, Iterable, Selector] = None,
        options: dict = None,
        **kwargs
    ):
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
        SelectorPlugin.__init__(self, selector, All())
        PathPlugin.__init__(self, path)
        self.default = default
        self.options = options or dict() | kwargs
