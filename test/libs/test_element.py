from pathlib import Path
import pytest
from hausse.lib.element import Element

class TestElement:
    def test_init(self):
        
        text = "Lorem ipsum blahblah"
        path = Path("/test/foo/bar.ext")

        d = Element(path, arg1="Foo")
        d._contents = text

        assert d._filename == "bar.ext"
        assert str(d) == text
        assert getattr(d, "arg1") == "Foo"
        assert d._metadata() == {"arg1": "Foo"}

    
    def test_update(self):

        text = "Lorem ipsum blahblah"
        path = Path("/test/foo/bar.ext")

        d = Element(path, arg1="Foo")
        d._contents = text

        metadata = {
            "arg2": "Bar"
        }

        d._update_metadata(metadata)

        assert getattr(d, "arg2") == "Bar"
        assert d._metadata() == {"arg1": "Foo", "arg2": "Bar"}

        # TODO: Check pertinence
        d._contents = "Test"

        assert str(d) == "Test"
        assert getattr(d, "arg2") == "Bar"
        assert d._metadata() == {"arg1": "Foo", "arg2": "Bar"}