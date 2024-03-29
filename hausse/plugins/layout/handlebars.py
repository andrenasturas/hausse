import glob
import logging
import os
import pathlib
from pathlib import Path, PurePath
from typing import List

import pybars
from hausse.lib import Element, LayoutPlugin, Project


class Handlebars(LayoutPlugin):
    """
    Apply handlebars layouts to elements
    """

    def __call__(self, project: Project):

        # Compiler init
        compiler = pybars.Compiler()

        # Partials compilation
        partials = project.settings.get("partials", dict())
        for name, partial in partials.items():
            partials[name] = compiler.compile(partial)

        # Templates compilation
        templates = project.settings.get("templates", dict())
        for file in self.path.rglob("*.hbs"):
            with open(file, "r") as layout:
                if PurePath(file).name in templates:
                    logging.warning(
                        f"A layout file named {PurePath(file).name} has already been registered. The new one is skipped."
                    )
                else:
                    templates[PurePath(file).name] = compiler.compile(layout.read())

        for element in self.selector(project):

            # Template selection
            template = templates.get(getattr(element, "layout", self.default))

            if template is None:
                logging.info(
                    f"Element {element._filename} with no defined layout is skipped."
                )

            else:
                # Render
                element._contents = template(element, partials=partials)
                element._path = element._path.with_suffix(".html")
