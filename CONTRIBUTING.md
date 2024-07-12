google-site-verification  
3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

# Contributing

Contributors and contributions are welcome. Please read these guidelines
first.

## Git

The project homepage is on
[GitHub](https://github.com/sr-murthy/continuedfractions).

Contributors can open pull requests from a fork targeting the parent
`main`
[branch](https://github.com/sr-murthy/continuedfractions/tree/main). But
it may be a good first step to create an
[issue](https://github.com/sr-murthy/continuedfractions/issues) or open
a [discussion
topic](https://github.com/sr-murthy/continuedfractions/discussions).

A simple Git workflow, using a feature and/or fix branch created off the
`main` branch of your fork, is recommended.

## Repo

If you wish to contribute please first ensure you have [SSH access to
GitHub](https://docs.github.com/en/authentication/connecting-to-github-with-ssh).
This basically involves creating a project-specific SSH keypair - if you
don't already have one - and adding it to GitHub. If you have done this
successfully then this verification step should work:

``` bash
ssh -vT git@github.com
```

Some SSH configuration may be required: on MacOS or Linux your
user-defined SSH configuration file (`~/.ssh/config`) should look
something like this:

``` shell
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  ForwardAgent yes
  Preferredauthentications publickey
  IdentityFile ~/.ssh/<SSH private key filename>
  PasswordAuthentication no
```

For Windows please consult the [Windows OpenSSH
documentation](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_server_configuration).

Once you’ve forked the repository, you can clone your fork, e.g. over
SSH:

``` python
git clone git+ssh://git@github.com/<fork user>/continuedfractions
```

You can create additional remotes for the parent project to enable
easier syncing, or you can simply create PRs directly against the parent
project.

## Dependencies & PDM

The package has no external (production) dependencies - some development
dependencies are specified in the `[tool.pdm.dev-dependencies]` section
of the [project
TOML](https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml),
but they are not mandatory. Of these, the most important are probably
the `'test'` dependencies, including
[pytest](https://docs.pytest.org/en/8.0.x/) and
[pytest-cov](https://pytest-cov.readthedocs.io/):

``` toml
test = [
    "coverage[toml]",
    "pytest",
    "pytest-cov",
    "pytest-xdist",
]
```

[PDM](https://pdm-project.org/latest) is used (by myself, currently, the
sole maintainer) to manage all dependencies and publish packages to
PyPI. It is also used to automate certain tasks, such as running tests,
as described in the section.

There are no root-level `requirements*.txt` files - but only a single
(default, version-controlled, cross-platform)
[pdm.lock](https://github.com/sr-murthy/continuedfractions/blob/main/pdm.lock)
lockfile, which defines metadata for all TOML-defined development
dependencies, including the currently empty set of production
dependencies, and their sub-dependencies etc. This can be used to
install all development dependencies, including the project itself, in
editable mode where available:

``` bash
pdm install -v --dev
```

> [!NOTE]
> It is important to note that `pdm install` uses either the default
> lockfile (`pdm.lock`), or one specified with `-L <lockfile>`. Multiple
> lockfiles can be generated and maintained. Refer to the [PDM install
> documentation](https://pdm-project.org/latest/reference/cli/#install)
> for more information.

If you don't wish to install any editable dependencies, including the
project itself, you can use:

``` bash
pdm install -v --dev --no-editable --no-self
```

The default lockfile can be updated with any and all upstream changes in
the TOML-defined dependencies, but excluding any editable dependencies
including the project itself, using:

``` bash
pdm update -v --dev --no-editable --no-self --update-all
```

This will usually modify `pdm.lock`, in which case the file should be
staged and included in a commit.

The lockfile can be exported in its entirety to another format, such as
`docs/requirements.txt` using:

``` bash
pdm export -v -f requirements --dev -o docs/requirements.txt
```

For more information on PDM lockfiles and installing requirements see
the [PDM documentation](https://pdm-project.org/latest/).

## Tests `microscope`

Tests are defined in the `tests` folder, and should be run with
[pytest](https://pytest-cov.readthedocs.io/en/latest/).

For convenience different types of test targets are defined in the
[Makefile](https://github.com/sr-murthy/continuedfractions/blob/main/Makefile):
`lint` for Ruff linting, `doctests` for running
[doctests](https://docs.python.org/3/library/doctest.html) and
`unittests` for running unittests and measuring coverage, using `pytest`
and the `pytest-cov` plugin:

``` bash
make lint
make unittests
make doctests
```

Linting warnings should be addressed first. The doctests serve as
acceptance tests, and are best run after the unit tests.

## Documentation

[Project
documentation](https://continuedfractions.readthedocs.io/en/latest/) is
defined and built using [Sphinx](https://www.sphinx-doc.org/en/master/),
and deployed to [Read The Docs](https://readthedocs.org). Currently, the
building and deployment steps for documentation are not automated in a
CI pipeline, but are done manually - this will be addressed in future
releases.

The Sphinx documentation can be built locally on any branch from the
**project root** using:

``` bash
make -C docs html
```

First, ensure that you have installed the docs Python requirements,
which include all development dependencies, either via `pip`:

``` bash
pip install -r docs/requirements.txt
```

or via [PDM](https://pdm.fming.dev/latest/):

``` bash
pdm install -v --dev --no-editable --no-self
```

## CI/CD

The CI/CD pipelines are defined in the [CI
YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/ci.yml)
and the [CodeQL Analysis
YML](https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/codeql-analysis.yml),
and pipelines for all branches include a tests stage, consisting of Ruff
linting, Python doctests, and unit tests, in that order. This will be
amended in the future to ensure that tests are only run on updates to
PRs targeting `main`, to avoid duplication on `main`.

## Versioning and Releases

The [PyPI package](https://pypi.org/project/continuedfractions/) is
currently at version `0.17.3` - the goal is to use [semantic
versioning](https://semver.org/) consistently for all future releases,
but some earlier releases do not comply with strict semantic versioning.

There is currently no dedicated pipeline for releases - both [GitHub
releases](https://github.com/sr-murthy/continuedfractions/releases) and
[PyPI packages](https://pypi.org/project/continuedfractions) are
published manually, but both have the same version tag.

Pipelines for releases will be added as part of a future release.