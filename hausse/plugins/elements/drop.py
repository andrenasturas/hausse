from typing import List

from hausse.lib import Project, SelectorPlugin
from hausse.lib.element import Element


class Drop(SelectorPlugin):
    """
    Drop specified elements from the current loaded elements.
    """

    def __call__(self, project: Project):
        for element in list(self.selector(project)):
            project.elements.remove(element)
