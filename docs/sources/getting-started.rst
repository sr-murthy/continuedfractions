===============
Getting Started
===============

The package uses only Python standard libraries, and is supported on Python versions ``3.10``-``3.12``. It is CI-tested on Ubuntu Linux (22.04.3 LTS), Mac OS (12.7.3) and Windows (Windows Server 2022), but should also install on any other platform supporting these Python versions.

.. _getting-started.installation:

Installation
============

The simplest way of installing it is a standard ``pip``/``pip3`` install:

.. code:: python

   pip install continuedfractions

For contributors there are development requirements which are specified in the `project TOML <https://github.com/sr-murthy/continuedfractions/blob/main/pyproject.toml>`_ - contribution guidelines will be described in more detail later.

The ``continuedfractions`` package consists of two core libraries.

-  `continuedfractions.lib <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/lib.py>`_
-  `continuedfractions.continuedfraction <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/continuedfraction.py>`_

.. _getting-started.package-structure:

Package Structure
=================

.. _getting-started.package-structure.continuedfractions_lib:

``continuedfractions.lib``
++++++++++++++++++++++++++

This is a `library <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/lib.py>`_ of standalone functions, which are summarised below.

-  ``continued_fraction_rational`` - generates the (ordered) sequence of elements (coefficients) of a finite, simple continued fraction representation of a given rational number, given as a ``fractions.Fraction`` object. The representation will be unique if the given number is a rational number with an exact binary fractional representation, otherwise it will be approximate.
-  ``continued_fraction_real`` - generates the sequence of elements of a finite, simple, continued fraction representation of a real number, given as a single ``int``, ``float``, ``fractions.Fraction``, ``decimal.Decimal`` object, or a pair of ``ints`` and/or ``fractions.Fraction`` objects representing the numerator and non-zero denominator, respectively, of the number. The resulting continued fraction representation will be exact for any rational number and which has an exact representation as a binary fraction, otherwise, it will only be approximate. The latter limitation will be addressed in future versions.
-  ``convergent`` - returns the ``k``-th convergent (for a positive integer `k`) of a continued fraction representation of a number, from a sequence of its elements; the convergent is returned as a``fractions.Fraction`` object
-  ``mediant`` - returns the ``k``-th left or right mediant of two rational numbers, given as ``fractions.Fraction`` objects

.. _getting-started.package-structure.continuedfractions_continuedfraction:

``continuedfractions.continuedfraction``
++++++++++++++++++++++++++++++++++++++++

This is a `library <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/continuedfraction.py>`_ containing a single main class, ``ContinuedFraction``, which subclasses ``fractions.Fraction``, and is designed to represented continued fractions as Python objects which are fully operable as rational numbers.
