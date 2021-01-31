import logging

from hausse.lib import Plugin


# TODO: Delete this
@DeprecationWarning
class Metadata(Plugin):
    """
    Adds global metadata to the Hausse project. Added values are accessible globally.

    Parameters
    ----------
    additional_metadata : dict
        Dictionnary of metadata to be added in the Hausse project global metadata
    replace : bool
        If True, new metadata will overwrite without warning previous metadata with same key. Error is thrown otherway.

    """

    def __init__(self, additional_metadata: dict, replace: bool=False):
        
        self.replace = replace
        self.additional_metadata = additional_metadata


    def __call__(self, elements: list, metadata: dict, settings: dict):
        
        for key, value in self.additional_metadata.items():
            
            if key.startswith("_"):
                logging.warning(f"Additional metadata's key `{key}` starts with an underscore, which are usually used by system variables.")
            
            if not self.replace and key in metadata:
                logging.error(f"Attribute {key} already exists in current metadata, additional metadata value is skipped.")
            else:
                metadata[key] = value