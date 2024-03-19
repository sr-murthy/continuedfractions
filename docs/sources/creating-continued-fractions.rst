============================
Creating Continued Fractions
============================

It's useful to start with the basic mathematics of continued fractions, using a simple example.

.. _creating-continued-fractions.basic-math:

The Basic Math
==============

Consider the `rational number <https://en.wikipedia.org/wiki/Rational_number>`_ :math:`\frac{649}{200} = \frac{3 \times 200 + 49}{200} = 3.245` which has a continued fraction representation, or simply, a continued fraction, given by:

.. math::

   \frac{649}{200} = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}

This is derived by repeatedly applying `Euclid's division lemma <https://en.wikipedia.org/wiki/Euclidean_division#Division_theorem>`_, as described below:

.. math::

   \begin{align}
   \frac{649}{200} &= 3 + \cfrac{49}{200} \\
                   &= 3 + \cfrac{1}{\cfrac{200}{49}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{4}{49}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{1}{\cfrac{49}{4}}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}
   \end{align}

The numbers :math:`3, 4, 12, 4` are called **elements** (or **coefficients**) of the continued fraction :math:`[3; 4, 12, 4]`, and the number of elements after the first - in this case :math:`3` - is defined to be its **order**.

The representation :math:`[3; 4, 12, 4]` is called **simple** (or **regular**) because all of the numerators in the fractional terms are equal to :math:`1`, which makes the fractions irreducible (cannot be simplified further). Mathematically, the continued fraction is written as :math:`[3; 4, 12, 4]`. The representation is also unique - the only other representation is :math:`[3; 4, 12, 3, 1]`, which can be rewritten as :math:`[3; 4, 12, 4]`.

.. note::

   All references to continued fractions are to the simple, unique variants, where the last element :math:`> 1`.

   Support for non-simple (irregular/generalised) continued fractions is planned to be included in a future release.

We can think of :math:`3`, which is the integer part of :math:`\frac{649}{200} = 3.245`, as the "head" of the continued fraction, and the integers :math:`4, 12, 4`, which determine the fractional part :math:`\cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{49}{200} = 0.245` of the continued fraction, as its "tail".

.. _creating-continued-fractions.from-numeric-types:

Creating Continued Fractions from Numeric Types
===============================================

Import the core class :py:class:`continuedfractions.continuedfraction.ContinuedFraction`.

.. code:: python

   >>> from continuedfractions.continuedfraction import ContinuedFraction

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object for :math:`\frac{649}{200}` can be created as follows.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf
   ContinuedFraction(649, 200)

.. note::

   The same object can also be constructed using ``ContinuedFraction('649/200')``, ``ContinuedFraction('3.245')``, ``ContinuedFraction(Fraction(649, 200))``, ``ContinuedFraction(Fraction(649), 200))``, ``ContinuedFraction(649, Fraction(200)))``, and ``ContinuedFraction(Decimal('3.245'))``, and even ``ContinuedFraction(ContinuedFraction(649, 200))`` .

   But passing a numeric literal such as ``649/200`` will result in an evaluation of the decimal integer division using `binary floating point division <https://docs.python.org/3/tutorial/floatingpoint.html>`_, thus producing a fractional approximation, in this case, ``ContinuedFraction(3653545197704315, 1125899906842624)``.

The float value of ``ContinuedFraction(649, 200)`` is available via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.as_float()` method, in this case, a value of :math:`3.245`.

.. code:: python

   >>> cf.as_float()
   3.245

A :py:class:`decimal.Decimal` value of ``ContinuedFraction(649, 200)`` is also available via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.as_decimal()` method.

.. code:: python

   >>> cf.as_decimal()
   Decimal('3.245')

Every finite continued fraction represents a rational number, as a finite continued fraction is a "nested" sum of rational numbers. Conversely, every rational number can be represented as a finite (and simple) continued fraction, by an iterative procedure using `Euclidean division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_. On the other hand, infinite continued fractions represent `irrational numbers <https://en.wikipedia.org/wiki/Irrational_number>`_ and conversely every infinite continued fraction represents an irrational number.

There are infinitely many rational and irrational numbers that cannot be represented exactly as binary fractions, which form the basis for `floating point arithmetic <https://docs.python.org/3/tutorial/floatingpoint.html>`_, and, therefore, also, cannot be represented exactly as Python :py:class:`float` objects. To deal with this, the package processes rational numbers using the :py:class:`fractions.Fraction` class, which allows for exact continued fractions for any rational number, limited only by the available memory and/or capacity of the running environment.

