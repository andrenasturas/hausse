import logging
from typing import List
from hausse.lib import Plugin, Element
from hausse.lib.selector import Selector

class Relations(Plugin):
    """
    Relations
    =========

    Create relations between elements based on a foreign key.

    For each Element in `selection`, this plugin will replace its `key` attribute, if present, by references to the corresponding Element in provided `collection`.

    # TODO: Finish documentation
    """

    def __init__(self, selection, collection, key = None):
        
        self.selection = Selector(selection)
        self.collection = collection if isinstance(collection, str) else collection.name
        self.key = key or self.collection


    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        if self.collection in settings["collections"]:

            collection = settings["collections"][self.collection]
            
            for element in self.selection(elements, metadata, settings):

                key = getattr(element, self.key, None)

                if key:

                    if isinstance(key, list):
                        setattr(element, self.key, [collection.get(elt, elt) for elt in key])
                        
                    else:
                        setattr(element, self.key, collection.get(key, key))
        
        else:

            if "collections" not in settings:
                logging.error(f"Relations plugin must be used after Collections plugin.")

            logging.error(f"Relations did not found {self.collection} collection in project metadata.")