import os
from typing import Iterable, Union

from .lib import Plugin, Element
from .utils import clean_dir, Keys, Defaults
from pathlib import Path


class Hausse(object):
    """
    Hausse
    ======

    A Hausse object is used to generate a static project using a set of plugins.

    A Hausse object should be initialized, populated by initialized plugins with `use()` method, then executed with the `build()` method.

    Note that all Hausse's method returns `self`, for convenient methods call chaining.

    Parameters
    ----------
    `base_dir` (str) :
        The base working directory path for the project. Current folder by default.
    **kwargs
        Additional options.
    """

    def __init__(self, base_dir: str = Defaults.BASE, **kwargs):

        # Loaded plugins list
        self._plugins = []
        
        # Data
        self.elements = list()
        self.metadata = dict()
        self.settings = Defaults.SETTINGS | kwargs | {Keys.BASE: Path(base_dir)}


    def source(self, src: str = Defaults.SRC):
        """Sets the source files directory path. `src` by default."""
        
        self.settings[Keys.SRC] = Path(src)

        return self

    
    def dist(self, dist: str = Defaults.DIST):
        """Sets the output directory path. `dist` by default."""

        self.settings[Keys.DIST] = Path(dist)

        return self

    def clean(self, clean: bool = True):
        """Toggle output directory cleaning. True by default."""

        self.settings[Keys.CLEAN] = clean

        return self


    def use(self, plugin: Union[Iterable[Plugin], Plugin]):
        """Register a plugin or a list of plugins in the Hausse project plugins list to be used."""

        if isinstance(plugin, list):
            self._plugins += plugin
        else:
            self._plugins.append(plugin)

        return self


    def build(self):
        """Build the project. All the actual processing logic is run in this method scope."""

        # Saving original working directory
        owd = os.getcwd()

        # Set working directory
        os.chdir(self.settings.get(Keys.BASE, Defaults.BASE))

        # Cleaning dist directory
        if self.settings.get(Keys.CLEAN, Defaults.CLEAN):
            clean_dir(self.settings.get(Keys.DIST, Defaults.DIST))
       
        # Load all source files
        src = self.settings.get(Keys.SRC, Defaults.SRC)
        self.elements += [Element(p.relative_to(src), src, self.metadata) for p in src.rglob("*") if p.is_file()]
                    
        # Apply all plugins work
        for plugin in self._plugins:
            plugin(self.elements, self.metadata, self.settings)
        
        # Saving built files
        for document in self.elements:

            # Arborescence creation
            document_path = Path(os.path.join(self.settings[Keys.DIST], document._path))
            document_path.parent.mkdir(parents=True, exist_ok=True)

            # Saving built file
            with open(os.path.join(self.settings[Keys.DIST], document._path), "w") as file:
                file.write(str(document))

        # Restoring original working directory
        os.chdir(owd)

        return self