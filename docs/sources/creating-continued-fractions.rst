============================
Creating Continued Fractions
============================

Import the core class :py:class:`continuedfractions.continuedfraction.ContinuedFraction`.

.. code:: python

   >>> from continuedfractions.continuedfraction import ContinuedFraction

.. _creating-continued-fractions.from-numeric-types:

From Numeric Types
==================

As a starting point, we can take the `rational number <https://en.wikipedia.org/wiki/Rational_number>`_ :math:`\frac{649}{200} = \frac{3 \times 200 + 49}{200} = 3.245` which
has a continued fraction representation:

.. math::

   \frac{649}{200} = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}

This representation is called **simple** because all of the numerators in the fractional terms are equal to :math:`1`, which makes the fractions irreducible (cannot be simplified further). Mathematically, the continued fraction is written as :math:`[3; 4, 12, 4]`.

We can think of :math:`3`, which is the integer part of :math:`\frac{649}{200} = 3.245`, as the "head" of the continued fraction, and the integers :math:`4, 12, 4`, which determine the fractional part :math:`\cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{49}{200} = 0.245` of the continued fraction, as its "tail". It is not hard to see that the integers :math:`3, 4, 12, 4` uniquely determine the continued fraction as a simple form.

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object for :math:`\frac{649}{200}` can be created as follows.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf
   ContinuedFraction(649, 200)

**Note**: The same object can also be constructed using ``ContinuedFraction('649/200')``, ``ContinuedFraction('3.245')``, ``ContinuedFraction(Fraction(649, 200))``, ``ContinuedFraction(Fraction(649), 200))``, ``ContinuedFraction(649, Fraction(200)))``, and ``ContinuedFraction(Decimal('3.245'))``. But passing a numeric literal such as ``649/200`` will result in an evaluation of the decimal integer division using `binary floating point division <https://docs.python.org/3/tutorial/floatingpoint.html>`_,
thus producing a fractional approximation, in this case, ``ContinuedFraction(3653545197704315, 1125899906842624)``.

The float value of ``ContinuedFraction(649, 200)`` is available via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.as_float()` method, in this case, a value of :math:`3.245`.

.. code:: python

   >>> cf.as_float()
   3.245

A :py:class:`decimal.Decimal` value of ``ContinuedFraction(649, 200)`` is also available via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.as_decimal()` method.

.. code:: python

   >>> cf.as_decimal()
   Decimal('3.245')

Every finite continued fraction represents a rational number, as a finite continued fraction is a "nested" sum of rational numbers. Conversely, every rational number can be represented as a finite (and simple) continued fraction, by an iterative procedure using `Euclidean division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_. On the other hand, infinite continued fractions represent `irrational numbers <https://en.wikipedia.org/wiki/Irrational_number>`_ and conversely every infinite continued fraction represents an irrational number.

There are infinitely many rational and irrational numbers that cannot be represented exactly as binary fractions, which form the basis for `floating point arithmetic <https://docs.python.org/3/tutorial/floatingpoint.html>`_, and, therefore, also, cannot be represented exactly as Python :py:class:`float` objects. To deal with this, the package processes rational numbers using the :py:class:`fractions.Fraction` class, which allows for exact continued fraction representations for any rational number, limited only by the available memory and/or capacity of the running environment.

Continued fraction representations for irrational numbers given directly as :py:class:`float` objects end up as fractional approximations, as they rely on converting :py:class:`decimal.Decimal` representations of the given :py:class:`float` object to a :py:class:`fractions.Fraction` object. However, as described in the :ref:`next section <creating-continued-fractions.from-elements>`, the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method can be used to create :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects with arbitrary sequences of elements, which can give much more accurate results.

An example is given below for the irrational :math:`\sqrt{2}`, which is given by the infinite periodic continued fraction :math:`[1; 2, 2, 2, \ldots]`. We first begin by constructing the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object for :math:`\sqrt{2}` directly from a ``math.sqrt(2)`` object:

.. code:: python

   >>> sqrt2 = ContinuedFraction(math.sqrt(2))
   >>> sqrt2
   ContinuedFraction(6369051672525773, 4503599627370496)
   >>> sqrt2.elements
   # -> (1, 2, 2, 2, 2, ... ,1, 1, 10, 2, ... ,1, 3, 1, 17, 12, 3, 2, 6, 1, 11, 2, 2)
   >>> sqrt2.as_float()
   1.4142135623730951
   >>> sqrt2.as_decimal()
   Decimal('1.4142135623730951454746218587388284504413604736328125')
   >>> Decimal(math.sqrt(2)).as_integer_ratio()
   Fraction(6369051672525773, 4503599627370496)


