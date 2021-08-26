import logging
from typing import Optional

from ..utils import Defaults
from .element import Element


class Project(object):
    """
    A Project represents a set of files, metadata and settings.

    Parameters
    ----------
    path : PurePath
        Relative path of file location
    source : Path
        Path of the source folder from where the file is loaded
    global_metadata : dict
        Reference to the Hausse global metadata dict, for convenient access
    **kwargs :
        Any additional metadata to be added to the Element attributes
    """

    def __init__(
        self,
        elements: list[Element] = None,
        metadata: dict = None,
        settings: dict = None,
        **kwargs,
    ):

        # Data
        self.elements: list = elements or list()
        self.metadata: dict = metadata or dict()
        self.settings: dict = Defaults.SETTINGS | (settings or dict()) | kwargs

        # Metadata
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __getattr__(self, key):
        """Metadata attributes helper.

        Makes possible to look for project global metadata as attributes.
        """
        return self.metadata.get(key)
