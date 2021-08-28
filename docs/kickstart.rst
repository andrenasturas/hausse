Core features
#############

This page will walk you through the design of a rudimentary but functional site, starting from the hello-world project stated previously, and discovering in the process some of the core features of **hausse**.

Main settings
*************

By default, **hausse** works in the current directory, looks for sources files in ``src/`` folder and write final results in ``dist/`` folder. You can change this if necessary.

.. code-block:: python

    project = Hausse('./path/to/project')
    project.source('rel/to/project/sources')
    project.destination('rel/to/project/sources')

Project path is relative to the current execution path. All others paths are relative to the project path.

Templating
**********

Create a layout in ``layouts/layout.hbs``:

.. code-block:: handlebars

    <html>
        <head>
            <title>Awesome website</title>
        </head>
        <body>
            {{{ this }}}
        </body>
    </html>

And then, add the **Handlebars** layout plugin to the Hausse project.

.. code-block:: python
    :emphasize-lines: 7

    from hausse import Hausse
    from hausse.plugins import Markdown
    from hausse.plugins import Handlbars

    project = Hausse()
    project.use(Markdown())
    project.use(Handlbars())
    project.build()

The output ``dist/index.html`` file is now your Markdown content rendered in HTML and embedded into your template.

.. tip::
    It is possible to chain Hausse's method calls to write a more compact code.

    .. code-block:: python

        Hausse().use(Markdown()).use(Handlebars()).build()

Metadata
********

One important and useful concept in **hausse** is metadata. Plugin can add and use them on processed files. For example, **Markdown** plugin can read `YAML front matter <https://assemble.io/docs/YAML-front-matter.html>`_ of Markdown files.

Edit ``src/index.md`` to add metadata:

.. code-block:: markdown
    :emphasize-lines: 1,2,3

    ---
    date: 2021-05-03
    ---

    # My new website

    Here some contents

Modify the template to make use of these metadata.

.. code-block:: handlebars
    :emphasize-lines: 6

    <html>
        <head>
            <title>Awesome website</title>
        </head>
        <body>
            Date : {{ date }}
            {{{ this }}}
        </body>
    </html>


Collections
***********

One last very common concept often used: the Collections. They can be used to manage blog posts, tag lists, galleries, and any set of elements on your site.

Create a folder ``articles`` in you source directory, and write some articles into it. For example, in ``./src/articles/first-post.md``:

.. code-block:: markdown

    ---
    date: 2021-05-04
    title: My first blog post
    ---
    
    Hello there! I'm very **happy** to present my new blog build with Hausse!

Then, summon the Collection plugin.

.. code-block:: python
    :emphasize-lines: 7

    from hausse import Hausse
    from hausse.plugins import Markdown
    from hausse.plugins import Handlbars

    project = Hausse()
    project.use(Markdown())
    project.use(Collection('articles'))
    project.use(Handlbars())
    project.build()

Finally, modify your index template to list your articles on your main page.


.. code-block:: handlebars
    :emphasize-lines: 8-13

    <html>
        <head>
            <title>Awesome website</title>
        </head>
        <body>
            Date : {{ date }}
            {{{ this }}}
            <h2>My blog posts</h2>
            <ul>
                {{#each articles}}
                <li><a href="articles/{{ _filename }}>{{ title }}</a></li>
                {{/each}}
            </ul>
        </body>
    </html>
