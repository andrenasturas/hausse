import os
from typing import Iterable, Union

from .lib import Plugin, Element
from .utils import clean_dir, Keys, Defaults
from pathlib import Path


class Hausse(object):
    """
    Hausse
    ======

    A pluggable static project generator.

    Hausse can build a static project using a customized list of plugins.

    A Hausse object should be initialized, populated by initialized plugins
    with `use()` method, then executed with the `build()` method. Note that
    without any plugins, Hausse will do no more thant copying files from the
    source directory (`src` by default) to the output directory (`dist` by
    default). All processing is done by the plugins.

    Note also that all Hausse's method returns `self`, for convenient methods
    call chaining.

    Parameters
    ----------
    - `base_dir` ( str ) :
        Base working directory path for the project. Current folder by default.
    - `elements` ( list[ Element ] ) :
        Additional elements to be add to the project
    - `metadata` ( dict ) :
        Additional metadata to be add to the project
    - `settings` ( dict ) :
        Additional settings to be add to the project
    - `**kwargs` ( dict ) :
        Additional settings to be add to the project. Overwrite `settings`.


    Examples
    --------

    >>> Hausse().build()
    # Copy the content of `./src` to `./dist`

    >>> Hausse().use(Markdown()).build()
    # Parses markdown files from `./src` to HTML files in `./dist`.

    >>> Hausse("website").use(Markdown()).build()
    # Same as before, but using `./website/src` and `./website/dist`

    >>> Hausse("website", metadata={"foo": "bar"}).use(Markdown()).build()
    # Same as before, but with "foo" metadata accessible everywhere.


    Attributes
    ----------
    - `_plugins` ( list[ Plugin ] ) :
        Registered plugins that will be called in `build()` method.
    - `elements` ( list[ Element ] ) :
        Elements (files, mainly) loaded from source to be processed.
    - `metadata` ( dict ) :
        Global metadata accessible from any Element.
    - `settings` ( dict ) :
        Technical storage dictionary for plugins interactions.
    """

    def __init__(
        self,
        base_dir: str = Defaults.BASE,
        elements: list[Element] = None,
        metadata: dict = None,
        settings: dict = None,
        **kwargs
    ):

        # Loaded plugins list
        self._plugins = []

        # Data
        self.elements = elements or list()
        self.metadata = metadata or dict()
        self.settings = Defaults.SETTINGS | (settings or dict()) | kwargs

        # Base directory
        self.settings[Keys.BASE] = Path(base_dir)

    def source(self, src: str = Defaults.SRC):
        """Sets the source files directory path. `src` by default."""

        self.settings[Keys.SRC] = Path(src) if src else None

        return self

    def dist(self, dist: str = Defaults.DIST):
        """Sets the output directory path. `dist` by default."""

        self.settings[Keys.DIST] = Path(dist) if dist else None

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

        # Load all source files if source folder is defined
        src = self.settings.get(Keys.SRC)
        if src:
            self.elements += [
                Element(p.relative_to(src), src, self.metadata)
                for p in src.rglob("*")
                if p.is_file()
            ]

        # Apply all plugins work
        for plugin in self._plugins:
            plugin(self.elements, self.metadata, self.settings)

        # Saving built files
        dist = self.settings.get(Keys.DIST)
        if dist:
            for document in self.elements:

                # Arborescence creation
                document_path = Path(os.path.join(dist, document._path))
                document_path.parent.mkdir(parents=True, exist_ok=True)

                # Saving built file
                with open(os.path.join(dist, document._path), "w") as file:
                    file.write(str(document))

        # Restoring original working directory
        os.chdir(owd)

        return self