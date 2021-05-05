Plugins
#######

Plugins already provided by Hausse are presented on the Hausse project website and documented in the reference section. The article below describes how to create new plugins.

How it works
************

In Hausse, all the data of a project is stored in three variables : :envvar:`elements`, :envvar:`metadata` and :envvar:`settings`.

.. warning::
    The three variables shape may evolve until the first stable release of Hausse. They may be stored in a single special structure.


.. glossary::

    Elements
        An Element represent usually a file, as each source file is loaded as an Element, and all Element remeining after plugins work are written back as files.
        
        However, this concept can be extended to other things, as in the Records plugin that can create new Elements for each record of a CSV file, which can be used and written as separates files.

        The :envvar:`elements` variable is a list of Elements objects, with no specific order.

    Metadata
        :envvar:`metadata` is a dictionary storing arbitrary public values. This is where plugins should store any data that should be globally accessible by the user or other plugins.

        .. note:: For convenience, especially in the case of templating, global metadata are accessed as fallback when a requested metadata key is not found in a Element.

    Settings
        :envvar:`settings` is a dictionary storing values used as global settings on a project-scale level. Plugins may use this variable to store data, conventionally by using the plugin name as the metadata key, that have to be stored and accessible from other plugins, but not visible as global metadata.


Create a simple plugin
**********************

In Hausse, plugins are basically Python callables expecting specific variables and modifying them inplace. It is therefore possible to create a basic plugin by simply writing a Python method.

.. code-block:: python

    def foo(elements, metadata, settings):
        # processing elements and metadata


Selectors
*********

Often, a plugin must work on a reduced set of elements. For example, you may want to apply **Markdown** plugin on a particular collection only, and keep other files untouched. In order to allow precise project design without the need to code functions systematically, Hausse provides **Selectors**.

A Selector is a callable object that can be initialized with a criteria, and passed to a summoned plugin. When project build runs that plugin, the Selector object is called with the :envvar:elements argument, and returns a subsets of Elements corresponding to the defined criteria.

.. code-block:: python

    from hausse import Hausse
    from hausse.plugins import Markdown
    from hausse.selector import Extensions as Ext

    # Convert .markdown files to HTML, ignoring .md files
    Hausse().use(Markdown(Ext('.markdown'))).build()

Hausse provides several Selectors, allowing selection based on filename, extensions, path pattern or collection appartenance.

.. note:: The implementation of Selectors union and difference is planned.

Also, Selectors are compatible with the Save and Rebuild feature shown in the next page.

.. tip::
    Collections are Selectors.

    .. code-block:: python

        from hausse import Hausse
        from hausse.plugins import Markdown, Collection

        # Parsing markdown files in articles directory only and copying everything else
        articles = Collection('articles')
        Hausse().use(articles).use(Markdown(articles)).build()
    

Create a fully featured plugin
******************************

Usually, plugins are implemented as classes inheriting from ``Plugin`` or one of its subclasses. This implementation standardize plugins, simplify some recurrent behaviors, and may allow in the future more extensive use of plugins, like performance analysis and debugging.

A fully implemented Plugin should at least be instantiable and callable with the three arguments :envvar:`elements`, :envvar:`metadata` and :envvar:`settings`.