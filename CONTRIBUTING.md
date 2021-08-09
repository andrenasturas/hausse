# Contributing to Hausse

Welcome here! Hausse is a little first project, originally intended for the creation of static web sites, but which seeks to be as versatile as possible. Feel free to contribute with new features and use cases!

- [Report bugs and request new features](#report-bugs-and-request-new-features)
- [Get started with the source code](#get-started-with-the-source-code)
  - [Begin from the start](#begin-from-the-start)
  - [Workspace setup](#workspace-setup)
  - [Tests](#tests)
  - [Conventions](#conventions)
  - [Pull request checklist](#pull-request-checklist)
- [Fix bugs or implement features](#fix-bugs-or-implement-features)
  - [Good first issues](#good-first-issues)
- [Improve the documentation](#improve-the-documentation)


## Report bugs and request new features

If you encounter a bug or a missing feature, file an issue in the [issue tracker](https://github.com/andrenasturas/hausse/issues).

For bugs, please include exhaustive informations about your operating system and specific used setup in your report, as well as steps to reproduce the bug.

## Get started with the source code

Hausse runs on Python 3.9. You can check your version by typing `python -V` in a console.

### Begin from the start

If all of this is new to you, feel free to consult [the language documentation](https://www.python.org/about/gettingstarted/). You will also need [git](https://git-scm.com/) to checkout the source code on your machine and pushing you contributions. Then, you can proceed and find [good first issues](#good-first-issues) to process!

### Workspace setup

Fisrt clone the repository:

```$ git clone https://github.com/andrenasturas/hausse.git```

Then install the dependencies. It is recommended to do so inside a [virtual environnement](https://docs.python.org/3/tutorial/venv.html).

```
$ cd hausse
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install -r requirements.txt
```

And then you are ready to code!

### Tests

In Hausse, testing is done with [`pytest`](https://pytest.org) library. You can run test with this command:

```$ python -m pytest```

### Conventions

Some conventions are enforced in this project:

- Source code must comply to PEP8 naming rules and black formatting rules.
- Commit messages should follow [conventional commits specification](https://www.conventionalcommits.org/). [Gitmojis](https://gitmoji.dev/) may be used as commits types.

### Pull request checklist

Before launching your pull request, make sure to check these little conditions:

- [x] All tests pass
- [x] New code is backed by new relevant tests
- [x] Documentation is updated accordingly
- [x] Code conventions are followed at best


## Fix bugs or implement features

Pick an open issue in the [issue tracker](https://github.com/andrenasturas/hausse/issues), [fork](https://github.com/andrenasturas/hausse/fork) the repository, [get started](#get-started) with a development workspace on your forked repository, commit your contribution and initiate a pull request on the issue.

### Good first issues

You are a beginner looking for interesting first issues ? You can look for [`good-first-issues` labelled issues](https://github.com/andrenasturas/hausse/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22).

## Improve the documentation

- You found a spot of documentation a bit unclear ?
- You would like to translate the guide ?
- Some method does not have its proper docstring ?
- You have an idea of a new sensible and simple use case example ?

Your help is very welcome. There is no such thing as overdocumented!