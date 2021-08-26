from pathlib import Path

import pytest
from hausse.lib.element import Element
from hausse.lib.project import Project
from hausse.lib.selector import All, Collection, Elements, Extensions, Pattern, Selector
from hausse.plugins.elements.collection import BaseCollection


class TestSelector:
    def test_selector_wrapper(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())

        pattern = "foo/*"
        patternSelector = Pattern(pattern)
        patternGuess = Selector(pattern)

        iterable = elements[2:]
        iterableSelector = Elements(iterable)
        iterableGuess = Selector(iterable)

        # Selector called on a pattern string should return a PathPatternSelector
        assert isinstance(patternGuess, Pattern)

        # Selector called on an iterable on Elements should return a ElementsSelector
        assert isinstance(iterableGuess, Elements)

        # Double-check equivalence
        assert set(patternGuess(project)) == set(patternSelector(project))
        assert set(iterableGuess(project)) == set(iterableSelector(project))

    def test_selector_all(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())

        assert set(All()(project)) == set(elements)

    def test_selector_collection(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())
        collection = BaseCollection("test")
        collection.add(elements[0])
        collection.add(elements[1])
        collection(project)

        assert set(Collection("test")(project)) == set(project.elements[:2])

    def test_selector_elements(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())

        selector = Elements(elements[2:])

        assert set(selector(project)) == set(elements[2:])

    def test_selector_extension(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())

        s1 = Extensions("ext")
        s2 = Extensions("EXT")
        s3 = Extensions(".ext")

        assert (
            set(s1(project))
            == set(s2(project))
            == set(s3(project))
            == {elements[0], elements[2]}
        )

    def test_selector_pattern(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld"),
        ]

        project = Project(elements, dict(), dict())

        s1 = Pattern("bar/*")
        s2 = Pattern("*.tld")

        assert set(s1(project)) == {elements[2], elements[3]}
        assert set(s2(project)) == {elements[1], elements[3]}