Continued fractions for irrational numbers given directly as :py:class:`float` objects end up as fractional approximations, as they rely on converting :py:class:`decimal.Decimal` representations of the given :py:class:`float` object to a :py:class:`fractions.Fraction` object. However, as described in the :ref:`next section <creating-continued-fractions.from-elements>`, the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method can be used to create :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects with arbitrary sequences of elements, which can give much more accurate results.

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

Creating Continued Fractions From Elements/Coefficients
=======================================================

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

Expanding the expression for :math:`\sqrt{n}` recursively we have the following infinite periodic continued fraction for :math:`\sqrt{n}`:

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

Then we can iteratively construct more accurate :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximations of :math:`\sqrt{2}` by iteratively taking more complete sequences of the elements from the full simple representation of :math:`[1; \bar{2}]`:

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

With the first 10 elements of the complete sequence of elements of the simple continued fraction of :math:`\sqrt{2}` we have obtained an approximation that is accurate to :math:`6` decimal places in the fractional part. We'd ideally like to have as few elements as possible in our :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximation of :math:`\sqrt{2}` for a desired level of accuracy, but this partly depends on how fast the partial, finite continued fractions represented by the chosen sequences of elements in our approximations are converging to the true value of :math:`\sqrt{2}` - these partial, finite continued fractions in a given continued fraction are called :ref:`convergents <exploring-continued-fractions.convergents-and-rational-approximations>`, and will be discussed in more detail later on.

If we use the first 101 elements (the leading 1, plus a tail of 100 2s) we get more accurate results:

.. code:: python

   # Create a `ContinuedFraction` from the sequence 1, 2, 2, 2, ..., 2, with 100 2s in the tail
   >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
   ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
   >>> sqrt2_100.elements
   # -> (1, 2, 2, 2, ..., 2) where there are `100` 2s after the `1`
   >>> sqrt2_100.as_decimal()
   Decimal('1.414213562373095048801688724')

The decimal value of ``ContinuedFraction.from_elements(1, *[2] * 100)`` in this construction is now accurate up to 27 digits in the fractional part, but the decimal representation stops there. Why 27? Because the :py:mod:`decimal` library uses a default `contextual precision <https://docs.python.org/3/library/decimal.html#decimal.DefaultContext>`_ of 28 digits. This can be increased, and the accuracy compared in the longer representation, as follows:

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

Input Validation
================

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class validates all inputs during object creation - in the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.validate` class method, and not instance
initialisation. Inputs that do not meet the following conditions trigger a :py:class:`ValueError`.

   - a single ``int`` or a non-``nan`` ``float``
   - a single numeric string (``str``)
   - a single ``fractions.Fraction`` or ``ContinuedFraction`` or
     ``decimal.Decimal`` object
   - a pairwise combination of an ``int``, ``fractions.Fraction`` or
     ``ContinuedFraction`` object, representing the numerator and non-zero
     denominator of a rational fraction

A number of examples are given below of validation passes and fails.

.. code:: python

   >>> ContinuedFraction.validate(100)
   >>> ContinuedFraction.validate(3, -2)

   >>> ContinuedFraction.validate(1, -2.0)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` 
   objects; or a pairwise combination of an integer, 
   `fractions.Fraction` or ``ContinuedFraction`` object, representing 
   the numerator and non-zero denominator, respectively, of a rational 
   fraction, are valid.

   >>> ContinuedFraction.validate(-.123456789)
   >>> ContinuedFraction.validate('-.123456789')
   >>> ContinuedFraction.validate('-649/200')
   >>> ContinuedFraction.validate(-3/2)

   >>> ContinuedFraction.validate(-3, 0)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` 
   objects; or a pairwise combination of an integer, 
   `fractions.Fraction` or ``ContinuedFraction`` object, representing 
   the numerator and non-zero denominator, respectively, of a rational 
   fraction, are valid.

   >>> ContinuedFraction.validate(Fraction(-415, 93))
   >>> ContinuedFraction.validate(ContinuedFraction(649, 200), 2)
   >>> ContinuedFraction.validate(ContinuedFraction(649, 200), Fraction(1, 2))
   >>> ContinuedFraction.validate(ContinuedFraction(649, 200), ContinuedFraction(1, 2))
   >>> ContinuedFraction.validate(Decimal('12345.6789'))
   >>> ContinuedFraction.validate(Decimal(12345.6789))

   >>> ContinuedFraction.validate(Fraction(3, 2), 2.5)
   Traceback (most recent call last):
   ...
   ValueError: Only single integers, non-nan floats, numeric strings, 
   `fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` 
   objects; or a pairwise combination of an integer, 
   `fractions.Fraction` or ``ContinuedFraction`` object, representing 
   the numerator and non-zero denominator, respectively, of a rational 
   fraction, are valid.

.. _creating-continued-fractions.negative-continued-fractions:

“Negative” Continued Fractions
==============================

Continued fractions for negative numbers can be derived, provided we use `Euclidean integer division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_ to calculate the elements of the representation, by starting with the integer part of the number, and then calculating the remaining elements for the fractional part with the successive quotients and remainders obtained in each division step. For example, :math:`\frac{-415}{93} = \frac{-5 \times 93 + 50}{93}` has the (unique) simple continued fraction :math:`[-5; 1, 1, 6, 7]`:

