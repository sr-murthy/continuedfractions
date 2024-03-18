============
Contributing
============

The project homepage is on `GitHub <https://github.com/sr-murthy/continuedfractions>`_.

Contributors and contributions are welcome via pull requests from a fork targeting the parent ``main`` `branch <https://github.com/sr-murthy/continuedfractions/tree/main>`_.

A simple Git workflow, using a feature and/or fix branch created off the ``main`` branch of your fork, is recommended.

.. _contributing.cloning:

Cloning
=======

If you wish to contribute please first ensure you have `SSH access to GitHub <https://docs.github.com/en/authentication/connecting-to-github-with-ssh>`_. If you do then this should work:

.. code:: bash

   ssh -vT git@github.com

If not please follow the SSH instructions linked above.

Once you’ve forked the repository, it is recommended to clone your fork over SSH:

.. code:: python

   git clone git+ssh://git@github.com/<fork user>/continuedfractions

.. _contributing.dependencies-and-pdm:

Dependencies & PDM
==================

As mentioned earlier, the package has no (production) dependencies, but groups of development requirements are specified in the
``[tool.pdm.dev-dependencies]`` section of the `project TOML <https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml>`_. Of these only the ``'test'`` dependencies,
including `pytest <https://docs.pytest.org/en/8.0.x/>`_ and `pytest-cov <https://pytest-cov.readthedocs.io/>`_, are important.

.. code:: toml

   test = [
       "coverage[toml]",
       "pytest",
       "pytest-cov",
       "pytest-xdist",
   ]

`PDM <https://pdm-project.org/latest>`_ is used (by myself, currently, the sole maintainer) to manage all dependencies and publish packages to PyPI. It is also used to automate certain tasks, such as running tests, as described in the section.

There are no root-level ``requirements*.txt`` files - but only a single (default, version-controlled, cross-platform) `pdm.lock <https://github.com/sr-murthy/continuedfractions/blob/main/pdm.lock>`_ lockfile, which defines metadata for all TOML-defined development dependencies, including the currently empty set of production dependencies, and their sub-dependencies etc. This can be used to install all development dependencies, including the project itself, in editable mode where available:

.. code:: bash

   pdm install -v --dev

.. note::

   It is important to note that the :command:`pdm install` uses either the default :file:`pdm.lock` lockfile, or one specified with :command:`-L <lockfile>`. Multiple lockfiles can be generated and maintained. Refer to the `PDM documentation <https://pdm-project.org/latest/reference/cli/#install>`_ for more information.

If you don't wish to install any editable dependencies, including the project itself, you can use:

.. code:: bash

   pdm install -v --dev --no-editable --no-self

The default lockfile can be updated with any and all upstream changes in the TOML-defined dependencies, but excluding any editable dependencies including the project itself, using:

.. code:: bash

   pdm update -v --dev --no-editable --no-self --update-all

This will usually modify :file:`pdm.lock`, in which case the file should be staged and included in a commit.

The lockfile can be exported in its entirety to another format, such as :file:`docs/requirements.txt` using:

.. code:: bash

   pdm export -v -f requirements --dev -o docs/requirements.txt

For more information on PDM lockfiles and installing requirements see the `PDM documentation <https://pdm-project.org/latest/>`_.

.. _contributing.makefile-and-tests:

Makefile and Tests
==================

The `Makefile <Makefile>`_ defines three main targets: ``lint`` for Ruff linting, ``doctests`` for running
`doctests <https://docs.python.org/3/library/doctest.html>`_ and ``unittests`` for running unittests and measuring coverage, using
``pytest`` and the ``pytest-cov`` plugin:

.. code:: bash

   make lint
   make doctests
   make unittests

Linting warnings should be addressed first. The doctests serve as acceptance tests, and should be run first, before the unit tests.

.. _contributing.documentation:

Documentation
=============

`Project documentation <https://continuedfractions.readthedocs.io/en/latest/>`_ is defined and built using `Sphinx <https://www.sphinx-doc.org/en/master/>`_, and deployed to `Read The Docs <https://readthedocs.org>`_. Currently, the building and deployment steps for documentation are not automated in a CI pipeline, but are done manually - this will be addressed in future releases.

The Sphinx documentation can be built locally on any branch from the **project root** using:

.. code:: bash

   make -C docs "html"

First, ensure that you have installed the docs Python requirements, which include all development dependencies, either via :program:`pip`:

.. code:: bash

   pip install -r docs/requirements.txt

or via `PDM <https://github.com/sr-murthy/continuedfractions/blob/main/docs/requirements.txt>`_:

.. code:: bash

   pdm install -v --dev --no-editable --no-self

.. _contributing.ci-cd:

Continuous Integration and Deployment (CI/CD)
=============================================

The CI/CD pipelines are defined in the `CI YML <.github/workflows/ci.yml>`_, and pipelines for all branches include a tests stage, consisting of Ruff linting, Python doctests, and unit tests, in that order. This will be amended in the future to ensure that tests are only run on updates to PRs targeting ``main``, to avoid duplication on ``main``.

.. _contributing.versioning-and-releases:

Versioning and Releases
=======================

The `PyPI package <https://pypi.org/project/continuedfractions/>`_ is currently at version ``0.11.21`` - `semantic versioning <https://semver.org/>`_ is used.

There is currently no dedicated pipeline for releases - both `GitHub releases <https://github.com/sr-murthy/continuedfractions/releases>`_ and `PyPI packages <https://pypi.org/project/continuedfractions>`_ are published manually, but both have the same version tag.

Pipelines for releases (and also documentation) will be added as part of a future release.
