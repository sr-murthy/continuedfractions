.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

==================
continuedfractions
==================

A simple extension of the Python :py:class:`fractions.Fraction` standard library class for working with (finite, simple) `continued fractions <https://en.wikipedia.org/wiki/Continued_fraction>`_ as Python objects.

The package is designed for users interested in:

- learning about and working with (finite, simple) continued fractions as Python objects, in an intuitive object-oriented way
- to allow stateful computations involving key properties such as elements/coefficients, convergents, semiconvergents, remainders, and others
- operating on them as rationals and instances of the :py:class:`fractions.Fraction` standard library class
- making approximations of and experimental computations for irrational numbers
- exploring other related objects such as enumerations of rational numbers, mediants, and special sequences of rational numbers such as Farey sequences

Installation
------------

Install from `PyPI <https://pypi.org/project/continuedfractions/>`__:

.. code:: shell

   pip install -U continuedfractions

or the ``main`` branch of the repo:

.. code:: shell

   pip install -U git+https://github.com/sr-murthy/continuedfractions

Only standard libraries used, so there are no dependencies.

For the source use the :doc:`API reference <sources/api-reference>`. Or if you're interested in contributing you can start with the :doc:`contributions guide <sources/contributing>`.

.. note::

   All graphs in the documentation are generated using `Graphviz <https://graphviz.org/>`_ (`DOT language <https://graphviz.org/doc/info/lang.html>`_) and the `edotor <https://edotor.net/>`_ graphical editor. The graph source files (:program:`.dot`) can be viewed `here <https://github.com/sr-murthy/continuedfractions/tree/main/docs/_static>`_.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/continued-fractions
   sources/sequences
   sources/contributing
   sources/api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
