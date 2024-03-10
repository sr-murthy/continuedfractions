============================
Creating Continued Fractions
============================

Import the core class ``ContinuedFraction`` from ``continuedfractions.continuedfraction``.

.. code:: python

   >>> from continuedfractions.continuedfraction import ContinuedFraction

.. _creating-continued-fractions.from-numbers:

From Numbers
============

As a starting point, we can take the `rational number <https://en.wikipedia.org/wiki/Rational_number>`_ :math:`\frac{649}{200} = \frac{3 \times 200 + 49}{200} = 3.245` which
has the continued fraction representation:

.. math::

   \frac{649}{200} = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}

This representation is called **simple** because all of the numerators in the fractional terms are equal to :math:`1`, which makes the fractions irreducible. Mathematically, the continued fraction is written as :math:`[3; 4, 12, 4]`.

The continued fraction object for :math:`\frac{649}{200}` can be created as follows.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf
   ContinuedFraction(649, 200)

**Note**: The same object can also be constructed using ``ContinuedFraction('649/200')``, ``ContinuedFraction('3.245')``, ``ContinuedFraction(Fraction(649, 200))``, ``ContinuedFraction(Fraction(649), 200))``, ``ContinuedFraction(649, Fraction(200)))``, and ``ContinuedFraction(Decimal('3.245'))``. But passing a numeric literal such as ``649/200`` will result in an evaluation of the decimal integer division using `binary floating point division <https://docs.python.org/3/tutorial/floatingpoint.html>`_,
thus producing a fractional approximation, in this case, ``ContinuedFraction(3653545197704315, 1125899906842624)``.

The float value of ``ContinuedFraction(649, 200)`` is available via the ``.as_float()`` method, in this case, an exact value of :math:`3.245`.

.. code:: python

   >>> cf.as_float()
   3.245

**Note**: the ``.as_float()`` is unique to ``ContinuedFraction`` - it is not defined in the superclass, ``fractions.Fraction``.

Every finite continued fraction represents a rational number, and conversely every rational number can be represented as a finite continued fraction. On the other hand, infinite continued fractions can only represent `irrational numbers <https://en.wikipedia.org/wiki/Irrational_number>`_.

There are infinitely many rational and irrational numbers that cannot be represented exactly as binary fractions, and, therefore, also, as Python ``fractions.Fraction`` or ``float`` objects. In the current implementation of ``continuedfractions`` the ``fractions.Fraction`` class is the key type involved in creating continued fractions representations. This means that for infinitely many real numbers the package will only produce (finite) approximate representations.

An example is given below for the irrational :math:`\sqrt{2}`, which is given by the infinite periodic continued fraction :math:`[1; 2, 2, 2, \ldots]`:

.. code:: python

   >>> sqrt2 = ContinuedFraction(math.sqrt(2))
   >>> sqrt2
   ContinuedFraction(6369051672525773, 4503599627370496)
   >>> sqrt2.as_float()
   1.4142135623730951

This limitation on exactness and length of continued fraction representations will be addressed in future versions.

.. _creating-continued-fractions.from-elements:

From Elements
=============

Continued fractions can also be constructed from sequences of elements, using the ``ContinuedFraction.from_elements()`` class method.

.. code:: python

   >>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
   >>> cf_inverse
   ContinuedFraction(200, 649)
   >>> cf_inverse.elements
   (0, 3, 4, 12, 4)
   >>> assert cf_inverse == 1/cf
   # True
   >>> assert cf * cf_inverse == 1
   # True
   >>> cf_negative_inverse = ContinuedFraction.from_elements(-1, 1, 2, 4, 12, 4)
   >>> cf_negative_inverse
   ContinuedFraction(-200, 649)
   >>> cf_negative_inverse.elements
   (-1, 1, 2, 4, 12, 4)
   >>> assert cf_negative_inverse == -1/cf
   # True
   >>> assert cf * cf_negative_inverse == -1
   >>> assert cf + (-cf) == cf_inverse + cf_negative_inverse == 0
   # True

.. _creating-continued-fractions.validation:

Validation
==========

The ``ContinuedFraction`` class validates all inputs during object creation - in the ``.__new__()`` class method, not instance
initialisation - using the ``.validate()`` class method. Inputs that do not meet the following conditions trigger a ``ValueError``.

-  a single integer or a non-nan float
-  a single numeric string
-  a single ``fractions.Fraction`` or ``decimal.Decimal`` object
-  two integers or ``fractions.Fraction`` objects, or a combination of
   an integer and a ``fractions.Fraction`` object, representing the
   numerator and non-zero denominator of a rational number

A number of examples are given below of validation passes and fails.

