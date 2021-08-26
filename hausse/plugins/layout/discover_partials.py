import glob
import os
from pathlib import Path, PurePath
from typing import List

from hausse.lib import PathPlugin, Project


class DiscoverPartials(PathPlugin):
    """
    Register layouts partials before layout engine plugin execution.
    """

    def __init__(self, path: str = "partials", pattern: str = "*.hbs"):
        super().__init__(path)
        self.pattern = pattern

    def __call__(self, project: Project):

        project.settings["partials"] = dict()

        for f in self.path.rglob(self.pattern):

            with open(f, "r") as p:

                project.settings["partials"][PurePath(f).stem] = p.read()
