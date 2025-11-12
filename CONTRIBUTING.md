google-site-verification  
3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

# Contributing

Contributors and contributions are welcome. Please read these guidelines first.

## Git `github`

The project homepage is on [GitHub](https://github.com/sr-murthy/continuedfractions).

Contributors can open pull requests from a fork targeting the parent `main`[branch](https://github.com/sr-murthy/continuedfractions/tree/main). But it may be a good first step to create an [issue](https://github.com/sr-murthy/continuedfractions/issues) or open
a [discussion topic](https://github.com/sr-murthy/continuedfractions/discussions).

## Repo `folder`

You will need to clone the repository first. As there are no dependencies there isn't much to set up, so this should be pretty simple. The minimum recommended version of Python is 3.10 as some of the type hinting may be incompatible with earlier versions.

## Dependencies `cubes`

Only standard libraries are used. See the [project TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml)
for more information.

Development dependencies are specified in the `[tool.pdm.dev-dependencies]` section of the TOML but these are purely indicative.

[PDM](https://pdm-project.org/latest) is used to manage all dependencies. It is also used to automate certain tasks, such as running
tests, as described in the section.

There are no root-level `requirements*.txt` files - but only a single (default, version-controlled, cross-platform)
[pdm.lock](https://github.com/sr-murthy/continuedfractions/blob/main/pdm.lock) lockfile. The lockfile is used with PDM to install all development dependencies, including the project itself, in editable mode where available:

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

## Tests `microscope`

Tests are defined in the `tests` folder and can be run directly or via the [Makefile](https://github.com/sr-murthy/continuedfractions/blob/main/Makefile), e.g. `make unitests` will run the unit tests. Linting can be performed with `make lint`, which requires [ruff](https://docs.astral.sh/ruff/) (specified in the dev. dependencies in the TOML). The doctests can be run with `make doctests`.

## Documentation `book`

[Project documentation](https://continuedfractions.readthedocs.io/en/latest/) is written and built using [Sphinx](https://www.sphinx-doc.org/en/master/), and deployed to [Read The Docs](https://readthedocs.org).

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

## CI `circle-play`

The main CI workflows are defined in the [CI YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/ci.yml)
and the [CodeQL Analysis YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/codeql-analysis.yml).

## Versioning and Releases `upload`

The latest release is `1.10.0`, and releases are created, tagged and published manually, not via a workflow.