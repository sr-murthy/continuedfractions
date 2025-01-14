.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

==================
continuedfractions
==================

A simple extension of the Python :py:mod:`fractions` standard library for working with (finite, simple) `continued fractions <https://en.wikipedia.org/wiki/Continued_fraction>`_ as Python objects.

The package is designed for users interested in:

- learning about and working with (finite, simple) continued fractions as Python objects, in an intuitive object-oriented way
- exploring their key properties, such as elements/coefficients, convergents, semiconvergents, remainders, and others
- operating on them as rationals and instances of the standard library :py:class:`fractions.Fraction` class
- making approximations of and experimental computations for irrational numbers
- exploring other related objects, such as mediants, and special sequences of rational numbers such as Farey sequences

.. note::

   Currently, it does **not** support the following features:

   * infinite and generalised continued fractions
   * symbolic representations of or operations with continued fractions

   Some - but not necessarily all - of these features may be considered for `future release <https://github.com/sr-murthy/continuedfractions/issues>`_.

Interested users can :doc:`start here <sources/getting-started>`, or go straight to the :doc:`API reference <sources/api-reference>`. If you're interested in contributing you can start with the :doc:`contributions guide <sources/contributing>`.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/getting-started
   sources/creating-continued-fractions
   sources/exploring-continued-fractions
   sources/sequences
   sources/contributing
   sources/api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
