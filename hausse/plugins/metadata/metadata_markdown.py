from typing import List
import markdown2

from hausse.lib import Plugin, Element
from hausse.lib.selector import Selector, AllSelector


class MetadataMarkdown(Plugin):
    """
    MetadataMarkdown
    ================

    Parse elements metadata as Markdown to HTML.

    This plugin accepts any number of keys at initialization. Then, it will
    iterate over Elements and search in the metadata of each of them the
    values corresponding to the provided keys. Finally, it parse theses
    values as markdown documents to html documents.

    Values are modified in place. No Element is created by this plugin.

    An optional keyword argument, `selection`, can be used to limit this
    plugins cope to a subset of Elements. By default, all Elements of the
    project will be processed.

    Parameters
    ----------
    - `*args` ( str ) :
        Metadata keys containing the string to be parsed as metadata
    - `selection` ( Selector | str | Iterable[ Element ] ) :
        If provided, indicates which Elements should be processed.
        By default, all Elements are processed.
        Note that this parameter must be passed explicitly.

    Example
    -------
    ```python
        >>> element = Element("test")
        >>> element.foo = "# Foo Example\\nThis is a **nice** example."
        >>> plugin = MetadataMarkdown("foo")
        >>> plugin([element], dict(), dict())
        >>> print(element.foo)
        <h1 id="foo-example">Foo Example</h1>
        <p>This is a <b>nice</b> example
    ```

    Attributes
    ----------
    - `keys` ( List[ str ] ) :
        Metadata keys containing the string to be parsed as metadata
    - `selection` ( Selector ) :
        If provided, indicates which Elements should be processed.
        By default, all Elements are processed.
        Note that this parameter must be passed explicitly.

    """

    def __init__(self, *args, **kwargs):
        self.extras = ['cuddled-lists', 'fenced-code-blocks', 'footnotes', 'header-ids', 'markdown-in-html', 'noreferrer', 'tag-friendly', 'task_list']
        
        self.keys = set(args)
        self.selection = Selector(kwargs.get("selection", AllSelector()))


    def __call__(self, elements: List[Element], metadata: dict, settings: dict):

        for element in self.selection(elements, metadata, settings):
            
            for key in self.keys:
                
                value = element._metadata().get(key)
                
                if value:
                    setattr(element, key, markdown2.markdown(value, extras=self.extras))