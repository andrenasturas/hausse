import os
import shutil
from pathlib import Path
from typing import List

from hausse.lib import Element, PathPlugin, Project
from hausse.utils import Keys


class Assets(PathPlugin):
    """
    Assets
    ======

    Copy all files from an asset directory, bypassing all others plugins work.

    This plugin is useful for copying static files like CSS stylesheets.
    """

    def __init__(self, path: str = "assets"):
        super().__init__(path)

    def __call__(self, project: Project):
        for element in os.listdir(self.path):
            s = os.path.join(self.path, element)
            d = os.path.join(project.settings[Keys.DIST], element)

            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
