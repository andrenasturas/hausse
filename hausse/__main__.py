import argparse
from pathlib import Path

from .utils import Defaults, Keys
from .hausse import Hausse

parser = argparse.ArgumentParser(prog="hausse", description="Modulable static project builder")

parser.add_argument("Path", type=str, nargs="?", help="Project folder or hausse.json file path")
parser.add_argument("-b", "--build", action="store_true", help="Builds the project")

args = parser.parse_args()

path = Path(args.Path or ".")

project = Hausse(path)

if path.is_file and path.exists():
    project.load(path)
else:
    project.load()

if args.build:
    project.build()

