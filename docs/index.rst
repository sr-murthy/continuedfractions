.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

==================
continuedfractions
==================

A simple extension of the Python :py:class:`fractions.Fraction` standard library class for working with (finite, simple) `continued fractions <https://en.wikipedia.org/wiki/Continued_fraction>`_ as Python objects.

The package is aimed at users interested in:

- working with (finite, simple) continued fractions as Python objects, in an intuitive object-oriented way
- making stateful computations involving key properties such as elements/coefficients, convergents, semiconvergents, remainders, and others
- operating on them as rationals and instances of the :py:class:`fractions.Fraction` standard library class
- testing approximations of irrational numbers
- exploring other related objects such as rational points in the plane, enumerations of rational numbers, mediants, and special sequences of rational numbers such as Farey sequences

Installation
------------

Install from `PyPI <https://pypi.org/project/continuedfractions/>`__:

.. code:: shell

   pip install -U continuedfractions

or the ``main`` branch of the repo:

.. code:: shell

   pip install -U git+https://github.com/sr-murthy/continuedfractions

Only standard libraries used, and there are no 3rd party dependencies.

In terms of Python versions, any version from 3.10+ should be fine on any platform (Linux, MacOS, Windows etc.). Earlier Python versions may not work because of some aspects of type hinting.

.. note::

   All graphs in the documentation are generated using `Graphviz <https://graphviz.org/>`_ (`DOT language <https://graphviz.org/doc/info/lang.html>`_) and the `edotor <https://edotor.net/>`_ graphical editor. The graph source files (:program:`.dot`) can be viewed `here <https://github.com/sr-murthy/continuedfractions/tree/main/docs/_static>`_.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sources/continued-fractions
   sources/rational-points
   sources/sequences
   sources/contributing
   sources/api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
