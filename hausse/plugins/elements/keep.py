from typing import List
from hausse.lib import SelectorPlugin, Element


class Keep(SelectorPlugin):
    """
    Keep only specified elements and drop everything else.
    """

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):
        elements[:] = self.selector(elements, metadata, settings)
    