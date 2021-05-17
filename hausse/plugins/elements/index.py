import logging
from typing import List
from pathlib import Path
from hausse.lib import Plugin, Element

class Index(Plugin):

    """
    Index
    =====

    Adds index in directory

    Useful to create an index page ex-nihilo without specific content.

    Parameters
    ----------
    directory : Path
        Directory where to create an index file. `.` by default.
    filename : Path
        Index filename. `index.html` by default.
    metadata : dict
        Metadata passed to the new index Element.
    **kwargs
        Metadata passed to the new index Element.
    """

    def __init__(self, directory : Path = None, filename : str = "index.html", metadata : dict = None, **kwargs):
        
        self.directory = Path(directory) or Path(".")
        self.filename = filename
        self.metadata = metadata or dict() | kwargs

    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        elements.append(Element(self.directory / Path(self.filename), global_metadata=metadata, **self.metadata))
    