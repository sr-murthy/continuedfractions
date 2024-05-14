.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

==================
continuedfractions
==================

A simple extension of the Python :py:mod:`fractions` standard library for working with `continued fractions <https://en.wikipedia.org/wiki/Continued_fraction>`_ as Python objects.

The package is designed to:

-  make it easy to construct continued fractions as Python objects
-  explore their key continued fractions properties, such as elements/coefficients,
   convergents, remainders, and other numerical properties etc.
-  operate on them fully as rational numbers and instances of the standard library
   :py:class:`fractions.Fraction` class
-  support approximations and experimental computations for irrational numbers
-  explore other objects related to continued fractions, such as mediants, sequences of coprime integers, and Farey sequences

You can :doc:`start here <sources/getting-started>`, or go straight to the :doc:`API reference <sources/api-reference>`.

Prelude
-------

.. math::

   \pi = 3 + \cfrac{1}{7 + \cfrac{1}{15 + \cfrac{1}{1 + \cfrac{1}{292 + \ddots}}}}

.. code:: python

   >>> import decimal, math; from continuedfractions.continuedfraction import ContinuedFraction
   >>> cf = ContinuedFraction(math.pi)
   >>> cf
   ContinuedFraction(884279719003555, 281474976710656)
   >>> cf.elements
   (3,7,15,1,292,1,1,1,2,1,3,1,14,4,2,3,1,12,5,1,5,20,1,11,1,1,1,2)
   >>> cf.as_decimal()
   Decimal('3.141592653589793115997963468544185161590576171875')
   >>> cf.convergent(0), cf.convergent(1), cf.convergent(2), cf.convergent(10), cf.convergent(20), cf.convergent(27)
   (ContinuedFraction(3, 1), ContinuedFraction(22, 7), ContinuedFraction(333, 106), ContinuedFraction(4272943, 1360120), ContinuedFraction(509453239292, 162164002615), ContinuedFraction(884279719003555, 281474976710656))
   >>> cf.order
   27
   >>> pi_approx = ContinuedFraction.from_elements(3, 7, 15, 1, 292)
   >>> pi_approx
   ContinuedFraction(355, 113)
   >>> pi_approx.as_float()
   3.1415929203539825
   >>> math.pi - pi_approx.as_float()
   -2.667641894049666e-07
   >>> import pytest
   >>> pytest.approx(pi_approx.as_float(), abs=1e-6) == math.pi
   True

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
