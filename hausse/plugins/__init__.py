"""
Plugins
=======

This module contains all available Hausse plugins.

"""

from .assets import Assets

from .csv_expand import CSVExpand

# Elements organization plugins
from .elements.drop import Drop
from .elements.keep import Keep
from .elements.collection import Collection, Collections
from .elements.relations import Relations
from .elements.index import Index

# Layouts-related plugins
from .layout.handlebars import Handlebars
from .layout.layouts import Layouts
from .layout.discover_partials import DiscoverPartials

# Data processing plugins
from .data.markdown import Markdown

# Metadata processing plugins
from .metadata.metadata_markdown import MetadataMarkdown