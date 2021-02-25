

import os
from pathlib import Path
import shutil
from typing import List

from hausse.lib import Plugin, Element
from hausse.utils import Keys


class Assets(Plugin):
    """
        Assets
        ======

        Copy all files from an asset directory, bypassing all others plugins work.

        This plugin is useful for copying static files like CSS stylesheets.
    """

    def __init__(self, path: str = "public"):
        self.path = Path(path)

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):
        for element in os.listdir(self.path):
            s = os.path.join(self.path, element)
            d = os.path.join(settings[Keys.DIST], element)

            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d) 