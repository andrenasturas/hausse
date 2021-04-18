from hausse.lib import Element
import pytest
import logging


from hausse.plugins import Markdown

LOG = logging.getLogger(__name__)


def test_markdown():

    elt = Element("a.md")
    elt._contents = "# H1\n\nLorem Ipsum\n"

    M = Markdown()

    M([elt], None, None)

    assert elt._contents == '<h1 id="h1">H1</h1>\n\n<p>Lorem Ipsum</p>\n'


def test_markdown_metadata():

    elt = Element("a.md")
    elt._contents = "---\nfoo: test a\nbar: test b\n---\n# H1\n\nLorem Ipsum\n"

    M = Markdown()

    M([elt], None, None)

    assert elt._contents == '<h1 id="h1">H1</h1>\n\n<p>Lorem Ipsum</p>\n'
    assert getattr(elt, "foo") == 'test a'
    assert getattr(elt, "bar") == 'test b'