import pytest

from pathlib import PurePath

from hausse.plugins import Collections, Collection
from hausse.lib import Element


def test_collection_add():
    

    d1 = Element(PurePath("a/b/c"))

    collection = Collection("test")

    collection.add(d1)

    assert d1 in collection
    assert collection.name in d1.collections


def test_collections_init():

    # TODO: test more accurately pattern matching

    c = Collections({
        "test_a": {
            "pattern": "a/**/*"
        },
        "test_a/b": {
            "pattern": "a/b/*",
            "reverse": True
        }
    })

    assert len(c.collections) == 2


def test_collections_call():

    # TODO: Test Collections sub-methods instead of main call method
    # TODO: Test more accurately collection members indexing and sorting

    elements = []
    settings = dict()
    metadata = dict()

    d1 = Element(PurePath("a/b/c"), global_metadata=metadata)
    d2 = Element(PurePath("a/b/f"), global_metadata=metadata)
    d3 = Element(PurePath("a/k/c"), global_metadata=metadata)
    d4 = Element(PurePath("a/b/d/c"), global_metadata=metadata)

    elements.append(d1)
    elements.append(d2)
    elements.append(d3)
    elements.append(d4)

    c = Collections({
        "test_a": {
            "selector": "**/c"
        },
        "test_b": {
            "selector": "a/b/*",
            "reverse": True
        }
    })

    c(elements, metadata, settings)

    # Check plugin settings entry
    assert "collections" in settings

    c1 = settings.get("collections", {}).get("test_a")
    c2 = settings.get("collections", {}).get("test_b")

    # Check collection creation
    assert isinstance(c1, Collection)
    assert isinstance(c2, Collection)

    # Check collection setup
    assert getattr(c1, "name") == "test_a"
    assert getattr(c2, "name") == "test_b"

    # Check correct collections assignement
    assert str(c1) in getattr(d1, "collections", [])
    assert str(c1) in getattr(d3, "collections", [])
    assert str(c1) in getattr(d4, "collections", [])
    assert str(c2) in getattr(d1, "collections", [])
    assert str(c2) in getattr(d2, "collections", [])
    assert str(c2) not in getattr(d3, "collections", [])
    assert str(c2) not in getattr(d4, "collections", [])

    # Check global metadata binding
    assert metadata.get("test_a") == c1
    assert metadata.get("test_b") == c2

    # Check global metadata access
    assert getattr(d4, "test_b") == c2

    # Check collection elements order
    assert list(c1) == [d1, d3, d4]
    assert list(c2) == [d2, d1]