.. math::

   -\frac{415}{93} = -5 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{6 + \cfrac{1}{7}}}}

Compare this with :math:`[4; 2, 6, 7]`, which is the simple continued fraction of :math:`\frac{415}{93} = \frac{4 \times 93 + 43}{93}`:

.. math::

   \frac{415}{93} = 4 + \cfrac{1}{2 + \cfrac{1}{6 + \cfrac{1}{7}}}

To understand the difference in the sequence of elements between a "positive" and "negative" continued fraction, more generally, we can start by applying `Euclid's division lemma <https://en.wikipedia.org/wiki/Euclidean_division#Division_theorem>`_ to a positive rational number :math:`\frac{a}{b}`, with :math:`a, b` coprime (no common divisors except :math:`1`), and :math:`[a_0;a_1,\ldots,a_n]` as the simple continued fraction of order :math:`n \geq 1` (and :math:`a_n > 1`). The lemma implies that there are unique, positive integers :math:`q, v`, with :math:`0 < v < b`, such that :math:`a = qb + v`. Then:

.. math::

   \begin{align}
   \frac{a}{b} &= q + \frac{v}{b} \\
               &= q + \frac{1}{\frac{b}{v}} \\
               &= q + \frac{1}{R_1} \\
               &= [a_0 = q; a_1, \ldots, a_n]
   \end{align}

where :math:`R_1 = [a_1; a_2, \ldots, a_n]` is the "residual", :math:`(n - 1)`-order simple continued fraction of :math:`\frac{b}{v}`, also called the :ref:`1st remainder <exploring-continued-fractions.remainders>` of the continued fraction :math:`[a_0;a_1,\ldots,a_n]` of :math:`\frac{a}{b}`.

.. note::

   For integers :math:`0 < a < b`, if :math:`\frac{b}{a} > 1` has a simple continued fraction :math:`[a_0; a_1, \ldots, a_n]` of order :math:`n`, then :math:`0 < \frac{a}{b} < 1` has an "inverted" simple continued fraction :math:`[0; a_0, a_1, \ldots, a_n]` of order :math:`n + 1`. Both are unique if :math:`a_n > 1`.

   Also, if :math:`m` is any integer then :math:`m + [a_0;a_1,\ldots, a_n] = [a_0;a_1,\ldots, a_n] + m` is a symbolic expression for  :math:`[m;] + [a_0;a_1,\ldots, a_n] = [a_0;a_1,\ldots, a_n] + [m;] = [a_0 + m;a_1,\ldots, a_n]`, where :math:`[m;]` is the continued fraction of :math:`m`.

We can write :math:`-a = -(qb + v)` as:

.. math::

   -a = -qb - v = -qb - b + b - v = -(q + 1)b + (b - v)

so that:

.. math::

   \begin{align}
   -\frac{a}{b} &= -(q + 1) + \frac{b - v}{b} \\
                &= -(q + 1) + \frac{1}{\frac{b}{b - v}} \\
                &= -(q + 1) + \frac{1}{1 + \frac{v}{b - v}} \\
                &= -(q + 1) + \frac{1}{1 + \frac{1}{\frac{b}{v} - 1}} \\
                &= -(q + 1) + \frac{1}{1 + \frac{1}{R_1 - 1}} \\
                &= [-(q + 1); 1, a_1 - 1, a_2, a_3,\ldots, a_n]
   \end{align}

where :math:`R_1 - 1 = [a_1 - 1;a_2,\ldots, a_n]` and :math:`\frac{1}{R_1 - 1} = [0; a_1 - 1, a_2, a_3,\ldots, a_n]`.

