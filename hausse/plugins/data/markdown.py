from typing import List

from hausse.lib import Project, SelectorPlugin
from hausse.lib.selector import Extensions
from markdown2 import markdown


class Markdown(SelectorPlugin):
    """
    Markdown
    ========

    Parse Markdown files to HTML.

    Parameters
    ----------
    selection
        Files to parse. By default, all files with `.md` or `.markdown` extensions are selected.
    extras : List of str
        Extras settings passed to the markdown processor.
    """

    default_extras = [
        "cuddled-lists",
        "fenced-code-blocks",
        "footnotes",
        "header-ids",
        "markdown-in-html",
        "metadata",
        "noreferrer",
        "tag-friendly",
        "task_list",
    ]

    def __init__(self, selection=None, extras: List[str] = None):

        super().__init__(selection, Extensions("md", "markdown"))
        self.extras = extras

    def __call__(self, project: Project):

        for element in self.selector(project):
            m = markdown(element._contents, extras=self.extras or self.default_extras)
            element._contents = str(m)
            element._update_metadata(m.metadata)
