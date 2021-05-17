"""Hausse main module."""

import logging
import json
import yaml
import os
from importlib import import_module
from typing import Callable, Iterable, Union

from .lib import Element
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
    base : str
        Working directory or hausse.json file path. Current folder by default.
        If None and hausse.json available in current folder, it will be used.
    elements : List of Element
        Additional elements to be add to the project
    metadata : dict
        Additional metadata to be add to the project
    settings : dict
        Additional settings to be add to the project
    **kwargs : dict
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
    _plugins : List of Plugin
        Registered plugins that will be called in `build()` method.
    elements : List of Element
        Elements (files, mainly) loaded from source to be processed.
    metadata : dict
        Global metadata accessible from any Element.
    settings : dict
        Technical storage dictionary for plugins interactions.
    """

    def __init__(
        self,
        base_dir: str = None,
        elements: list[Element] = None,
        metadata: dict = None,
        settings: dict = None,
        **kwargs,
    ):

        # Loaded plugins list
        self._plugins: list[Callable] = list()

        # Data
        self.elements = elements or list()
        self.metadata = metadata or dict()
        self.settings = Defaults.SETTINGS | (settings or dict()) | kwargs

        # Base directory
        base_path = Path(base_dir) if base_dir else Path(Defaults.BASE)
        self.settings[Keys.BASE] = (
            base_path.parent if base_path.is_file() else base_path
        )

    def source(self, src: str = Defaults.SRC):
        """Set the source files directory path. *Defaults to `src`*."""
        self.settings[Keys.SRC] = Path(src or Defaults.SRC)

        return self

    def destination(self, dist: str = Defaults.DIST):
        """Set the output directory path. *Defaults to `dist`*."""
        self.settings[Keys.DIST] = Path(dist or Defaults.DIST)

        return self

    def clean(self, clean: bool = Defaults.CLEAN):
        """Toggle output directory cleaning. False by default."""
        self.settings[Keys.CLEAN] = Defaults.CLEAN if clean is None else clean

        return self

    def use(self, plugin: Union[Iterable[Callable], Callable]):
        """Register a plugin or a list of plugins.

        Each plugin have to be registered into the Hausse project via this
        method. Plugins are stored and used in order. A plugin can be used
        multiple time at once if relevent.

        Note
        ----
        This method actually accepts any callables, not only Plugin objects, in
        order to allow usage of simple custom-made methods without full Plugin
        implementation.

        """
        if isinstance(plugin, list):
            self._plugins += plugin
        elif callable(plugin):
            self._plugins.append(plugin)
        else:
            raise ValueError(f"{type(plugin)} is not callable nor an iterable")

        return self

    def build(self):
        """Build the project."""
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

    def save(self, file=None, mode=None, hidden: bool = False):
        """Save the current configuration to a file."""
        if file is None:
            file = Defaults.FILES[0]
        if hidden and not file.startswith("."):
            file = "." + file

        file = self.settings[Keys.BASE] / Path(file)

        settings = dict()
        if str(self.settings[Keys.SRC]) != Defaults.SRC:
            settings[Keys.SRC] = str(self.settings[Keys.SRC])
        if str(self.settings[Keys.DIST]) != Defaults.DIST:
            settings[Keys.DIST] = str(self.settings[Keys.DIST])
        if self.settings[Keys.CLEAN] != Defaults.CLEAN:
            settings[Keys.CLEAN] = str(self.settings[Keys.CLEAN])
        settings[Keys.PLUGINS] = {
            plugin.__class__.__name__: plugin.save() for plugin in self._plugins
        }

        with open(file, "w", encoding="utf-8") as f:
            if mode == "json" or not mode and file.endswith(".json"):
                json.dump(settings, f, ensure_ascii=False, indent=4)

            if (
                mode == "yaml"
                or mode == "yml"
                or not mode
                and file.endswith(".yml")
                or not mode
                and file.endswith(".yaml")
            ):
                yaml.dump(settings, f, allow_unicode=True)

    def load(self, file=None, mode=None):
        """Loads a `hausse.json` settings file"""

        if file is None:
            for default in Defaults.FILES:
                if (self.settings[Keys.BASE] / Path(default)).exists():
                    file = self.settings[Keys.BASE] / Path(default)
                    break

        file = Path(file)

        try:
            with open(file) as settings:

                if mode == "json" or not mode and file.suffix == ".json":
                    settings = json.load(settings)

                elif (
                    mode == "yaml"
                    or mode == "yml"
                    or not mode
                    and file.suffix in [".yml", ".yaml"]
                ):
                    settings = yaml.load(settings)

                self.source(settings.get(Keys.SRC))
                self.destination(settings.get(Keys.DIST))
                self.clean(settings.get(Keys.CLEAN))

                plugins = import_module("hausse.plugins")

                for name, kwargs in settings.get("plugins", []).items():
                    plugin = getattr(plugins, name)
                    if plugin:
                        self.use(plugin(**kwargs))
        except:
            logging.warn(f"Failed to load {file} settings file.")

    # Aliases
    src = source
    dist = destination
    dest = destination
