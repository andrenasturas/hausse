from pathlib import PurePath

from hausse.lib import Element, Project
from hausse.plugins import Collection, Relations


def test_relations_default():

    e1 = Element("e1", c2=["e3", "e4"])
    e2 = Element("e2", c2="e3")
    e3 = Element("e3")
    e4 = Element("e4")

    c1 = Collection("c1", [e1, e2])
    c2 = Collection("c2", [e3, e4])

    r = Relations(c1, c2)

    assert r.collection == "c2"
    assert r.key is None

    p = Project([e1, e2, e3, e4])

    c1(p)
    c2(p)

    r(p)

    assert e3 in getattr(e1, "c2", [])
    assert e4 in getattr(e1, "c2", [])
    assert getattr(e2, "c2", []) is e3
