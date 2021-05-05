Getting Started
###############

What is Hausse?
***************

Hausse is a modular project generator, mainly used to build static websites. It collects files from a source folder, process them using a chosen set of plugins, and write them into an output folder.

.. note::
   Hausse plugin-based behaviour is similar to the NodeJS project `Metalsmith <https://metalsmith.io>`_.

Hausse is shipped with a fair amount of plugins.


Installation
************

Hausse is available on `PyPI <https://pypi.org/project/hausse/>`_.

.. code-block:: bash

   pip install hausse

In order to generate static websites, you will probably need additional packages:

* `markdown2 <https://pypi.org/project/markdown2>`_ for Markdown language processing
* `pybars3 <https://pypi.org/project/pybars3>`_ for Handlebars templates

Due to the versatility of Hausse, these dependencies are optional and are not automatically installed with it.
   
Hello world
***********

Let's build a very simple static website. Write the following into ``src/index.md``.

.. code-block:: markdown

   # My new website

   Here some contents

Then, open a Python file and write the following code:

.. code-block:: python

   from hausse import Hausse
   from hausse.plugins import Markdown

   project = Hausse()
   project.use(Markdown())
   project.build()

This code create a new Hausse project in the current directory, summons the **Markdown** plugin and triggers the project build, writing the result in ``dist/index.html``.

That's it ! You now have the basics to build nice static websites.