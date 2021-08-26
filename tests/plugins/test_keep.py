from pathlib import PurePath

import pytest
from hausse.lib import Element, Project
from hausse.plugins import Keep


def test_keep_simple_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    K = Keep("a/b/c")

    K(project)

    assert len(project.elements) == 1
    assert d1 in project.elements
    assert d2 not in project.elements
    assert d3 not in project.elements
    assert d4 not in project.elements


def test_keep_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    K = Keep("a/*/c")

    K(project)

    assert len(project.elements) == 2
    assert d1 in project.elements
    assert d2 not in project.elements
    assert d3 in project.elements
    assert d4 not in project.elements


def test_keep_multiple_wildcard_pattern():

    d1 = Element(PurePath("a/b/c"))
    d2 = Element(PurePath("a/b/f"))
    d3 = Element(PurePath("a/k/c"))
    d4 = Element(PurePath("a/k/d/c"))

    project = Project([d1, d2, d3, d4])

    K = Keep("**/c")

    K(project)

    assert len(project.elements) == 3
    assert d1 in project.elements
    assert d2 not in project.elements
    assert d3 in project.elements
    assert d4 in project.elements
