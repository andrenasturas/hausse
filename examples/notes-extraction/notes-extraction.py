from hausse import Hausse
from hausse.plugins import Markdown, CSVExpand, Collections, Layouts

# Project initialization
project = Hausse()

# Enable "dist" folder cleanup before writing new files
project.clean()

# Tells Hausse to load source files from "data" directory
# By default, Hausse will load files from "src" directory
project.source("data")

# Tells Hausse to write generated files in "dist" (default value)
project.dist("dist")

# Parse Markdown files
project.use(Markdown())

# CSVExpand genrate new Elements from a CSV file records
# Argument `delimiter` defines how to read CSV file (comma by default)
# Argument `contents_column` tells which column will fill the Element `_contents` attribute
# Argument `filename_column` tells which column will fill the Element `_filename` attribute
project.use(CSVExpand(delimiter="\t", contents_column="Data", filename_column="ID"))

# Since CSVExpand created Elements based on the CSV file in "notes" folder, we catch them all
project.use(
    Collections(
        {
            "notes":
            {
                "pattern": "notes/*"
            }
        }
    )
)

# We have a layout file for records rendering, let's use it by default for all of them
project.use(Layouts("layouts", "note.hbs"))

# Finally, build time
project.build()