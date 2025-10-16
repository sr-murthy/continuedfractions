google-site-verification  
3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

# Contributing

Contributors and contributions are welcome. Please read these guidelines first.

## Git

The project homepage is on [GitHub](https://github.com/sr-murthy/continuedfractions).

Contributors can open pull requests from a fork targeting the parent `main` [branch](https://github.com/sr-murthy/continuedfractions/tree/main). But it may be a good first step to create an
[issue](https://github.com/sr-murthy/continuedfractions/issues) or open a [discussion topic](https://github.com/sr-murthy/continuedfractions/discussions).

## Repo

You will need to clone the repository first. As there are no dependencies there isn't much to set up, so this should be pretty simple. The minimum recommended version of Python is 3.10 as some of the type hinting may be incompatible with earlier versions.

## Dependencies & PDM

The package uses only standard libraries, and no third party libraries are used. See the [project TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml) for more information.

Some development dependencies are specified in the `[tool.pdm.dev-dependencies]` section of the TOML including some
`'test'` dependencies, such as [pytest](https://docs.pytest.org/en/8.0.x/) and [pytest-cov](https://pytest-cov.readthedocs.io/).

[PDM](https://pdm-project.org/latest) is used to manage all dependencies and publish packages to PyPI. It is also used to automate certain tasks, such as running tests, as described in the section.

There are no root-level `requirements*.txt` files - but only a single (default, version-controlled, cross-platform) [pdm.lock](https://github.com/sr-murthy/continuedfractions/blob/main/pdm.lock) lockfile, which defines metadata for all TOML-defined development dependencies, including the currently empty set of production dependencies, and their sub-dependencies etc. This can be used to install all development dependencies, including the project itself, in editable mode where available:

``` shell
pdm install -v --dev
```

> [!NOTE]
> The `pdm install` command uses either the default lockfile (`pdm.lock`), or one specified with `-L <lockfile>`. Multiple lockfiles can be generated and maintained. Refer to the [PDM install documentation](https://pdm-project.org/latest/reference/cli/#install) for more information.

If you don't wish to install any editable dependencies, including the project itself, you can use:

``` shell
pdm install -v --dev --no-editable --no-self
```

The default lockfile can be updated with any and all upstream changes in the TOML-defined dependencies, but excluding any editable dependencies including the project itself, using:

``` shell
pdm update -v --dev --no-editable --no-self --update-all
```

This will usually modify `pdm.lock`, in which case the file should be staged and included in a commit.

The lockfile can be exported in its entirety to another format, such as `docs/requirements.txt` using:

``` shell
pdm export -v -f requirements --dev -o docs/requirements.txt
```

For more information on PDM lockfiles and installing requirements see the [PDM documentation](https://pdm-project.org/latest/).

## Tests

Tests are defined in the `tests` folder, and should be run with [pytest](https://pytest-cov.readthedocs.io/en/latest/).

There is a [Makefile](https://github.com/sr-murthy/continuedfractions/blob/main/Makefile) with different targets for linting (`lint`), running doctests (`doctests`) and unit tests (`unittests`):

``` shell
make lint
make unittests
make doctests
```

Unit tests can be run all at once using `make unittests` or individually using `pytest`, e.g. running the test class for the `~continuedfractions.lib.continued_fraction_rational` function:

``` shell
python -m pytest -sv tests/units/test_lib.py::TestContinuedFractionRational
```

The doctests are intended to test the docstring code examples, but can also be considered a form of acceptance tests. They can be run all at once using `make doctests`, or individually by library using `python -m doctest`, e.g. running all the doctests in
`~continuedfractions.sequences` (from the repo root):

``` shell
PYTHONPATH=src python -m doctest -v src/continuedfractions/sequences.py
```

## Documentation

[Project documentation](https://continuedfractions.readthedocs.io/en/latest/) is defined and built using [Sphinx](https://www.sphinx-doc.org/en/master/), and deployed to [Read The Docs](https://readthedocs.org). Currently, the building and deployment steps for documentation are manual, and not automated in a CI pipeline.

The Sphinx documentation source pages and assets are contained in the `docs/` subfolder. The HTML pages can be built locally on any branch (from the project root) using:

``` shell
make -C docs html
```

The pages will be built inside `docs/_build/html`, with the index/home page being `docs/_build/html/index.html`.

In order for this to work first ensure that you have installed the documentation Python requirements listed in `docs/requirements.txt`. This can be done either via `pip`:

``` shell
pip install -r docs/requirements.txt
```

or via [PDM](https://pdm.fming.dev/latest/):

``` shell
pdm install -v --dev --no-editable --no-self
```

## CI

The main CI workflows are defined in the [CI YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/ci.yml)
and the [CodeQL Analysis YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/codeql-analysis.yml).
Currently, pipelines for all branches include a tests stage that includes Ruff linting, unit tests,and doctests, in that order.

## Versioning and Releases

The latest release is `1.8.0`.

There is currently no dedicated pipeline for releases - both [GitHub releases](https://github.com/sr-murthy/continuedfractions/releases) and [PyPI packages](https://pypi.org/project/continuedfractions) are published manually, but both have the same version tag.