.. code:: python

   >>> ContinuedFraction.validate(100)
   >>> ContinuedFraction.validate(3, -2)

   >>> ContinuedFraction.validate(1, -2.0)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `decimal.Decimal` objects; or two 
   integers or two `fractions.Fraction` objects or a pairwise 
   combination of these, representing the numerator and non-zero 
   denominator, respectively, of a rational fraction, are valid.

   >>> ContinuedFraction.validate(-.123456789)
   >>> ContinuedFraction.validate('-.123456789')
   >>> ContinuedFraction.validate('-649/200')
   >>> ContinuedFraction.validate(-3/2)

   >>> ContinuedFraction.validate(-3, 0)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `decimal.Decimal` objects; or two 
   integers or two `fractions.Fraction` objects or a pairwise 
   combination of these, representing the numerator and non-zero 
   denominator, respectively, of a rational fraction, are valid.

   >>> ContinuedFraction.validate(Fraction(-415, 93))
   >>> ContinuedFraction.validate(Decimal('12345.6789'))
   >>> ContinuedFraction.validate(Decimal(12345.6789))

   >>> ContinuedFraction.validate(Fraction(3, 2), 2.5)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `decimal.Decimal` objects; or two 
   integers or two `fractions.Fraction` objects or a pairwise 
   combination of these, representing the numerator and non-zero 
   denominator, respectively, of a rational fraction, are valid.

.. _creating-continued-fractions.negative-continued-fractions:

“Negative” Continued Fractions
------------------------------

Continued fractions representations with negative terms are valid, provided we use the `Euclidean integer division algorithm <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_ to calculate the successive quotients and remainders in each step. For example, :math:`\frac{-415}{93} = \frac{-5 \times 93 + 50}{93}` has the continued fraction representation :math:`[-5; 1, 1, 6, 7]`:

.. math::

   -\frac{415}{93} = -5 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{6 + \cfrac{1}{7}}}}

Compare this with :math:`[4; 2, 6, 7]`, which is the continued fraction representation of :math:`\frac{415}{93} = \frac{4 \times 93 + 43}{93}`:

.. math::

   \frac{415}{93} = 4 + \cfrac{1}{2 + \cfrac{1}{6 + \cfrac{1}{7}}}

``ContinuedFraction`` objects for negative numbers are constructed in the same way as with positive numbers, subject to the validation rules described above. And to avoid zero division problems if a fraction has a negative denominator the minus sign is “transferred” to the numerator. A few examples are given below.

.. code:: python

   >>> ContinuedFraction('-3.245')
   ContinuedFraction(-415, 93)
   >>> ContinuedFraction(-415, 93)
   ContinuedFraction(-415, 93)
   >>> -ContinuedFraction(415, 93)
   ContinuedFraction(-415, 93)
   >>> ContinuedFraction(-415, 93).elements
   (-5, 1, 1, 6, 7)
   >>> ContinuedFraction(-415, 93).convergents 
   mappingproxy({0: Fraction(-5, 1), 1: Fraction(-4, 1), 2: Fraction(-9, 2), 3: Fraction(-58, 13), 4: Fraction(-415, 93)})
   >>> ContinuedFraction(-415, 93).as_float()
   -4.462365591397849
   >>> ContinuedFraction(415, 93).as_float()
   4.462365591397849

**Note** As negation of numbers is a unary operation, the minus sign in a “negative” ``ContinuedFraction`` object must be attached to the fraction, before enclosure in parentheses.

.. code:: python

   >>> -ContinuedFraction(415, 93).elements
   ...
   TypeError: bad operand type for unary -: 'tuple'
   >>> -(ContinuedFraction(415, 93)).elements
   ...
   TypeError: bad operand type for unary -: 'tuple'
   >>> (-ContinuedFraction(415, 93)).elements
   (-5, 1, 1, 6, 7)
   >>> assert ContinuedFraction(415, 93) + (-ContinuedFraction(415, 93)) == 0
   # True

.. _creating-continued-fractions.references:

References
----------

[1] Baker, Alan. A concise introduction to the theory of numbers. Cambridge: Cambridge Univ. Pr., 2002.

[2] Barrow, John D. “Chaos in Numberland: The secret life of continued fractions.” plus.maths.org, 1 June 2000,
https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractionsURL.

[3] Emory University Math Center. “Continued Fractions.” The Department of Mathematics and Computer Science, https://mathcenter.oxford.emory.edu/site/math125/continuedFractions/. Accessed 19 Feb 2024.

[4] Wikipedia. “Mediant (mathematics)”. https://en.wikipedia.org/wiki/Mediant_(mathematics). Accessed 23 February 2024.

[5] Python 3.12.2 Docs. “Floating Point Arithmetic: Issues and Limitations.” https://docs.python.org/3/tutorial/floatingpoint.html. Accessed 20 February 2024.

[6] Python 3.12.2 Docs. “fractions - Rational numbers.” https://docs.python.org/3/library/fractions.html. Accessed 21 February
2024.

[7] Python 3.12.2 Docs. “decimal - Decimal fixed point and floating point arithmetic.” https://docs.python.org/3/library/decimal.html. Accessed 21 February 2024.

[8] Wikipedia. “Continued Fraction”. https://en.wikipedia.org/wiki/Continued_fraction. Accessed 19 February 2024.

[9] Wikipedia. “Stern-Brocot Tree”. https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree. Accessed 23 February 2024.