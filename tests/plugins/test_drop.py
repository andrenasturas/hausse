from pathlib import PurePath

import pytest
from hausse.lib import Element, Project
from hausse.plugins import Drop


def test_drop_simple_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    D = Drop("a/b/c")

    D(project)

    assert len(project.elements) == 3
    assert d1 not in project.elements
    assert d2 in project.elements
    assert d3 in project.elements
    assert d4 in project.elements


def test_drop_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    D = Drop("a/*/c")

    D(project)

    assert len(project.elements) == 2
    assert d1 not in project.elements
    assert d2 in project.elements
    assert d3 not in project.elements
    assert d4 in project.elements


def test_drop_multiple_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    D = Drop("**/c")

    D(project)

    assert len(project.elements) == 1
    assert d1 not in project.elements
    assert d2 in project.elements
    assert d3 not in project.elements
    assert d4 not in project.elements
