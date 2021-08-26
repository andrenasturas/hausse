"""
Plugins
=======

This module contains all available Hausse plugins.

"""

from .assets import Assets
from .csv_expand import CSVExpand

# Data processing plugins
from .data.markdown import Markdown
from .elements.collection import Collection, Collections

# Elements organization plugins
from .elements.drop import Drop
from .elements.index import Index
from .elements.keep import Keep
from .elements.relations import Relations
from .layout.discover_partials import DiscoverPartials

# Layouts-related plugins
from .layout.handlebars import Handlebars
from .layout.layouts import Layouts

# Metadata processing plugins
from .metadata.metadata_markdown import MetadataMarkdown
