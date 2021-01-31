import os
from hausse.lib.plugin import Plugin
import pytest
from pathlib import Path
from hausse import Hausse

def test_init_defaults():

    h = Hausse()

    assert isinstance(h._plugins, list)
    assert isinstance(h.elements, list)
    assert isinstance(h.settings, dict)
    assert isinstance(h.metadata, dict)
    assert Path(h.settings.get("base_dir")) == Path(".")
    assert Path(h.settings.get("src_dir")) == Path("src")
    assert Path(h.settings.get("dist_dir")) == Path("dist")


def test_init_additional_settings():

    h = Hausse(arg1="Foo", arg2="Bar")
    
    assert h.settings.get("arg1") == "Foo"
    assert h.settings.get("arg2") == "Bar"


def test_init_paths():

    h = Hausse(base_dir=Path("a/b/c"), src_dir="d/e/f", dist_dir=Path("g/h"))
    
    assert Path(h.settings.get("base_dir")) == Path("a/b/c")
    assert Path(h.settings.get("src_dir")) == Path("d/e/f")
    assert Path(h.settings.get("dist_dir")) == Path("g/h")


def test_source():

    h = Hausse()

    h.source("d/e/f")

    assert Path(h.settings.get("src_dir")) == Path("d/e/f")


def test_dist():

    h = Hausse()

    h.dist("g/h")

    assert Path(h.settings.get("dist_dir")) == Path("g/h")


def test_clean():

    h = Hausse()

    h.clean()

    assert h.settings.get("clean") is True

    h.clean(False)

    assert h.settings.get("clean") is False


def test_use():

    class FooPlugin(Plugin):
        def __init__(self):
            pass
        def __call__(self):
            pass

    h = Hausse()
    p1 = FooPlugin()
    p2 = FooPlugin()

    h.use(p1)
    h.use(p2)

    assert h._plugins[0] is p1
    assert h._plugins[1] is p2


def test_build():

    H = Hausse()
    H.source("test")
    H.dist("test")

    # Saving original working directory
    owd = os.getcwd()

    #H.build()
    # TODO: Implement test
    # Check non modified current directory
    assert os.getcwd() == owd

    assert False
