from hausse.lib.selector import Selector, ElementsSelector, PathPatternSelector
from pathlib import PurePath
from typing import Callable, Generator, Iterable, List, Optional, Union

from hausse.lib import Plugin, Element
import logging


class BaseCollection(Plugin):

    def __init__(self, name):
        self.name = name
        self.members = []

    def __str__(self) -> str:
        return self.name

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def add(self, element: Element):

        if element in self.members:
            logging.debug(f"Element {element._filename} is already in {self.name} Collection.")
            return

        # Adding to internal element list
        self.members.append(element)

        # Create element collections attribute if it does not exists already
        if hasattr(element, "collections"):
            if isinstance(element.collections, list):
                element.collections = set(element.collections)
            elif not isinstance(element.collections, set):
                element.collections = {element.collections}            
        else:
            setattr(element, "collections", set())

        # Reverse-adding collection name and various attributes to element
        element.collections.add(self.name)

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        # Collection setup
        # Creating dedicated attribute in the settings
        if "collections" not in settings:
            settings["collections"] = dict()

        # Collection registration
        settings["collections"][self.name] = self

        # Metadata shortcut
        if self.name in metadata:
            logging.warning(
                f"Attribute {self.name} already exists in metadata, collection shortcut creation skipped."
            )
        else:
            metadata[self.name] = self


class IndexableCollection(BaseCollection):

    def __init__(self, name, indexBy):
        
        super().__init__(name)
        self.indexBy = indexBy
        self.index = dict()

    def __getitem__(self, key) -> Element:
        return self.index[key]

    def get(self, *args, **kwargs) -> Element:
        return self.index.get(*args, **kwargs)

    def add(self, element: Element):

        # Common adding process
        super().add(element)

        # Indexing the element in index dictionnary, if enabled
        if self.indexBy is not None:
            logging.debug(
                f"Collection {self.name} will be indexed using the {self.indexBy} attribute of elements."
            )

            index_name = getattr(element, self.indexBy)

            if index_name in self.index:
                logging.error(
                    f"Element {element._filename} has the same {self.indexBy} attribute as an already registered element, and will not be accessible from the {self.name} collection index."
                )
            elif index_name is None:
                logging.error(
                    f"Element {element._filename} has no {self.indexBy} attribute, and will not be accessible from the {self.name} collection index."
                )
            elif not isinstance(index_name, str):
                logging.error(
                    f"Element {element._filename} has a non-subscritable {self.indexBy} attribute, and will not be accessible from the {self.name} collection index."
                )
            else:
                self.index[index_name] = element


class Collection(IndexableCollection):
    """
    Collections
    ===========

    Used to group Elements.

    Example
    -------

    To build a static blog, articles documents may be grouped together.
    This creates a object that can be used to iterate over the articles.
    >>> Collection("articles", "articles/*")

    Once a Collection is created, it is stored `settings['collections'][name]`, where `name` is the first and required parameter.

    The Collection is also accessible directly by its name in global `metadata`, which allows usage of these kind of calls in layouts :

    ```handlebars
    {{#each articles}}
        {{> article_template this}}
    {{/each}}
    ```

    Attributes
    ----------
    - `name` (str) :
        Name of the Collection. This is the only mandatory parameter at initialization.
    - `selection` (Selector | str | iterable[Element]) :
        A Selector object to indicate which Elements should be added into the Collection.
        It can also be a filepath pattern string, or an iterable over the wanted Elements.
        If `None`, the pattern `"{name}/*`will be used by default, using the Collection's name.
    - `sortBy` (str | Callable) :
        #TODO: Implement sortBy
        Not yet implemented.
    - `indexBy` (str) :
        #TODO: Implement indexBy
        Not yet implemented.
    - `reverse` (bool) :
        #TODO: Implement reverse
        Not yet implemented.
    - `metadata` (dict) :
        Key-values fields to be added to the Collection.
    - `kwargs` (dict) :
        Any additional keyword argument will be added to the metadata of the Collection.
        Keywords arguments are added after `metadata` argument and overwrite its values if keys are present in both.
    """

    # TODO: Implement pattern, sortBy and reverse stuffs
    def __init__(
        self,
        name: str,
        selection: Union[Selector, str, Iterable[Element]] = None,
        sortBy: Union[str, Callable] = None,
        indexBy: Optional[str] = None,
        reverse: bool = False,
        metadata: dict = None,
        **kwargs,
    ):
        super().__init__(name, indexBy)

        self.selection = (
            Selector(selection) if selection else PathPatternSelector(f"{name}/*")
        )
        self.sortBy = sortBy
        self.reverse = reverse

        for k, v in (metadata or dict() | kwargs).items():
            setattr(self, k, v)

    
    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        super().__call__(elements, metadata, settings)

        # Collection filling
        for element in self.selection(elements, metadata, settings):
            self.add(element)


class Collections(Plugin):
    """
    Collections
    ===========

    Create multiple Collections, by selection and by metadata.

    This plugin will create automatically Collections based on the `collections` metadata of Elements if present.
    """
    
    def __init__(self, collections: dict = {}):

        self.collections = {
            name: Collection(name, **collection)
            for name, collection in collections.items()
        }

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        # Collections setup
        if not "collections" in settings:
            settings["collections"] = dict()

        # Collections registration
        # TODO: Possible optimization by not executing as plugin but filling all by once in elements loop ?
        for collection in self.collections:
            collection(elements, metadata, settings)

        # Parsing elements 
        for element in elements:

            # Check collection attr in element
            if hasattr(element, "collections"):    

                # Fix single intially set collection
                if isinstance(element.collections, list):
                    element.collections = set(element.collections)
                elif not isinstance(element.collections, set):
                    element.collections = {element.collections}

                # Iterating on set element collections
                for name in element.collections:

                    # Auto-creation
                    if name not in settings["collections"]:
                        BaseCollection(name)(elements, metadata, settings)

                    settings["collections"][name].add(element)