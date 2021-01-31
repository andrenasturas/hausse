from typing import List
import markdown2

from hausse.lib import Plugin, Element


class MetadataMarkdown(Plugin):
    """
    Parse elements metadata as Markdown to HTML.
    """

    def __init__(self, selection=None):
        self.extras = ['cuddled-lists', 'fenced-code-blocks', 'footnotes', 'header-ids', 'markdown-in-html', 'noreferrer', 'tag-friendly', 'task_list']
        
        if isinstance(selection, str):
            selection = [selection]
        self.selection = selection


    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        for element in elements:
            
            for key, value in element._metadata().items():
                
                if self.selection is None or key in self.selection:
                    setattr(element, key, markdown2.markdown(value, extras=self.extras))