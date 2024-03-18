===============
Getting Started
===============

This is a `PyPI package <https://pypi.org/project/continuedfractions/>`_ which uses only Python standard libraries, and is supported on any **Linux**, **Mac OS** or **Windows** system supporting **Python 3.10**, **3.11**, or **3.12**. It is CI-tested on **Ubuntu Linux** (22.04.3 LTS), **Mac OS** (12.7.3) and **Windows** (Windows Server 2022), but should also install on any other platform supporting these Python versions.

.. _getting-started.installation:

Installation
============

The simplest way of installing it is a standard ``pip``/``pip3`` install:

.. code:: python

   pip install continuedfractions

For contributors there are development requirements which are specified in the `project TOML <https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml>`_ - contribution guidelines will be described in more detail later.

The ``continuedfractions`` package consists of two core libraries.

-  :py:mod:`continuedfractions.lib`
-  :py:mod:`continuedfractions.continuedfraction`

.. _getting-started.package-structure:

Package Structure
=================

.. _getting-started.package-structure.continuedfractions_lib:

``continuedfractions.lib``
++++++++++++++++++++++++++

This is a library of standalone functions, which are summarised below.

-  :py:meth:`~continuedfractions.lib.continued_fraction_rational` - generates the (ordered) sequence of elements (coefficients) of a unique, finite, simple continued fraction of a given rational number, given as a :py:class:`fractions.Fraction` object.
-  :py:meth:`~continuedfractions.lib.continued_fraction_real` - generates the sequence of elements of a simple continued fraction of a real number, given as a single :py:class:`int`, :py:class:`float`, :py:class:`fractions.Fraction`, :py:class:`decimal.Decimal` object, or an :py:class:`int` pair and/or :py:class:`fractions.Fraction` pair, representing the numerator and non-zero denominator, respectively, of the number.
- :py:meth:`~continuedfractions.lib.fraction_from_elements` - returns a :py:class:`fractions.Fraction` object given a sequence of elements of a (finite) simple continued fraction.
-  :py:meth:`~continuedfractions.lib.convergent` - returns the ``k``-th convergent (for a positive integer :math:`k`) from a sequence of elements of a (finite) simple continued fraction; the convergent is returned as a :py:class:`fractions.Fraction` object.
-  :py:meth:`~continuedfractions.lib.mediant` - returns the ``k``-th left or right mediant of two rational numbers, given as :py:class:`fractions.Fraction` objects; the mediant is returned as a :py:class:`fractions.Fraction` object.

.. _getting-started.package-structure.continuedfractions_continuedfraction:

``continuedfractions.continuedfraction``
++++++++++++++++++++++++++++++++++++++++

This is a library containing a single main class:

- :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` - a subclass of :py:class:`fractions.Fraction`, designed to represented (finite) simple continued fractions as Python objects, which are fully operable as rational numbers.
