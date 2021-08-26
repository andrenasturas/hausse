# Hausse

Hausse is a python plugin-based static site generator. It works with plugins that can be chained to process files and produce the wanted result.


![https://img.shields.io/pypi/v/hausse](https://pypi.org/project/hausse/) [![GitHub top language](https://img.shields.io/github/languages/top/andrenasturas/hausse)](https://github.com/andrenasturas/hausse/search?l=python) ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/andrenasturas/hausse) [https://img.shields.io/github/issues/andrenasturas/hausse/bug](https://github.com/andrenasturas/hausse/labels/bug) [https://img.shields.io/github/license/andrenasturas/hausse](https://github.com/andrenasturas/hausse/blob/main/LICENSE) [![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability-percentage/andrenasturas/hausse)](https://codeclimate.com/github/andrenasturas/hausse) [![Read the Docs](https://img.shields.io/readthedocs/hausse)](https://hausse.readthedocs.io)

## Installation

```bash
pip install hausse
```

## How it works

First, create a Hausse project.

```python
project = Hausse()
```

Then, use the **[plugins](/hausse/plugins)** you need. For example, if you want to parse markdown files, there is the **Markdown** plugin.

```python
project.use(Markdown())
```

You can use multiple plugins for more precise processing.

```python
# If your markdown files have rich metadata values, you can process them too
project.use(MetadataMarkdown("rich_metadata"))
# you may also render your pages with html page layouts
project.use(Handlebars())
```

Finally, build your project.

```python
project.build()
```

When your pipeline is done, you can save it to a `hausse.json` file.

```python
project.save()
```

This file allows you to build your project directly from command line.

```bash
python -m hausse path/of/your/project
```

That's it !

## Examples

Here are a few examples to illustrate the possibilities offered by Hausse and to inspire your future projects

- **[Portfolio](blueprints/portfolio)**, a single-page website featuring a résumé, skills overviews and projects showcases.
- **[Notes extraction](blueprints/notes-extraction)**, a presentation of a CSV file of a Notes app data extraction.

## What if I need a new plugin ?

Nothing more simple ! Writing a new plugin for Hausse is very easy. A Plugin is nothing more than a python object with a specific `__call__` method.

When `build()` is called on a Hausse project, all Plugins are successively _called_ as functions with the `Hausse` project object itself as an argument. Its attributes contains everything needed by the plugins:

- `elements` is a **Element** list. A **Element** represents a file, with its own metadata accessible as object attributes, and content stored in `._contents` attribute.
- `metadata` is a dictionary of global metadata.
- `settings` is a dictionary of technical objects, deposited by some Plugins to be easily usable by others plugins.

You may also implement the `__init__` method as you wish to store Plugin parameters that will be needed during the build.

Finally, if you feel like it should be added to hausse plugins, you can create a [plugin request](https://github.com/andrenasturas/hausse/issues/new?assignees=&labels=plugin&template=03_Plugin_request.md&title=Plugin%3A+).