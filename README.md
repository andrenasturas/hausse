<center>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="236px" height="236">
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#306998" stroke="ffd743" style="transform: scale(2) translateY(25px);"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#ffd43b" stroke="ffd743" style="transform: scale(2) translateX(28px) translateY(25px);"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#ffd43b" stroke="ffd743" style="transform: scale(2) translateX(14px)"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#ffd43b" stroke="ffd743" style="transform: scale(2) translateX(42px)"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#ffd43b" stroke="ffd743" style="transform: scale(2) translateX(14px) translateY(50px);"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#ffd43b" stroke="ffd743" style="transform: scale(2) translateX(42px) translateY(50px);"/>
    <polygon 
            points="24.8,22 37.3,29.2 37.3,43.7 24.8,50.9 12.3,43.7 12.3,29.2" 
            fill="#306998" stroke="ffd743" style="transform: scale(2) translateX(56px) translateY(25px);"/>
</svg>
</center>

# Hausse

Hausse is a python plugin-based static site generator. Designed to behave similarly to [Metalsmith](https://github.com/segmentio/metalsmith), Hausse works with plugins that can be chained to process files and produce the wanted result.

## Installation

```bash
pip install hausse
```

## How it works

First, you may create a Hausse project.

```python
project = Hausse()
```

Then, you can use the plugins you want. For example, if you want to parse markdown files, there is the **Markdown** plugin.

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

Finally, you can build your project.

```python
project.build()
```

For convenience, Hausse allows all its methods to be called in chain, and even using list of Plugins instead of registering them one by one.

```python
# Equivalent
Hausse.use(Markdown()).use(MetadataMarkdown("rich_metadata")).use(Handlebars()).build()
Hausse.use([Markdown(), MetadataMarkdown("rich_metadata"), Handlebars()]).build()
```

That's it ! All you have to do now is to select the right plugins for your project !

## Examples

Here are a few examples to illustrate the possibilities offered by Hausse and to inspire your future projects

- **[Blog](examples/blog)**. Just a simple blog.
- **[Portfolio](examples/portfolio)**, a single-page website featuring a résumé, skills overviews and projects showcases.
- **[Notes extraction](examples/notes)**, a presentation of a CSV file of a Notes app data extraction.

## what if I need a new plugin ?

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