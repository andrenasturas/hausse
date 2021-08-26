from typing import List

from hausse.lib import Element, Project, SelectorPlugin


class Keep(SelectorPlugin):
    """
    Keep only specified elements and drop everything else.
    """

    def __call__(self, project: Project):
        project.elements[:] = self.selector(project)
