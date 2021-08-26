Production
##########

Once your project is setup, the next step is to prepare the production workflow, i.e. automate the build and publication.

Save and Rebuild
****************

The Python script you wrote is useful to design your website, but when the design is done, it is no longer necessary. Instead, you can save your project to a JSON file, and use it directly from the console.

.. warning:: Custom plugins are not supported by the Save and Rebuild feature. If necessary, you have to stick to the design script and run it with python.


To do so, call the :py:func:`save` method on your project. The setting file name is ``hausse.json`` by default.

Rebuilding from the console is done by running the Hausse module with the :option:`--build` argument:

.. code-block:: bash

    python -m hausse hausse.json --build

.. tip:: You can skip the file  argument if one with a default name is present in current directory.


Publish
*******

You are now able to build your static website on-demand via a single command. While you can put the built static HTML files on a web server, you can also take advantage of this easy build process to use services such as `GitLab Pages <https://docs.gitlab.com/ee/user/project/pages/>`_ or `GitHub Pages <https://pages.github.com/>`_.

Example of GitLab Pages workflow:

.. code-block:: yaml

    image: python:latest
    variables:
        PIP_CACHE_DIR: "$CI_PROJECT_DIR/.cache/pip"
    cache:
        paths:
            - .cache/pip
            - .venv/
    before_script:
        - python -V
        - virtualenv .venv
        - source .venv/bin/activate
    pages:
        script:
            - pip install build pybars3 markdown2 pyyaml
            - python -m hausse --dist public --build
    artifacts:
        paths:
            -public

.. note:: GitLab looking for Pages files in a directory named ``public``, you should use the argument :option:`--dist` to fix the output directory accordingly. This is equivalent to adding ``.destination('public')`` in the design script.
