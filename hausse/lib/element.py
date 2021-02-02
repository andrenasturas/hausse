import logging
from pathlib import Path, PurePath
from typing import Optional

class Element(object):
    """
        The Element stores processed files content and dedicated metadata.

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

    def __init__(self, path: PurePath, source: Optional[Path] = None, global_metadata: Optional[dict] = None, **kwargs):

        self._path = Path(path)
        self._filename = self._path.name
        self._global_metadata = global_metadata
        
        # Metadata
        for k, v in kwargs.items():
            setattr(self, k, v)

        # Content
        if source is not None and self._path is not None:
            self._load(source)


    def __getattr__(self, key):
        try:
            return self._global_metadata[key]
        except KeyError:
            raise AttributeError(f"'{self._filename}' Element has no attribute '{key}', nor has the global metadata")
        except TypeError:
            raise AttributeError(f"'{self._filename}' Element has no attribute '{key}', and global metadata is not accessible")
        

    def __str__(self):
        return self._contents

    
    def _metadata(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


    def _update_metadata(self, new: dict):
        for key, value in new.items():
            if key.startswith('_'):
                logging.warning(f"Adding a hidden metadata {key} in {self._filename} element.")
            if hasattr(self, key):
                logging.warning(f"Overwritting existant {key} metadata in {self._filename} element.")
            setattr(self, key, value)

    def _load(self, source):
        with open(Path(source) / Path(self._path), "r") as file:
            self._contents = file.read()