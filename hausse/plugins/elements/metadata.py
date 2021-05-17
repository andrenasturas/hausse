import logging
from typing import List
from hausse.lib import Plugin, Element
from hausse.lib.selector import Selector

class Metadata(Plugin):

    """
    Metadata
    ========

    Adds metadata to a selection of elements.

    For each Element in the provided `selection`, each `new_metadata` items
    will be added as object arguments.

    Parameters
    ----------
    selection
        Elements to edit.
    new_metadata : dict
        A dictionnary of metadata elements added to the selected collection.
    replace : bool
        If True, allows the plugin to overwrite existing metadata in elements.
        
    """

    def __init__(self, selection, new_metadata, replace : bool = False):
        
        self.selection = Selector(selection)
        self.new_metadata = new_metadata
        self.replace = replace

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        selection = self.selection(elements, metadata, settings)

        for element in selection:
            for key, value in self.new_metadata.items():
                if not self.replace and hasattr(element, key):
                    # Prevent metadata overwritting
                    continue
                setattr(element, key, value)