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

   All references to continued fractions are to the simple forms where the last element :math:`> 1`.

   Support for non-simple, generalised continued fractions is planned to be included in a future release.

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

.. _creating-continued-fractions.decimal-precision:

Decimal Precision
-----------------

The Python :py:mod:`decimal` library can, in principle, support arbitrary precision arithmetic, subject to the limitations of the running environment, system, hardware etc. It does this via `context objects <https://docs.python.org/3.12/library/decimal.html#context-objects>`_ for :py:class:`~decimal.Decimal` instances, in which you can set the precision of the :py:class:`~decimal.Decimal` values in your current environment to whatever is appropriate to your computation or experiment, subject to the limitations of your environment and/or system.

An example is given below:

.. code:: python

   # Inspect the current context
   >>> decimal.getcontext()
   Context(prec=28, rounding=ROUND_HALF_EVEN, Emin=-999999, Emax=999999, capitals=1, clamp=0, flags=[Inexact, Rounded], traps=[InvalidOperation, DivisionByZero, Overflow])
   >>> Decimal('1') / 3
   Decimal('0.3333333333333333333333333333')
   # Increase the precision to 100 digits, including the integer part of the number
   >>> decimal.getcontext().prec = 100
   >>> Decimal('1') / 3
   Decimal('0.3333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333333')

.. note::

   This doesn't necessarily work for all :py:class:`float` values, e.g. ``math.pi``, or ``math.sqrt(2)``, so be careful.

You can also set indicators that :py:class:`~decimal.Decimal` computations should be exact, and trigger signals if results are not exact and that some kind of rounding was applied - see the `Decimal FAQ <https://docs.python.org/3.12/library/decimal.html#decimal-faq>`_ for more information and examples.

.. _creating-continued-fractions.irrational-numbers:

Irrational Numbers
------------------

Every finite continued fraction represents a rational number, as a finite continued fraction is a "nested" sum of rational numbers. Conversely, every rational number can be represented as a finite (and simple) continued fraction, by an iterative procedure using `Euclidean division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_. On the other hand, infinite continued fractions represent `irrational numbers <https://en.wikipedia.org/wiki/Irrational_number>`_ and conversely every infinite continued fraction represents an irrational number.

There are infinitely many rational and irrational numbers that cannot be represented exactly as binary fractions, which form the basis for `floating point arithmetic <https://docs.python.org/3/tutorial/floatingpoint.html>`_, and, therefore, also, cannot be represented exactly as Python :py:class:`float` instances. To deal with this, the package processes rational numbers using the :py:class:`fractions.Fraction` class, which allows for exact continued fractions for any rational number, limited only by the available memory and/or capacity of the running environment.

Continued fractions for irrational numbers given directly as :py:class:`float` instances end up as fractional approximations, as they rely on converting :py:class:`decimal.Decimal` representations of the given :py:class:`float` object to a :py:class:`fractions.Fraction` object. However, as described in the :ref:`next section <creating-continued-fractions.from-elements>`, the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method can be used to create :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances with arbitrary sequences of elements, which can give much more accurate results.

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
   >>> cf_negative_inverse = ContinuedFraction.from_elements(-1, 1, 2, 4, 12, 4)
   >>> cf_negative_inverse
   ContinuedFraction(-200, 649)
   >>> cf_negative_inverse.elements
   (-1, 1, 2, 4, 12, 4)

The given sequence of elements can be arbitrarily long, subject to the limitations of the environment, system etc. Here is an example for approximating :math:`\sqrt{2}` with :math:`[1; \overbrace{2, 2,\ldots, 2]}^{1000 \text{twos}}` where the tail contains 1000 twos.

.. code:: python

   >>> decimal.getcontext().prec = 1000
   >>> ContinuedFraction.from_elements(1, *[2] * 1000).as_decimal()
   >>> Decimal('1.414213562373095048801688724209698078569671875376948073176679737990732478462107038850387534327641572735013846230912297024924836055850737212644121497099935831413222665927505592755799950501152782060571470109559971605970274534596862014728517418640889198609552329230484308714321450839762603627995251407989687253396546331808829640620615258352395054745750287759961729835575220337531857011354374603408498847160386899970699004815030544027790316454247823068492936918621580578463111596668713013015618568987237235288509264861249497715421833420428568606014682472077143585487415565706967765372022648544701585880162075847492265722600208558446652145839889394437092659180031138824646815708263010059485870400318648034219489727829064104507263688131373985525611732204024509122770022693976417470272013752399982976782217338826145327739130951193355408762382855063050397471264684204993755563270525522588635793369056816493299408349652485293806821732869748392205646382061385126800425762739265218823406558704964782626829881122')

