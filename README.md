# hausse

**hausse** is a python plugin-based static site generator. It works with plugins that can be chained to process files and produce the wanted result.


## Installation

```bash
pip install hausse
```

## How it works

First, create a hausse project.

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

### Going to production

When your pipeline is done, you can save it to a `hausse.json` file.

```python
project.save()
```

This file allows you to build your project directly from command line.

```bash
python -m hausse path/of/your/project
```

That's it !

### What if I need a new plugin ?

Nothing more simple ! Writing a new plugin for Hausse is very easy. A Plugin is nothing more than a python object with a specific `__call__` method.

When `build()` is called on a Hausse project, all Plugins are successively called as functions with the `Hausse` project object itself as an argument. Its attributes contains everything needed by the plugins:

- `elements` is a **Element** list. A **Element** represents a file, with its own metadata accessible as object attributes, and content stored in `._contents` attribute.
- `metadata` is a dictionary of global metadata.
- `settings` is a dictionary of technical objects, deposited by some Plugins to be easily usable by others plugins.

You may also implement the `__init__` method as you wish to store Plugin parameters that will be needed during the build.

Finally, if you feel like it should be added to hausse plugins, do not hesitate to [contribute](CONTRIBUTING.md)!
## Documentation

A detailled documentation is available on [Read The Docs](https://hausse.readthedocs.io).

## Contributing

Contributions are always welcome! See [`CONTRIBUTING.md`](CONTRIBUTING.md) for ways to get started.

## Roadmap

- Plugins, more plugins!
- Ease bootstrap
- Standalone build

## Related

The plugin-based generator principle is inspired by [Metalsmith](https://metalsmith.io/), a similar tool written in javascript.

## Examples

Here are a few examples to illustrate the possibilities offered by Hausse and to inspire your future projects

- **[Portfolio](blueprints/portfolio)**, a single-page website featuring a résumé, skills overviews and projects showcases.
- **[Notes extraction](blueprints/notes-extraction)**, a presentation of a CSV file of a Notes app data extraction.

## License

[MIT License](https://choosealicense.com/licenses/mit/).