Here, ``ContinuedFraction(6369051672525773, 4503599627370496)`` is a fractional approximation of :math:`\sqrt{2}`, for the reasons described above, and not exact, as reflected in the tail elements of the sequence deviating from the mathematically correct value of :math:`2`. Also, note that the decimal value of ``ContinuedFraction(math.sqrt(2))`` above for :math:`\sqrt{2}` is only accurate up to :math:`15` digits in the fractional part, compared to the `first one million digit representation <https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil>`_.

However, in the :ref:`next section <creating-continued-fractions.from-elements>`, we describe a way to construct continued fractions with arbitary sequences of elements, which can produce results of any given desired level of accuracy for irrational numbers.

.. _creating-continued-fractions.from-elements:

From Elements
=============

Continued fractions can also be constructed from sequences of elements, using the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` class method.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
   >>> cf_inverse
   ContinuedFraction(200, 649)

We can verify that the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects constructed for :math:`\frac{649}{200}` and its (multiplicative) inverse :math:`\frac{200}{649}`, are as expected.

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

For rational numbers :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` will produce exactly the same results as the constructor for :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`, but with the benefit of allowing the user to specify the exact sequence of elements beforehand.

.. _creating-continued-fractions.irrationals-from-elements:

Approximating Irrationals
-------------------------

Using :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` can be very useful when trying to approximate irrational numbers with (finite) continued fractions. We know, for example, that the square root :math:`\sqrt{n}` of any non-square (positive) integer :math:`n` is irrational. This can be seen by writing :math:`n = a^2 + r`, for integers :math:`a, r > 0`, from which we have:

.. math::
   :nowrap:

   \begin{alignat*}{1}
   & r &&= n - a^2 = \left(\sqrt{n} + a\right)\left(\sqrt{n} - a\right) \\
   & \sqrt{n} &&= a + \frac{r}{a + \sqrt{n}}
   \end{alignat*}

Expanding the expression for :math:`\sqrt{n}` recursively we have the following infinite periodic continued fraction representation for :math:`\sqrt{n}`:

.. math::

   \sqrt{n} = a + \cfrac{r}{2a + \cfrac{r}{2a + \cfrac{r}{2a + \ddots}}}

With :math:`a = r = 1` we can represent :math:`\sqrt{2}` as the continued fraction:

.. math::

   \sqrt{2} = 1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{2 + \ddots}}}

written more compactly as :math:`[1; \bar{2}]`, where :math:`\bar{2}` represents an infinite sequence :math:`2, 2, 2, \ldots`.

We can start with a more precise representation of :math:`\sqrt{2}` in Python as a :py:class:`decimal.Decimal` object:

.. code:: python
   
   >>> Decimal(math.sqrt(2))
   >>> Decimal('1.4142135623730951454746218587388284504413604736328125')

Then we can iteratively construct more accurate :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximations of :math:`\sqrt{2}` by iteratively taking more complete sequences of the elements of the complete continued fraction representation :math:`[1; \bar{2}]`:

.. code:: python

   >>> ContinuedFraction.from_elements(1, 2).as_decimal()
   >>> Decimal('1.5')

   >>> ContinuedFraction.from_elements(1, 2, 2).as_decimal()
   >>> Decimal('1.4')

   >>> ContinuedFraction.from_elements(1, 2, 2, 2, 2).as_decimal()
   >>> Decimal('1.413793103448275862068965517')

   ...

   >>> ContinuedFraction.from_elements(1, 2, 2, 2, 2, 2, 2, 2, 2, 2).as_decimal()
   >>> Decimal('1.414213624894869638351555929')

   ...

With the first 10 elements of the complete sequence of elements of the continued fraction representation of :math:`\sqrt{2}` we have obtained an approximation that is accurate to :math:`6` decimal places in the fractional part. We'd ideally like to have as few elements as possible in our :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximation of :math:`\sqrt{2}` for a desired level of accuracy, but this partly depends on how fast the partial, finite continued fractions represented by the chosen sequences of elements in our approximations are converging to the true value of :math:`\sqrt{2}` - these partial, finite continued fractions in a continued fraction representation are called convergents, and will be discussed in more detail later on.

If we use the first 101 elements (the leading 1, plus a tail of 100 2s) we get more accurate results:

.. code:: python

   # Create a `ContinuedFraction` from the sequence 1, 2, 2, 2, ..., 2, with 100 2s in the tail
   >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
   ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
   >>> sqrt2_100.elements
   # -> (1, 2, 2, 2, ..., 2) where there are `100` 2s after the `1`
   >>> sqrt2_100.as_decimal()
   Decimal('1.414213562373095048801688724')