The algorithm implemented by :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` is described in the :ref:`documentation <exploring-continued-fractions.fast-algorithms>`.

For rational numbers :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` will produce exactly the same results as the constructor for :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`, but with the benefit of allowing the user to specify an exact sequence of elements, if it is known, or an arbitrary sequence of elements for :ref:`approximations <exploring-continued-fractions.rational-approximation>`.

.. _creating-continued-fractions.rational-operations:

Rational Operations
===================

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class is a subclass of :py:class:`fractions.Fraction` and supports all of the rational operations implemented in the superclass. This means that :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances are fully operable as rational numbers, as well as encapsulating the properties of (finite) simple continued fractions.

.. note::

   Implementations of rational operations in the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class will always return a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance **unless** the operation is binary and the other operand is either not a :py:class:`fractions.Fraction` instance, or in some operations, such as :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__pow__`, :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__rpow__` etc., not an :py:class:`int`.

A few examples are given below of some key rational operations for the rational :math:`\frac{649}{200}` with ``ContinuedFraction(649, 200)``.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf.elements
   (3, 4, 12, 4)
   >>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
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
   >>> cf ** 2
   ContinuedFraction(9, 4)
   >>> (cf ** 2).elements
   (10, 1, 1, 7, 1, 4, 1, 3, 5, 1, 7, 2)
   >>> assert ContinuedFraction.from_elements(10, 1, 1, 7, 1, 4, 1, 3, 5, 1, 7, 2) == cf ** 2
   # True

As these examples illustrate, the continued fraction properties of the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances are fully respected by the rational operations.

Rational operations for :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` can involve any instance of :py:class:`numbers.Rational`, including :py:class:`int` and :py:class:`fractions.Fraction`, and the result is always a new :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance:

.. code:: python

   >>> cf = ContinuedFraction('0.5')
   >>> cf
   ContinuedFraction(1, 2)
   >>> id(cf), id(-cf)
   (4603182592, 4599771072)

There is no support for operations involving :py:class:`decimal.Decimal`:

.. code:: python

   >>> ContinuedFraction('1.5') + Decimal('0.5')
   TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'Fraction'

For any other numeric type, such as :py:class:`complex`, if the operation is defined the result is not a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance:
   
.. code:: python

   >>> complex(1, 2) + ContinuedFraction(3, 2)
   (2.5+2j)

The full set of rational operations can be viewed directly in the `class source <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/continuedfraction.py>`_ - the class source also can be viewed from links in the :doc:`class API reference <continuedfractions/continuedfraction>`.

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

where :math:`R_1 = [a_1; a_2, \ldots, a_n]` is the "residual", :math:`(n - 1)`-order simple continued fraction of :math:`\frac{b}{v}`, also called the :ref:`1st remainder <exploring-continued-fractions.remainders>` of the continued fraction :math:`[a_0;a_1,\ldots,a_n]` of :math:`\frac{a}{b}`. And :math:`\frac{1}{R_1}` is a symbolic expression for the rational number which is the (multiplicative) inverse of the rational number represented by :math:`R_1`.

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

Thus, we can say that if :math:`[a_0; a_1,\ldots, a_n]` is the :math:`n`-order simple continued fraction of a positive rational number :math:`\frac{a}{b}` then the simple continued fraction of :math:`-\frac{a}{b}` is given by:

.. math::

   \begin{cases}
   [-a_0;]                                     \hskip{3em} & n = 0 \\
   [-(a_0 + 1); 2]                             \hskip{3em} & n = 1 \text{ and } a_1 = 2 \\
   [-(a_0 + 1); a_2 + 1, a_3,\ldots, a_n]      \hskip{3em} & n \geq 2 \text{ and } a_1 = 1 \\
   [-(a_0 + 1); 1, a_1 - 1, a_2, \ldots,a_n]   \hskip{3em} & n \geq 2 \text{ and } a_1 \geq 2
   \end{cases}

This represents a **division-free** algorithm for computing the simple continued fraction of the negative of a positive rational number, and is faithfully implemented in the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__neg__` method.

We can verify this with :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances, starting with non-trivial cases with small fractions :math:`\frac{a}{b}` where :math:`|a| < |b|`:

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

The construction (creation + initialisation) of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances occurs mostly in the :py:class:`fractions.Fraction` class, but there are no sign-related differences either in the construction steps in :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__new__`.

A few examples are given below.

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
