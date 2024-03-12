==================
continuedfractions
==================

A simple extension of the Python `fractions <https://docs.python.org/3/library/fractions.html>`_ standard library for working with `continued fractions <https://en.wikipedia.org/wiki/Continued_fraction>`_ as Python objects.

The ``continuedfractions`` package is designed to:

-  make it easy to construct continued fractions as Python objects
-  explore their key properties, such as elements/coefficients,
   convergents, segments, remainders
-  operate on them as rationals and instances of the standard library
   `fractions.Fraction <https://docs.python.org/3/library/fractions.html#fractions.Fraction>`_
   class

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
   >>> cf.as_float()
   3.141592653589793
   >>> cf.convergents
   mappingproxy({0: Fraction(3, 1), 1: Fraction(22, 7), 2: Fraction(333, 106), 3: Fraction(355, 113), 4: Fraction(103993, 33102), 5: Fraction(104348, 33215), 6: Fraction(208341, 66317), 7: Fraction(312689, 99532), 8: Fraction(833719, 265381), 9: Fraction(1146408, 364913), 10: Fraction(4272943, 1360120), 11: Fraction(5419351, 1725033), 12: Fraction(80143857, 25510582), 13: Fraction(325994779, 103767361), 14: Fraction(732133415, 233045304), 15: Fraction(2522395024, 802903273), 16: Fraction(3254528439, 1035948577), 17: Fraction(41576736292, 13234286197), 18: Fraction(211138209899, 67207379562), 19: Fraction(252714946191, 80441665759), 20: Fraction(1474712940854, 469415708357), 21: Fraction(29746973763271, 9468755832899), 22: Fraction(31221686704125, 9938171541256), 23: Fraction(373185527508646, 118788642786715), 24: Fraction(404407214212771, 128726814327971), 25: Fraction(777592741721417, 247515457114686), 26: Fraction(1181999955934188, 376242271442657), 27: Fraction(3141592653589793, 1000000000000000)})
   >>> cf.order
   27
   >>> pi_approx = ContinuedFraction.from_elements(3, 7, 15, 1)
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
   sources/mediants
   sources/contributing
   sources/api-reference

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