Note that the decimal value of ``ContinuedFraction.from_elements(1, *[2] * 100)`` in this construction is now accurate up to 27 digits in the fractional part, but the decimal representation stops there. Why 27? Because the :py:mod:`decimal` library uses a default `contextual precision <https://docs.python.org/3/library/decimal.html#decimal.DefaultContext>`_ of 28 digits. This can be increased, and the accuracy compared in the longer representation, as follows:

.. code:: python

    # `decimal.Decimal.getcontext().prec` stores the current context precision
    >>> import decimal
    >>> decimal.getcontext().prec
    28
    # Increase it to 100 digits, and try again
    >>> decimal.getcontext().prec = 100
    >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
    >>> sqrt2_100.as_decimal()
    Decimal('1.414213562373095048801688724209698078569671875376948073176679737990732478462093522589829309077750929')

Now, the decimal value of ``ContinuedFraction.from_elements(1, *[2] * 100)`` is accurate up to 75 digits in the fractional part, but deviates from the `true value <https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil>`_ from the 76th digit onwards.

This example also highlights the fact that "almost all" square roots of positive integers are irrational, even though the set of positive integers which are perfect squares and the set of positive integers which are not perfect squares are both countably infinite - the former is an infinitely sparser subset of the integers.

.. _creating-continued-fractions.validation:

Validation
==========

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class validates all inputs during object creation - in the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.validate` class method, and not instance
initialisation. Inputs that do not meet the following conditions trigger a :py:class:`ValueError`.

-  a single integer or a non-nan float
-  a single numeric string
-  a single :py:class:`fractions.Fraction` or :py:class:`decimal.Decimal` object
-  two integers or :py:class:`fractions.Fraction` objects, or a combination of
   an integer and a :py:class:`fractions.Fraction` object, representing the
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
==============================

Continued fractions representations for negative numbers are valid, provided we use `Euclidean integer division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_ to calculate the elements of the representation, by starting with the integer part of the number, and then calculating the remaining elements for the fractional part with the successive quotients and remainders obtained in each division step. For example, :math:`\frac{-415}{93} = \frac{-5 \times 93 + 50}{93}` has the continued fraction representation :math:`[-5; 1, 1, 6, 7]`:

.. math::

   -\frac{415}{93} = -5 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{6 + \cfrac{1}{7}}}}

Compare this with :math:`[4; 2, 6, 7]`, which is the continued fraction representation of :math:`\frac{415}{93} = \frac{4 \times 93 + 43}{93}`:

.. math::

   \frac{415}{93} = 4 + \cfrac{1}{2 + \cfrac{1}{6 + \cfrac{1}{7}}}

:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects for negative numbers are constructed in the same way as with positive numbers, subject to the validation rules described above. And to avoid zero division problems if a fraction has a negative denominator the minus sign is “transferred” to the numerator. A few examples are given below.

.. code:: python

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

**Note** As negation of numbers is a unary operation, the minus sign in a “negative” :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object must be attached to the fraction, before enclosure in parentheses.

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
==========

[1] Baker, Alan. A concise introduction to the theory of numbers. Cambridge: Cambridge Univ. Pr., 2002.

[2] Barrow, John D. “Chaos in Numberland: The secret life of continued fractions.” plus.maths.org, 1 June 2000,
https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractionsURL.

[3] Emory University Math Center. “Continued Fractions.” The Department of Mathematics and Computer Science, https://mathcenter.oxford.emory.edu/site/math125/continuedFractions/. Accessed 19 Feb 2024.

[4] Khinchin, A. Ya. Continued Fractions. Dover Publications, 1997.

[5] NASA. "The Square Root of Two to 1 Million Digits". Astronomy Picture of the Day, https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil. Accessed 13 March 2024.

[6] Python 3.12.2 Docs. “decimal - Decimal fixed point and floating point arithmetic.” https://docs.python.org/3/library/decimal.html. Accessed 21 February 2024.

[7] Python 3.12.2 Docs. “Floating Point Arithmetic: Issues and Limitations.” https://docs.python.org/3/tutorial/floatingpoint.html. Accessed 20 February 2024.

[8] Python 3.12.2 Docs. “fractions - Rational numbers.” https://docs.python.org/3/library/fractions.html. Accessed 21 February
2024.

[9] Wikipedia. “Continued Fraction”. https://en.wikipedia.org/wiki/Continued_fraction. Accessed 19 February 2024.
