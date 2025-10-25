.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

============
Contributing
============

Contributors and contributions are welcome. Please read these guidelines first.

.. _contributing.git:

Git :fab:`github`
=================

The project homepage is on `GitHub <https://github.com/sr-murthy/continuedfractions>`_.

Contributors can open pull requests from a fork targeting the parent ``main`` `branch <https://github.com/sr-murthy/continuedfractions/tree/main>`_. But it may be a good first step to create an `issue <https://github.com/sr-murthy/continuedfractions/issues>`_ or open a `discussion topic <https://github.com/sr-murthy/continuedfractions/discussions>`_.

.. _contributing.repo:

Repo :fas:`folder`
==================

You will need to clone the repository first. As there are no dependencies there isn't much to set up, so this should be pretty simple. The minimum recommended version of Python is 3.10 as some of the type hinting may be incompatible with earlier versions.

.. _contributing.dependencies-and-pdm:

Dependencies :fas:`cubes`
=========================

Only standard libraries are used. See the `project TOML <https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml>`_ for more information.

Development dependencies are specified in the ``[tool.pdm.dev-dependencies]`` section of the TOML but these are purely indicative.

`PDM <https://pdm-project.org/latest>`_ is used to manage all dependencies. It is also used to automate certain tasks, such as running tests, as described in the section.

There are no root-level ``requirements*.txt`` files - but only a single (default, version-controlled, cross-platform) `pdm.lock <https://github.com/sr-murthy/continuedfractions/blob/main/pdm.lock>`_ lockfile. The lockfile is used with PDM to install all development dependencies, including the project itself, in editable mode where available:

.. code:: shell

   pdm install -v --dev

.. note::

   The :command:`pdm install` command uses either the default lockfile (:file:`pdm.lock`), or one specified with :command:`-L <lockfile>`. Multiple lockfiles can be generated and maintained. Refer to the `PDM install documentation <https://pdm-project.org/latest/reference/cli/#install>`_ for more information.

If you don't wish to install any editable dependencies, including the project itself, you can use:

.. code:: shell

   pdm install -v --dev --no-editable --no-self

The default lockfile can be updated with any and all upstream changes in the TOML-defined dependencies, but excluding any editable dependencies including the project itself, using:

.. code:: shell

   pdm update -v --dev --no-editable --no-self --update-all

This will usually modify :file:`pdm.lock`, in which case the file should be staged and included in a commit.

The lockfile can be exported in its entirety to another format, such as :file:`docs/requirements.txt` using:

.. code:: shell

   pdm export -v -f requirements --dev -o docs/requirements.txt

For more information on PDM lockfiles and installing requirements see the `PDM documentation <https://pdm-project.org/latest/>`_.

.. _contributing.tests:

Tests :fas:`microscope`
=======================

Tests are defined in the :file:`tests` folder and can be run directly or via the `Makefile <https://github.com/sr-murthy/continuedfractions/blob/main/Makefile>`_, e.g. ``make unitests`` will run the unit tests. Linting can be performed with ``make lint``, which requires `ruff <https://docs.astral.sh/ruff/>`_ (specified in the dev. dependencies in the TOML). The doctests can be run with ``make doctests``.

.. _contributing.documentation:

Documentation :fas:`book`
=========================

`Project documentation <https://continuedfractions.readthedocs.io/en/latest/>`_ is written and built using `Sphinx <https://www.sphinx-doc.org/en/master/>`_, and deployed to `Read The Docs <https://readthedocs.org>`_.

The Sphinx documentation source pages and assets are contained in the :file:`docs/` subfolder. The HTML pages can be built locally on any branch (from the project root) using:

.. code:: shell

   make -C docs html

The pages will be built inside :file:`docs/_build/html`, with the index/home page being :file:`docs/_build/html/index.html`.

In order for this to work first ensure that you have installed the documentation Python requirements listed in :file:`docs/requirements.txt`. This can be done either via :program:`pip`:

.. code:: shell

   pip install -r docs/requirements.txt

or via `PDM <https://pdm.fming.dev/latest/>`_:

.. code:: shell

   pdm install -v --dev --no-editable --no-self

.. _contributing.ci:

CI :fas:`circle-play`
=====================

The main CI workflows are defined in the `CI YML <https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/ci.yml>`_ and the `CodeQL Analysis YML <https://github.com/sr-murthy/continuedfractions/blob/main/.github/workflows/codeql-analysis.yml>`_. 

.. _contributing.versioning-and-releases:

Versioning and Releases :fas:`upload`
=====================================

The latest release is ``1.9.0``, and releases are created, tagged and published manually, not via a workflow.
