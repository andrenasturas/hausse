import logging
from pathlib import Path
from typing import List

from hausse.lib import Element, Plugin, Project


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

    def __init__(
        self,
        directory: Path = None,
        filename: str = "index.html",
        metadata: dict = None,
        **kwargs
    ):

        self.directory: Path = Path(directory) if directory else Path(".")
        self.filename: str = filename
        self.metadata: dict = metadata or dict() | kwargs

    def __call__(self, project: Project):

        project.elements.append(
            Element(
                self.directory / Path(self.filename),
                global_metadata=project.metadata,
                **self.metadata
            )
        )
