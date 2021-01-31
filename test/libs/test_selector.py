from hausse.plugins.elements.collection import BaseCollection, Collection
from pathlib import Path
import pytest
from hausse.lib.element import Element
from hausse.lib.selector import AllSelector, CollectionSelector, ElementsSelector, PathPatternSelector, Selector, ExtensionSelector


class TestSelector:
    def test_selector_wrapper(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())

        pattern = "foo/*"
        patternSelector = PathPatternSelector(pattern)
        patternGuess = Selector(pattern)

        iterable = elements[2:]
        iterableSelector = ElementsSelector(iterable)
        iterableGuess = Selector(iterable)

        # Selector called on a pattern string should return a PathPatternSelector
        assert isinstance(patternGuess, PathPatternSelector)

        # Selector called on an iterable on Elements should return a ElementsSelector 
        assert isinstance(iterableGuess, ElementsSelector)

        # Double-check equivalence
        assert set(patternGuess(*args)) == set(patternSelector(*args))
        assert set(iterableGuess(*args)) == set(iterableSelector(*args))
        
    def test_selector_all(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())

        assert set(AllSelector()(*args)) == set(elements)
        
    def test_selector_collection(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())
        collection = BaseCollection("test")
        collection.add(elements[0])
        collection.add(elements[1])
        collection(*args)

        assert set(CollectionSelector("test")(*args)) == set(elements[:2])

    def test_selector_elements(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())

        selector = ElementsSelector(elements[2:])

        assert set(selector(*args)) == set(elements[2:])

    def test_selector_extension(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())

        s1 = ExtensionSelector("ext")
        s2 = ExtensionSelector("EXT")
        s3 = ExtensionSelector(".ext")

        assert set(s1(*args)) == set(s2(*args)) == set(s3(*args)) == {elements[0], elements[2]}

    def test_selector_pattern(self):

        elements = [
            Element("foo/a.ext"),
            Element("foo/b.tld"),
            Element("bar/c.ext"),
            Element("bar/d.tld")
        ]

        args = (elements, dict(), dict())

        s1 = PathPatternSelector("bar/*")
        s2 = PathPatternSelector("*.tld")

        assert set(s1(*args)) == {elements[2], elements[3]}
        assert set(s2(*args)) == {elements[1], elements[3]}