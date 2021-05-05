<center><img src="doc/hausse.png" alt="Hausse logo"/></center>

# Hausse

Hausse is a python plugin-based static site generator. It works with plugins that can be chained to process files and produce the wanted result.

## Installation

```bash
pip install hausse
```

## How it works

First, create a Hausse project.

```python
project = Hausse()
```

Then, use the **[plugins](/doc/plugins)** you need. For example, if you want to parse markdown files, there is the **Markdown** plugin.

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

- **[Blog](examples/blog)**. Just a simple blog.
- **[Portfolio](examples/portfolio)**, a single-page website featuring a résumé, skills overviews and projects showcases.
- **[Notes extraction](examples/notes-extraction)**, a presentation of a CSV file of a Notes app data extraction.

## What if I need a new plugin ?

Nothing more simple ! Writing a new plugin for Hausse is very easy. A Plugin is nothing more than a python object with a specific `__call__` method.

When `build()` is called on a Hausse project, all Plugins are successively _called_ as functions with the same arguments :

- `elements` is a **Element** list. A **Element** represents a file, with its own metadata accessible as object attributes, and content stored in `._contents` attribute.
- `metadata` is a dictionary of global metadata.
- `settings` is a dictionary of technical objects, deposited by some Plugins to be easily usable by others plugins.

```python
for plugin in plugins:
    plugin(elements, metadata, settings)
```

You may also implement the `__init__` method as you wish to store Plugin parameters that will be needed during the build.

## Why this name ?

The word `hausse` is the french name for a honey super. It thus refers to the grid that you set up for the bees to build a layer of the structure, which you then harvest.

One may also consider it as an acronym for _Highly Adjustable Universal Static Site Generator_.