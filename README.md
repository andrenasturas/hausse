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

```python
Hausse().use(Markdown()).use(Layouts())
```

## Why this name ?

The word `hausse` is the french name for a honey super. It thus refers to the grid that you set up for the bees to build a layer of the structure, which you then harvest.

One may also consider it as an acronym for _Highly Adjustable Universal Static Site Generator_.