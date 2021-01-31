import glob
from pathlib import Path, PurePath
import os
from typing import List

from hausse.lib import Element, Plugin

class DiscoverPartials(Plugin):
    """
    Register layouts partials before layout engine plugin execution.
    """

    def __init__(self, directory: str = "partials", pattern: str = "*.hbs"):
        self.directory = Path(directory)
        self.pattern = pattern

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):
        
        settings['partials'] = dict()

        for f in self.directory.rglob(self.pattern):

            with open(f, "r") as p:

                settings['partials'][PurePath(f).stem] = p.read()
