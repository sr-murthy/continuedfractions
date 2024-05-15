.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

===============
Getting Started
===============

This is a `PyPI package <https://pypi.org/project/continuedfractions/>`_ which uses only Python standard libraries, and is supported on any **Linux**, **Mac OS** or **Windows** system supporting **Python 3.10**, **3.11**, or **3.12**. It is CI-tested on **Ubuntu Linux** (22.04.4 LTS), **Mac OS** (13.6.6) and **Windows** (Windows Server 2022 21H2), but should also install on any other platform supporting these Python versions.

.. _getting-started.installation:

Installation
============

A standard ``pip`` install is sufficient:

.. code:: python

   pip install continuedfractions

Potential contributors may want look at the `project TOML <https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml>`_, and then the :doc:`contributions overview <contributing>`.

.. _getting-started.package-structure:

Package Structure
=================

The ``continuedfractions`` package consists of three core libraries.

-  :py:mod:`continuedfractions.lib`
-  :py:mod:`continuedfractions.continuedfraction`
-  :py:mod:`continuedfractions.sequences`

.. note::

   The :py:mod:`continuedfractions.utils` library contains internal utilities.

Each is summarised below. Or you can go straight to the :doc:`API reference <api-reference>`.

.. _getting-started.package-structure.continuedfractions_lib:

``continuedfractions.lib``
++++++++++++++++++++++++++

This is a library of standalone functions:

-  :py:meth:`~continuedfractions.lib.continued_fraction_rational` - generates the (ordered) sequence of elements (coefficients) of the unique simple continued fraction of a given rational number, given as a :py:class:`fractions.Fraction` instance.
-  :py:meth:`~continuedfractions.lib.continued_fraction_real` - generates the sequence of elements of a simple continued fraction of a real number, given as a single :py:class:`int`, :py:class:`float`, :py:class:`str`, or :py:class:`decimal.Decimal` value; the results for :py:class:`float` inputs may be approximate and not necessarily unique.
- :py:meth:`~continuedfractions.lib.fraction_from_elements` - returns a :py:class:`fractions.Fraction` instance of the rational number represented by a simple continued fraction with the given sequence of elements.
-  :py:meth:`~continuedfractions.lib.convergent` - returns the :math:`k`-th convergent (for a positive integer :math:`k`) from a sequence of elements of a (finite) simple continued fraction; the convergent is returned as a :py:class:`fractions.Fraction` instance.
-  :py:meth:`~continuedfractions.lib.mediant` - returns the :math:`k`-th left or right mediant of two rational numbers, given as :py:class:`fractions.Fraction` values; the mediant is returned as a :py:class:`fractions.Fraction` instance.

.. note::

   There are also two "wrapper" functions for computing left- and right-mediants - :py:func:`~continuedfractions.lib.left_mediant` and :py:func:`~continuedfractions.lib.right_mediant` - but these just call :py:func:`~continuedfractions.lib.mediant`.

.. _getting-started.package-structure.continuedfractions_continuedfraction:

``continuedfractions.continuedfraction``
++++++++++++++++++++++++++++++++++++++++

This is a library containing a single main class:

- :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` - a subclass of :py:class:`fractions.Fraction`, designed to represent (finite) simple continued fractions as Python objects, which are fully operable as rational numbers.

.. _getting-started.package-structure.continuedfractions_sequences:

``continuedfractions.sequences``
++++++++++++++++++++++++++++++++

This is a library of functions and classes relating to ordered sequences and structures of integers and rational numbers, such as (currently) coprime integers, Farey sequences and (in the future) the Stern-Brocot tree:

- :py:func:`~continuedfractions.sequences.coprime_integers` - returns a tuple of (positive) integers `coprime <https://en.wikipedia.org/wiki/Coprime_integers>`_ (or relatively prime) to a given positive integer.
- :py:class:`~continuedfractions.sequences.KSRMTree` - an implicit/generative class implementation of the Kanga-Saunders-Randall-Mitchell (KSRM) ternary trees for generating pairs of (positive) coprime integers.
- :py:func:`~continuedfractions.sequences.coprime_pairs` - returns a tuple of all pairs of (positive) coprime integers :math:`<= n`. Uses the KSRM tree :py:meth:`~continuedfractions.sequences.KSRMTree.search` method to perform the search.
- :py:func:`~continuedfractions.sequences.farey_sequence` - returns a tuple of rational numbers forming the `Farey sequence <https://en.wikipedia.org/wiki/Farey_sequence>`_ of order :math:`n`. Uses the :py:func:`~continuedfractions.sequences.coprime_integers` and :py:func:`~continuedfractions.sequences.coprime_pairs` functions.
