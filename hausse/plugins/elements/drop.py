from hausse.lib.element import Element
from typing import List
from hausse.lib import SelectorPlugin

class Drop(SelectorPlugin):
    """
    Drop specified elements from the current loaded elements.
    """

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):
        for element in list(self.selector(elements, metadata, settings)):
            elements.remove(element)
    