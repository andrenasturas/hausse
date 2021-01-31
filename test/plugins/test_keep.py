import pytest

from pathlib import PurePath

from hausse.plugins import Keep
from hausse.lib import Element


def test_keep_simple_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    elements = [d1, d2, d3, d4]

    K = Keep("a/b/c")

    K(elements, None, None)

    assert len(elements) == 1
    assert d1 in elements
    assert d2 not in elements
    assert d3 not in elements
    assert d4 not in elements


def test_keep_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    elements = [d1, d2, d3, d4]

    K = Keep("a/*/c")

    K(elements, None, None)

    assert len(elements) == 2
    assert d1 in elements
    assert d2 not in elements
    assert d3 in elements
    assert d4 not in elements


def test_keep_multiple_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    elements = [d1, d2, d3, d4]

    K = Keep("**/c")

    K(elements, None, None)

    assert len(elements) == 3
    assert d1 in elements
    assert d2 not in elements
    assert d3 in elements
    assert d4 in elements
