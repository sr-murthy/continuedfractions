.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

===============
Getting Started
===============

This is a `PyPI package <https://pypi.org/project/continuedfractions/>`_ which uses only Python standard libraries, and is supported on any **Linux**, **Mac OS** or **Windows** system supporting **Python 3.10**, **3.11**, or **3.12**. It is CI-tested on these versions of Python on **Ubuntu Linux** (22.04.4 LTS, x64), **Mac OS** (13.6.6, x64) and **Windows** (Windows Server 2022 21H2, x64 + x86), but should generally install on any other platform supporting these Python versions.

.. _getting-started.installation:

Installation
============

A standard ``pip`` install is sufficient:

.. code:: python

   pip install continuedfractions

If you are interested in contributing please start with the :doc:`contributions guidelines <contributing>`.

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
--------------------------

This is a library of standalone functions for (finite, simple) continued fractions.

-  :py:meth:`~continuedfractions.lib.continued_fraction_rational` - generates a unique sequence of elements (coefficients) of the continued fraction of a rational number given as a :py:class:`fractions.Fraction` instance.
-  :py:meth:`~continuedfractions.lib.continued_fraction_real` - generates a finite sequence of elements of a continued fraction of a real number given as a single :py:class:`int`, :py:class:`float`, :py:class:`str`, or :py:class:`decimal.Decimal` value; the results for :py:class:`float` inputs may be approximate and not necessarily unique.
- :py:meth:`~continuedfractions.lib.fraction_from_elements` - returns a :py:class:`fractions.Fraction` instance of the rational number represented by a continued fraction from a sequence of its elements.
-  :py:meth:`~continuedfractions.lib.convergent` - returns the :math:`k`-th convergent of a continued fraction from a sequence of elements as a :py:class:`fractions.Fraction` instance.
- :py:meth:`~continuedfractions.lib.convergents` - generates a sequence of all convergents of a continued fraction from a sequence of its elements.
-  :py:meth:`~continuedfractions.lib.remainder` - returns the :math:`k`-th remainder of a continued fraction from a sequence of elements as a :py:class:`fractions.Fraction` instance.
-  :py:meth:`~continuedfractions.lib.mediant` - returns the :math:`k`-th left or right mediant of two rational numbers, given as :py:class:`fractions.Fraction` values; the mediant is returned as a :py:class:`fractions.Fraction` instance.

.. note::

   There are also two "wrapper" functions for computing left- and right-mediants - :py:func:`~continuedfractions.lib.left_mediant` and :py:func:`~continuedfractions.lib.right_mediant` - which are partial bindings of :py:func:`~continuedfractions.lib.mediant`.

.. _getting-started.package-structure.continuedfractions_continuedfraction:

``continuedfractions.continuedfraction``
----------------------------------------

This is a library containing a single main class:

- :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` - a subclass of :py:class:`fractions.Fraction`, designed to represent (finite, simple) continued fractions as Python objects, which are fully operable as rational numbers.

.. _getting-started.package-structure.continuedfractions_sequences:

``continuedfractions.sequences``
--------------------------------

This is a library of functions and classes relating to ordered sequences and structures of integers and rational numbers, such as coprime integers, coprime pair trees, and Farey sequences:

- :py:func:`~continuedfractions.sequences.coprime_integers_generator` - generates a sequence of integers `coprime <https://en.wikipedia.org/wiki/Coprime_integers>`_ (or relatively prime) to a given positive integer.
- :py:func:`~continuedfractions.sequences.coprime_integers` - wrapper of :py:func:`~continuedfractions.sequences.coprime_integers_generator` which returns tuples.
- :py:class:`~continuedfractions.sequences.KSRMTree` - an implicit/generative class implementation of the :ref:`Kanga-Saunders-Randall-Mitchell (KSRM) ternary trees <sequences.ksrm-trees>` for representing and generating pairs of (positive) coprime integers.
- :py:func:`~continuedfractions.sequences.coprime_pairs_generator` - generates a sequence of all pairs of (positive) coprime integers less than or equal to a given positive integer. Uses the KSRM tree :py:meth:`~continuedfractions.sequences.KSRMTree.search` method to perform the search.
- :py:func:`~continuedfractions.sequences.coprime_pairs` - wrapper of :py:func:`~continuedfractions.sequences.coprime_pairs_generator` which returns tuples.
- :py:func:`~continuedfractions.sequences.farey_sequence_generator` - generates a sequence of rational numbers called a `Farey sequence <https://en.wikipedia.org/wiki/Farey_sequence>`_ for a given positive integer. Uses the :py:func:`~continuedfractions.sequences.coprime_integers` and :py:func:`~continuedfractions.sequences.coprime_pairs` functions.
- :py:func:`~continuedfractions.sequences.farey_sequence` - wrapper of :py:func:`~continuedfractions.sequences.farey_sequence_generator` which returns tuples