.. note::

   If the last element :math:`a_n = 1` then :math:`[a_0; a_1, \ldots, a_n] = [a_0;a_1,\ldots,a_{n - 1} + 1]` is of order :math:`(n - 1)`. So in the representation :math:`[-(q + 1); 1, a_1 - 1, a_2, a_3,\ldots, a_n]` above for :math:`-\frac{a}{b}`, if :math:`a_1 = 2` then :math:`a_1 - 1 = 1` and the segment :math:`[-(q + 1); 1, a_1 - 1] = [-(q + 1); 1, 1] = [-(q + 1); 2]` is of order :math:`1`.

If :math:`\bar{R}_1` denotes the :ref:`1st remainder <exploring-continued-fractions.remainders>` :math:`[1; a_1 - 1, a_2, a_3,\ldots, a_n]` in the representation above for :math:`-\frac{a}{b}` then :math:`\bar{R}_1` is an :math:`n`-order, simple continued fraction. A special case is when :math:`a_1 = 1`: in this case :math:`a_0 = -1` and :math:`\bar{R}_1 = [a_2 + 1; a_3, \ldots, a_n]` is an :math:`(n - 2)`-order simple continued fraction. Note that this special case also applies when :math:`0 < a < b`.

Thus, we can say that if :math:`[a_0; a_1,\ldots, a_n]` is the :math:`n`-order simple continued fraction of a positive rational number :math:`\frac{a}{b}` then :math:`-\frac{a}{b}` has :math:`(n - 1)`- and :math:`(n + 1)`-order simple continued fractions given by:

.. math::

   -\frac{a}{b} = 
      \begin{cases}
         [-(a_0 + 1); a_2 + 1, a_3,\ldots, a_n], & a_1 = 1  \\
         [-(a_0 + 1); 1, a_1 - 1, a_2, a_3,\ldots, a_n], & a_1 > 1
      \end{cases}

As :math:`n \to \infty` then :math:`\lim_{n \to \infty} [a_0;a_1,\ldots,a_n] = [a_0;a_1,\ldots]` represents an irrational number, and the same relations hold.

We can see this in action with :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects, starting with small fractions :math:`\frac{a}{b}` where :math:`|a| < |b|`:

.. code:: python

   >>> ContinuedFraction(2, 3).elements
   (0, 1, 2)
   >>> ContinuedFraction(-2, 3).elements
   (-1, 3)
   >>> assert ContinuedFraction.from_elements(-1, 3) == ContinuedFraction(-2, 3)
   # True
   >>> ContinuedFraction(1, 2).elements
   (0, 2)
   >>> ContinuedFraction(-1, 2).elements
   (-1, 2)
   >>> assert ContinuedFraction.from_elements(-1, 2) == ContinuedFraction.from_elements(-1, 1, 1) == ContinuedFraction(-1, 2)
   # True

and now fractions :math:`\frac{a}{b}` where :math:`|a| > |b|`:

.. code:: python

   >>> ContinuedFraction(17, 10).elements
   (1, 1, 2, 3)
   >>> ContinuedFraction(-17, 10).elements
   (-2, 3, 3)
   >>> assert ContinuedFraction.from_elements(-2, 3, 3) == ContinuedFraction(-17, 10)
   # True
   >>> ContinuedFraction(10, 7).elements
   (1, 2, 3)
   >>> ContinuedFraction(-10, 7).elements
   (-2, 1, 1, 3)
   >>> assert ContinuedFraction.from_elements(-2, 1, 1, 3) == ContinuedFraction(-10, 7)
   # True

The construction (creation + initialisation) of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects via the ``__new__() -> __init__()`` step works the same way for negative numbers as with positive numbers, subject to the validation rules described above. And to avoid zero division problems if a fraction has a negative denominator the minus sign is “transferred” to the numerator. A few examples are given below.

.. code:: python

   >>> ContinuedFraction(-415, 93)
   ContinuedFraction(-415, 93)
   >>> -ContinuedFraction(415, 93)
   ContinuedFraction(-415, 93)
   >>> ContinuedFraction(-415, 93).elements
   (-5, 1, 1, 6, 7)
   >>> ContinuedFraction(-415, 93).convergents 
   mappingproxy({0: Fraction(-5, 1), 1: Fraction(-4, 1), 2: Fraction(-9, 2), 3: Fraction(-58, 13), 4: Fraction(-415, 93)})
   >>> ContinuedFraction(-415, 93).as_decimal()
   Decimal('-4.462365591397849462365591397849462365591397849462365591397849462365591397849462365591397849462365591')
   >>> ContinuedFraction(415, 93).as_decimal()
   Decimal('4.462365591397849462365591397849462365591397849462365591397849462365591397849462365591397849462365591')

.. note::

   As negation of numbers is a unary operation, the minus sign in a “negative” :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object must be attached to the fraction, before enclosure in parentheses.

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
