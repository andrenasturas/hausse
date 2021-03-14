import glob
from pathlib import Path, PurePath
import os
from typing import List

from hausse.lib import Element, PathPlugin

class DiscoverPartials(PathPlugin):
    """
    Register layouts partials before layout engine plugin execution.
    """

    def __init__(self, path: str = "partials", pattern: str = "*.hbs"):
        super().__init__(path)
        self.pattern = pattern

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):
        
        settings['partials'] = dict()

        for f in self.path.rglob(self.pattern):

            with open(f, "r") as p:

                settings['partials'][PurePath(f).stem] = p.read()
