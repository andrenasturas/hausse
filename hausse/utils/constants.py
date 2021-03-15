from pathlib import Path


# Main keys

class Keys:
    BASE = "base_dir"
    CLEAN = "clean"
    DIST = "dist_dir"
    SRC = "src_dir"
    PLUGINS = "plugins"


# Default values

class Defaults:
    FILES = ["hausse.json", "hausse.yaml", "hausse.yml", ".hausse.json", ".hausse.yaml", ".hausse.yml"]
    BASE = "."
    CLEAN = True
    DIST = "dist"
    SRC = "src"
    LAYOUTS = "layouts"
    SETTINGS = {Keys.BASE: Path(BASE), Keys.SRC: Path(SRC), Keys.DIST: Path(DIST), Keys.CLEAN: False}

