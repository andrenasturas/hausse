# import pytest
# import logging


# from hausse.plugins import Metadata

# LOG = logging.getLogger(__name__)


# def test_metadata_warn_underscore(caplog):

#     metadata = {"a": 1}
#     new = {"_b": 2}
    
#     m = Metadata(new)

#     with caplog.at_level(logging.WARNING):
#         m(None, metadata, None)

#     # Check metadata values
#     assert metadata.get("a") == 1
#     assert metadata.get("_b") == 2

#     # Check logging
#     assert "_b" in caplog.text

# def test_metadata_default(caplog):

#     metadata = {"a": 1, "bar": 2}
#     new = {"foo": 3, "bar": 4}
    
#     m = Metadata(new)

#     with caplog.at_level(logging.ERROR):
#         m(None, metadata, None)

#     # Check metadata values
#     assert metadata.get("a") == 1
#     assert metadata.get("bar") == 2
#     assert metadata.get("foo") == 3

#     # Check logging
#     assert "bar" in caplog.text


# def test_metadata_replace():

#     metadata = {"a": 1, "bar": 2}
#     new = {"foo": 3, "bar": 4}
    
#     m = Metadata(new, replace=True)
#     m(None, metadata, None)

#     assert metadata.get("a") == 1
#     assert metadata.get("bar") == 4
#     assert metadata.get("foo") == 3