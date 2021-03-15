from hausse import Hausse
from hausse.plugins import (
    Assets,
    DiscoverPartials,
    Drop,
    Handlebars,
    Markdown,
    MetadataMarkdown,
    Relations,
    Collection,
    Collections
)

# Collections preparations

# By default, all files in "src/formations" folder will be grouped in this collection
Links = Collection("links")
# Using `indexBy` enables indexation, which is useful for building relations
Projects = Collection("projects", indexBy="title")
Skills = Collection("skills", indexBy="name")

h = Hausse("examples/portfolio")
h.clean()
h.use(
    # `use()` method register plugins into the Hausse project
    # It is possible to call `use()` once or multiple times, with one or a list of Plugins
    # In any cases, Plugins will be called in order.
    [
        # Assets plugin is used to simply dump static files, like stylesheets or icons
        # As it bypass all other plugins by copying directly files in "dist" folder,
        # it does not retrives files from "src/assets" but directly from "assets"
        Assets("assets"),

        # Markdown parses all markdown files found in "src"
        # Note that this plugin will also load as metadata all key-values present in headers
        Markdown(),

        # MetadataMarkdown parses markdown string found in files metadata
        MetadataMarkdown("summary"),

        # Collections (with a s) auto-creates collections based on files' "collections" metadata
        Collections(),

        # Each of the following defines a Collection and fill it with according files
        Links,
        Skills,
        Projects,

        # Relations helps making links between files in different collections
        # That's why Collections have been defined before Hausse() call
        # Other solution is to use CollectionSelector(collection_name) instead of the Collection
        Relations(Projects, Skills),

        # DiscoverPartials registers partials templates for Handlebars layout processing
        DiscoverPartials("templates"),

        # Handlebars does the actual layout processing to html files
        Handlebars("layouts", "layout.hbs", "index.md"),

        # Drop removes useless files from the project, before writing them in "dist"
        # Note that it does not remove the actual files from "src" folder
        # Here, it is used because we build a single page from multiple markdown files
        # Once the layout plugin processed them, used markdown files are no longer wanted
        Drop("*.md"),
    ]
)
# And here the magic happens. When `build()` is called, Hausse project generation begins
# Files from "src" directory are loaded and stored in a elements structure
# Every registered Plugin is called in order on the same set of elements, metadata and settings
# When all Plugins have been called, all files from elements are written in "dist" directory
h.build()
# Save will store the Hausse project configuration into a `hausse.json` file,
# which can be used later by Hausse in CLI mode operation : `python -m hausse
# hausse.json`. It is useful to simplify the project setup when development is
# done and it goes to production.
h.save()