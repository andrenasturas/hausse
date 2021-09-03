from pathlib import Path

from hausse.utils import clean_dir


def test_clean_dir(tmp_path):

    d = tmp_path / "target"
    d.mkdir()

    Path(d / "folder").mkdir()
    Path(d / "folder" / "file").touch()
    Path(d / "file").touch()

    clean_dir(d)

    assert not any(d.iterdir())
