.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

===================
Continued Fractions
===================

It's useful to start with the basic mathematics of continued fractions, using a simple example.

.. _continued-fractions.basics:

The Basics
==========

Consider the `rational number <https://en.wikipedia.org/wiki/Rational_number>`_ :math:`\frac{649}{200} = \frac{3 \times 200 + 49}{200} = 3.245` which has a continued fraction representation, or simply, a continued fraction, given by:

.. math::

   \frac{649}{200} = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}

This is derived by repeatedly applying `Euclid's division lemma <https://en.wikipedia.org/wiki/Euclidean_division#Division_theorem>`_, as described below:

.. math::

   \begin{align}
   \frac{649}{200} &= \cfrac{3 \times 200 + 49}{200} \\
                   &= 3 + \cfrac{49}{200} \\
                   &= 3 + \cfrac{1}{\cfrac{200}{49}} \\
                   &= 3 + \cfrac{1}{\cfrac{4 \times 49 + 4}{49}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{4}{49}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{1}{\cfrac{49}{4}}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{1}{\cfrac{4 \times 12 + 1}{4}}} \\
                   &= 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}}
   \end{align}

The numbers :math:`3, 4, 12, 4` are called **elements** (or **coefficients**) of the continued fraction :math:`[3; 4, 12, 4]`, and the number of elements after the first - in this case :math:`3` - is defined to be its **order**. The order can be finite or infinite depending on whether the number represented is rational or irrational, as will be discussed later.

The representation :math:`[3; 4, 12, 4]` is called **simple** (or **regular**) because all of the numerators in the fractional terms are equal to :math:`1`, which makes the fractions irreducible (cannot be simplified further). Mathematically, the continued fraction is written as :math:`[3; 4, 12, 4]`. The representation is also unique - the only other representation is :math:`[3; 4, 12, 3, 1]`, which can be rewritten as :math:`[3; 4, 12, 4]`.

.. note::

   All references to "continued fraction" are to the simple forms.

We can think of :math:`3`, which is the integer part of :math:`\frac{649}{200} = 3.245`, as the "head" of the continued fraction, and the integers :math:`4, 12, 4`, which determine the fractional part :math:`\cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{49}{200} = 0.245` of the continued fraction, as its "tail". The order of the continued fraction is therefore the length of its tail.

We use here a widely used notation for continued fractions, which is as a tuple of integers :math:`[a_0; a_1, a_2, \ldots, a_n, \ldots]` standing for the expression:

.. math::

   a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 + \ddots \cfrac{1}{a_n + \ddots}}}

where :math:`a_0` is the integer part, and :math:`a_1,a_2,\ldots` are (positive) integers defining the fractional part, in the representation. If the order is finite, i.e. :math:`n < \infty`, then this expression describes a rational number, for which we may assume the last element :math:`a_n > 1` because :math:`[a_0; a_1, a_2, \ldots a_{n - 1}, a_n = 1] = [a_0; a_1, a_2, \ldots a_{n - 1} + 1]`.

.. _continued-fractions.from-numeric-types:

Creating Continued Fractions from Numeric Types
===============================================

Import the core class :py:class:`continuedfractions.continuedfraction.ContinuedFraction`.

.. code:: python

   >>> from continuedfractions.continuedfraction import ContinuedFraction

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance for :math:`\frac{649}{200}` can be created as follows.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf
   ContinuedFraction(649, 200)

.. note::

   The same instance can also be constructed using ``ContinuedFraction('649/200')``, ``ContinuedFraction('3.245')``, ``ContinuedFraction(Fraction(649, 200))``, ``ContinuedFraction(Fraction(649), 200))``, ``ContinuedFraction(649, Fraction(200)))``, and ``ContinuedFraction(Decimal('3.245'))``, and even ``ContinuedFraction(ContinuedFraction(649, 200))`` .

   But passing a numeric literal such as ``649/200`` will result in an evaluation of the decimal integer division using `binary floating point division <https://docs.python.org/3/tutorial/floatingpoint.html>`_, thus producing a fractional approximation, in this case, ``ContinuedFraction(3653545197704315, 1125899906842624)``.

.. note::

   All Python shell excerpts below (and elsewhere) were run in a Python 3.11.11 environment.

The elements of ``ContinuedFraction(649, 200)`` can be obtained via the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.elements` property, which returns a **generator** of the elements. The order :math:`3` can be obtained via the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.order` property:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> tuple(cf.elements)
   (3, 4, 12, 4)
   >>> cf.order
   3

For more details on the elements and order properties see :ref:`this <continued-fractions.elements-and-order>`.

As a shortcut, the :py:class:`decimal.Decimal` value of ``ContinuedFraction(649, 200)`` can be obtained the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.as_decimal()` method.

.. code:: python

   >>> cf.as_decimal()
   Decimal('3.245')

.. _continued-fractions.decimal-precision:

Decimal Precision
-----------------

According to the documentation the Python :py:mod:`decimal` library supports arbitrary precision arithmetic, subject to the limitations of the running environment, system, hardware etc. It does this via `context objects <https://docs.python.org/3.12/library/decimal.html#context-objects>`_ for :py:class:`~decimal.Decimal` instances, in which you can set the precision of the :py:class:`~decimal.Decimal` values in your current environment to whatever is appropriate to your computation or experiment, subject to the limitations of your environment and/or system.

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

.. _continued-fractions.irrational-numbers:

Irrational Numbers
------------------

Every finite continued fraction represents a rational number, as a finite continued fraction is a "nested" sum of rational numbers. Conversely, every rational number can be represented as a finite (and simple) continued fraction, by an iterative procedure using `Euclidean division <https://en.wikipedia.org/wiki/Continued_fraction#Calculating_continued_fraction_representations>`_. On the other hand, infinite continued fractions represent `irrational numbers <https://en.wikipedia.org/wiki/Irrational_number>`_ and conversely every infinite continued fraction represents an irrational number.

There are infinitely many rational and irrational numbers that cannot be represented exactly as binary fractions, which form the basis for `floating point arithmetic <https://docs.python.org/3/tutorial/floatingpoint.html>`_, and, therefore, also, cannot be represented exactly as Python :py:class:`float` instances. To deal with this, the package processes rational numbers using the :py:class:`fractions.Fraction` class, which allows for exact continued fractions for any rational number, limited only by the available memory and/or capacity of the running environment.

Continued fractions for irrational numbers given directly as :py:class:`float` instances end up as fractional approximations, as they rely on converting :py:class:`decimal.Decimal` representations of the given :py:class:`float` value to a :py:class:`fractions.Fraction` instance. However, as described in the :ref:`next section <continued-fractions.from-elements>`, the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method can be used to create :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances with arbitrary sequences of elements, which can give much more accurate results.

An example is given below for the irrational :math:`\sqrt{2}`, which is given by the infinite periodic continued fraction :math:`[1; 2, 2, 2, \ldots]`, where the :py:class:`decimal.Decimal` precision has been set to `100`. We first begin by constructing the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance for :math:`\sqrt{2}` directly from a ``math.sqrt(2)`` value:

.. code:: python

   >>> sqrt2 = ContinuedFraction(math.sqrt(2))
   >>> sqrt2
   ContinuedFraction(6369051672525773, 4503599627370496)
   >>> tuple(sqrt2.elements)
   # -> (1, 2, 2, 2, 2, ... ,1, 1, 10, 2, ... ,1, 3, 1, 17, 12, 3, 2, 6, 1, 11, 2, 2)
   >>> float(sqrt2)
   1.4142135623730951
   >>> sqrt2.as_decimal()
   Decimal('1.4142135623730951454746218587388284504413604736328125')
   >>> Decimal(math.sqrt(2)).as_integer_ratio()
   Fraction(6369051672525773, 4503599627370496)


Here, ``ContinuedFraction(6369051672525773, 4503599627370496)`` is a fractional approximation of :math:`\sqrt{2}`, for the reasons described above, and not exact, as reflected in the tail elements of the sequence deviating from the mathematically correct value of :math:`2`. Also, note that the decimal value of ``ContinuedFraction(math.sqrt(2))`` above for :math:`\sqrt{2}` is only accurate up to :math:`15` digits in the fractional part, compared to the `first one million digit representation <https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil>`_.

However, in the :ref:`next section <continued-fractions.from-elements>`, we describe a way to construct continued fractions with arbitary sequences of elements, which can produce results of any given desired level of accuracy for irrational numbers.

.. _continued-fractions.from-elements:

Creating Continued Fractions From Elements/Coefficients
=======================================================

Continued fractions can also be constructed from sequences of elements, using either the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` class method, or the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend` or :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.truncate` instance methods. Each is described below.

.. _continued-fractions.creation-from-complete-element-sequence:

New Instances From a Complete Sequence of Elements
--------------------------------------------------

The :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` class method allows new :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances to be created from a complete (ordered) sequence of elements. Some examples are given below.

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
   >>> tuple(cf_negative_inverse.elements)
   (-1, 1, 2, 4, 12, 4)

The given sequence of elements can be arbitrarily long, subject to the limitations of the environment, system etc.

A :py:class:`ValueError` is raised if the given elements are not integers, or if any tail elements are not positive integers.

.. code:: python

   >>> ContinuedFraction.from_elements('0', 1)
   ...
   ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
   >>> ContinuedFraction.from_elements(0, 1, 2.5)
   ...
   ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
   >>> ContinuedFraction.from_elements(1, 0)
   ...
   ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
   >>> ContinuedFraction.from_elements(1, -1)
   ...
   ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive

Here is an example for approximating :math:`\sqrt{2}` using :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` with :math:`[1; \overbrace{2, 2,\ldots, 2]}^{1000 \text{ twos}}` where the tail contains :math:`1000` twos.

.. code:: python

   >>> decimal.getcontext().prec = 1000
   >>> ContinuedFraction.from_elements(1, *[2] * 1000).as_decimal()
   >>> Decimal('1.414213562373095048801688724209698078569671875376948073176679737990732478462107038850387534327641572735013846230912297024924836055850737212644121497099935831413222665927505592755799950501152782060571470109559971605970274534596862014728517418640889198609552329230484308714321450839762603627995251407989687253396546331808829640620615258352395054745750287759961729835575220337531857011354374603408498847160386899970699004815030544027790316454247823068492936918621580578463111596668713013015618568987237235288509264861249497715421833420428568606014682472077143585487415565706967765372022648544701585880162075847492265722600208558446652145839889394437092659180031138824646815708263010059485870400318648034219489727829064104507263688131373985525611732204024509122770022693976417470272013752399982976782217338826145327739130951193355408762382855063050397471264684204993755563270525522588635793369056816493299408349652485293806821732869748392205646382061385126800425762739265218823406558704964782626829881122')

The algorithm implemented by :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` is division-free and uses a well known recurrence relation for convergents of simple continued fractions, which is described :ref:`here <continued-fractions.fast-algorithms>`.

For rational numbers :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` will produce exactly the same results as the constructor for :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`, but allows the user to specify an exact sequence of elements, if it is known, or an arbitrary sequence of elements for :ref:`approximations <continued-fractions.rational-approximation>` or experimental computations.

.. _continued-fractions.inplace-extension:

In-place Extension by New Elements
----------------------------------

The :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend` instance method can be used to perform an in-place extension from new elements - the new elements are added to the existing instance tail in the given order. To be precise, given a continued fraction :math:`[a_0; a_1, \ldots, a_n]` of order :math:`n` and an array of :math:`k \geq 1` non-negative integers :math:`(b_1, \ldots, b_k)` the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend` method implements the mapping:

.. math::

   [a_0; \overbrace{a_1, \ldots, a_n}^{\text{cf of order }n}], (\overbrace{b_1, \ldots, b_k}^{\text{#}k\text{ new elements}}) \longmapsto [a_0; \overbrace{a_1, \ldots, a_n, b_1, \ldots, b_k}^{\text{cf of order }(n + k)}]

Some examples are given below.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> id(cf)
   4762928384
   >>> cf.extend(5, 2)
   >>> cf
   ContinuedFraction(7457, 2298)
   >>> tuple(cf.elements)
   (3, 4, 12, 4, 5, 2)
   >>> assert cf == ContinuedFraction.from_elements(3, 4, 12, 4, 5, 2)
   # True
   >>> id(cf)
   4762928384

The result is an in-place modification of the existing instance, with the same object ID as before. All other attributes or properties will reflect the new values as determined by the complete sequence of elements formed by the original elements and the new elements provided with :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend`.

A :py:class:`ValueError` is raised if the tail elements provided are invalid, e.g. not positive integers.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf.extend(0, 4)
   ...
   ValueError: The elements/coefficients to be added to the tail must be positive integers.
   >>> cf.extend(1, -1)
   ...
   ValueError: The elements/coefficients to be added to the tail must be positive integers.

.. note::

   If the last of the new elements passed to :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend` happens to be :math:`1` then it is added to the previous element to ensure uniqueness of the new sequence of elements of the resulting continued fraction, e.g.:

   .. code:: python

      >>> cf = ContinuedFraction.from_elements(3, 4, 12, 3)
      >>> cf
      ContinuedFraction(490, 151)
      >>> cf.extend(1)
      >>> cf
      ContinuedFraction(649, 200)
      >>> tuple(cf.elements)
      (3, 4, 12, 4)

.. _continued-fractions.inplace-truncation:

In-place Truncation of Tail Elements
------------------------------------

The :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.truncate` instance method can be used to perform an in-place truncation of a trailing segment of the existing tail - the tail elements to be truncated are removed from the existing tail in the given order. To be precise, given a continued fraction :math:`[a_0; a_1, \ldots, a_n]` of order :math:`n` and a :math:`k`-length segment (or contiguous section) :math:`(a_{n - k + 1}, \ldots, a_n)` of its tail, where :math:`1 \leq k \leq n`, the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.extend` method implements the mapping:

.. math::

   [a_0; \overbrace{a_1, \ldots, a_n}^{\text{cf of order }n}], (\overbrace{a_{n - k + 1}, \ldots, a_n}^{\text{#}k\text{ tail elements}}) \longmapsto [a_0; \overbrace{a_1, \ldots, a_{n - k}}^{\text{cf of order }(n - k)}]

Some examples are given below.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> id(cf)
   4921448896
   >>> cf.truncate(12, 4)
   >>> cf
   ContinuedFraction(13, 4)
   >>> tuple(cf.elements)
   (3, 4)
   >>> assert cf == ContinuedFraction.from_elements(3, 4)
   # True
   >>> id(cf)
   4921448896

The result is an in-place modification of the existing instance, with the same object ID as before. All other attributes or properties will reflect the new values as determined by the complete sequence of elements formed by the truncation of the tail elements provided with :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.truncate`.

A :py:class:`ValueError` is raised if the tail elements provided are invalid, e.g. not positive integers, or do not form a trailing segment of the existing tail.

.. code:: python

   >>> cf = ContinuedFraction.from_elements(3, 4, 12, 4)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf.truncate(0, 4)
   ...
   ValueError: The elements/coefficients to be truncated from the tail must form a trailing segment of the existing tail.
   >>> cf.truncate(3, 4, 12, 4)
   ...
   ValueError: The elements/coefficients to be truncated from the tail must form a trailing segment of the existing tail.

.. _continued-fractions.rational-operations:

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
   >>> tuple(cf.elements)
   (3, 4, 12, 4)
   >>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
   >>> cf_inverse
   ContinuedFraction(200, 649)
   >>> tuple(cf_inverse.elements)
   (0, 3, 4, 12, 4)
   >>> assert cf_inverse == 1/cf
   # True
   >>> assert cf * cf_inverse == 1
   # True
   >>> cf_negative_inverse = ContinuedFraction.from_elements(-1, 1, 2, 4, 12, 4)
   >>> cf_negative_inverse
   ContinuedFraction(-200, 649)
   >>> tuple(cf_negative_inverse.elements)
   (-1, 1, 2, 4, 12, 4)
   >>> assert cf_negative_inverse == -1/cf
   # True
   >>> assert cf * cf_negative_inverse == -1
   >>> assert cf + (-cf) == cf_inverse + cf_negative_inverse == 0
   # True
   >>> cf ** 2
   ContinuedFraction(421201, 40000)
   >>> tuple((cf ** 2).elements)
   (10, 1, 1, 7, 1, 4, 1, 3, 5, 1, 7, 2)
   >>> assert ContinuedFraction.from_elements(10, 1, 1, 7, 1, 4, 1, 3, 5, 1, 7, 2) == cf ** 2
   # True

As these examples illustrate, the continued fraction properties of the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances are fully respected by the rational operations.

Rational operations for :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` can involve any instance of :py:class:`numbers.Rational`, including :py:class:`int` and :py:class:`fractions.Fraction`, but results are only guaranteed for the latter two types, and in these cases the result is always a new :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance.

.. code:: python

   >>> cf = ContinuedFraction('0.5')
   >>> cf
   ContinuedFraction(1, 2)
   >>> id(cf), id(-cf)
   (4603182592, 4599771072)

There is no support for binary operations involving :py:class:`decimal.Decimal`, :py:class:`complex`:

.. code:: python

   >>> ContinuedFraction('1.5') + Decimal('0.5')
   TypeError: argument should be a string or a Rational instance
   >>> ContinuedFraction(3, 2) + complex(1, 2)
   TypeError: argument should be a string or a Rational instance

The full set of rational operations can be viewed directly in the `class source <https://github.com/sr-murthy/continuedfractions/blob/main/src/continuedfractions/continuedfraction.py>`_ or the :doc:`API reference <continuedfractions/continuedfraction>`.

.. _continued-fractions.negative-continued-fractions:

“Negative” Continued Fractions
==============================

A brief explanation is given here of how continued fractions for negative fractions are implemented in this package. To illustrate the discussion we can consider the fraction :math:`\frac{-415}{93} = \frac{-5 \times 93 + 50}{93}`, which has the continued fraction :math:`[-5; 1, 1, 6, 7]`:

.. math::

   -\frac{415}{93} = -5 + \cfrac{1}{1 + \cfrac{1}{1 + \cfrac{1}{6 + \cfrac{1}{7}}}}

in comparison with :math:`\frac{415}{93} = \frac{4 \times 93 + 43}{93}`, which has the continued fraction :math:`[4; 2, 6, 7]`:

.. math::

   \frac{415}{93} = 4 + \cfrac{1}{2 + \cfrac{1}{6 + \cfrac{1}{7}}}

The implementation is again based on `Euclid's division lemma <https://en.wikipedia.org/wiki/Euclidean_division#Division_theorem>`_. Let :math:`\frac{a}{b}` be a positive rational with :math:`a > b` and :math:`a, b` coprime, and :math:`[a_0;a_1,\ldots,a_n]` the simple continued fraction of order :math:`n \geq 1` of :math:`\frac{a}{b}`, where we can assume :math:`a_n > 1`. The lemma implies that there are unique, positive integers :math:`q, v`, with :math:`0 < v < b`, such that :math:`a = qb + v`. Then:

.. math::

   \begin{align}
   \frac{a}{b} &= q + \frac{v}{b} \\
               &= q + \frac{1}{\frac{b}{v}} \\
               &= q + \frac{1}{R_1} \\
               &= [a_0 = q; a_1, \ldots, a_n]
   \end{align}

where :math:`R_1 = [a_1; a_2, \ldots, a_n]` is the "residual", :math:`(n - 1)`-order simple continued fraction of :math:`\frac{b}{v}`, also called the :ref:`1st remainder <continued-fractions.remainders>` of the continued fraction :math:`[a_0;a_1,\ldots,a_n]` of :math:`\frac{a}{b}`. If :math:`v = 1` then :math:`R_1 = [b;]` and :math:`[q; b]` is the simple continued fraction of :math:`\frac{a}{b}`. However, if :math:`v > 1` then :math:`R_1` is defined and and has the inversion :math:`\frac{1}{R_1} = [0; a_1, \ldots, a_n]`.

Wriring :math:`-a = -(qb + v)` as:

.. math::

   -a = -qb - v = -qb - b + b - v = -(q + 1)b + (b - v)

we have:

.. math::

   \begin{align}
   -\frac{a}{b} &= -(q + 1) + \frac{b - v}{b} \\
                &= -(q + 1) + \frac{1}{\frac{b}{b - v}} \\
                &= -(q + 1) + \frac{1}{1 + \frac{1}{\frac{b}{v} - 1}} \\
                &= -(q + 1) + \frac{1}{1 + \frac{1}{R_1 - 1}} \\
                &= [-(q + 1); 1, a_1 - 1, a_2, a_3,\ldots, a_n]
   \end{align}

where :math:`R_1 - 1 = [a_1 - 1;a_2,\ldots, a_n]` and :math:`\frac{1}{R_1 - 1} = [0; a_1 - 1, a_2, a_3,\ldots, a_n]`.

.. note::

   If the last element :math:`a_n = 1` then :math:`[a_0; a_1, \ldots, a_n] = [a_0;a_1,\ldots,a_{n - 1} + 1]` is of order :math:`(n - 1)`. So in the representation :math:`[-(q + 1); 1, a_1 - 1, a_2, a_3,\ldots, a_n]` above for :math:`-\frac{a}{b}`, if :math:`a_1 = 2` then :math:`a_1 - 1 = 1` and the segment :math:`[-(q + 1); 1, a_1 - 1] = [-(q + 1); 1, 1] = [-(q + 1); 2]` is of order :math:`1`.

If :math:`\bar{R}_1` denotes the :ref:`1st remainder <continued-fractions.remainders>` :math:`[1; a_1 - 1, a_2, a_3,\ldots, a_n]` in the representation above for :math:`-\frac{a}{b}` then :math:`\bar{R}_1` is an :math:`n`-order, simple continued fraction. A special case is when :math:`a_1 = 1`: in this case :math:`a_0 = -1` and :math:`\bar{R}_1 = [a_2 + 1; a_3, \ldots, a_n]` is an :math:`(n - 2)`-order simple continued fraction. Note that this special case also applies when :math:`0 < a < b`.

Thus, we can say that if :math:`[a_0; a_1,\ldots, a_n]` is the :math:`n`-order simple continued fraction of a positive rational number :math:`\frac{a}{b}` then the simple continued fraction of :math:`-\frac{a}{b}` is given by:

.. math::

   \begin{cases}
   [-a_0;]                                     \hskip{3em} & n = 0 \\
   [-(a_0 + 1); 2]                             \hskip{3em} & n = 1 \text{ and } a_1 = 2 \\
   [-(a_0 + 1); a_2 + 1, a_3,\ldots, a_n]      \hskip{3em} & n \geq 2 \text{ and } a_1 = 1 \\
   [-(a_0 + 1); 1, a_1 - 1, a_2, \ldots,a_n]   \hskip{3em} & n \geq 2 \text{ and } a_1 \geq 2
   \end{cases}

This provides a direct way to compute the continued fraction of the negative of a positive rational number, without going through usual division algorithm, and is faithfully implemented in the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__neg__` method.

The negation relations above can be illustrated with :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances for small fractions :math:`\frac{a}{b}` where :math:`|a| < |b|`:

.. code:: python

   >>> tuple(ContinuedFraction(2, 3).elements)
   (0, 1, 2)
   >>> tuple(ContinuedFraction(-2, 3).elements)
   (-1, 3)
   >>> assert ContinuedFraction.from_elements(-1, 3) == ContinuedFraction(-2, 3)
   # True
   >>> tuple(ContinuedFraction(1, 2).elements)
   (0, 2)
   >>> tuple(ContinuedFraction(-1, 2).elements)
   (-1, 2)
   >>> assert ContinuedFraction.from_elements(-1, 2) == ContinuedFraction.from_elements(-1, 1, 1) == ContinuedFraction(-1, 2)
   # True

and also fractions :math:`\frac{a}{b}` where :math:`|a| > |b|`:

.. code:: python

   >>> tuple(ContinuedFraction(17, 10).elements)
   (1, 1, 2, 3)
   >>> tuple(ContinuedFraction(-17, 10).elements)
   (-2, 3, 3)
   >>> assert ContinuedFraction.from_elements(-2, 3, 3) == ContinuedFraction(-17, 10)
   # True
   >>> tuple(ContinuedFraction(10, 7).elements)
   (1, 2, 3)
   >>> tuple(ContinuedFraction(-10, 7).elements)
   (-2, 1, 1, 3)
   >>> assert ContinuedFraction.from_elements(-2, 1, 1, 3) == ContinuedFraction(-10, 7)
   # True

The construction (creation + initialisation) of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances occurs mostly in the :py:class:`fractions.Fraction` class, but there are no sign-related differences either in the construction steps in :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.__new__`.

A few examples are given below (those involving :py:class:`decimal.Decimal` have precision set to `100`)

.. code:: python

   >>> ContinuedFraction(-415, 93)
   ContinuedFraction(-415, 93)
   >>> -ContinuedFraction(415, 93)
   ContinuedFraction(-415, 93)
   >>> tuple(ContinuedFraction(-415, 93).elements)
   (-5, 1, 1, 6, 7)
   >>> ContinuedFraction(-415, 93).as_decimal()
   Decimal('-4.462365591397849462365591397849462365591397849462365591397849462365591397849462365591397849462365591')
   >>> ContinuedFraction(415, 93).as_decimal()
   Decimal('4.462365591397849462365591397849462365591397849462365591397849462365591397849462365591397849462365591')

.. note::

   As negation of numbers is a unary operation, the minus sign in a “negative” :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance must be attached to the fraction, before enclosure in parentheses.

.. code:: python

   >>> -tuple(ContinuedFraction(415, 93).elements)
   ...
   TypeError: bad operand type for unary -: 'tuple'
   >>> -(ContinuedFraction(415, 93)).elements
   ...
   TypeError: bad operand type for unary -: 'tuple'
   >>> tuple((-ContinuedFraction(415, 93)).elements)
   (-5, 1, 1, 6, 7)
   >>> assert ContinuedFraction(415, 93) + (-ContinuedFraction(415, 93)) == 0
   # True

.. _continued-fractions.elements-and-order:

Elements and Order
==================

The **elements** (or coefficients) of a (possibly infinite), simple continued fraction :math:`[a_0;a_1,a_2\cdots]` of a real number :math:`x` include the head :math:`a_0 = [x]`, which is the integer part of :math:`x`, and the tail elements :math:`a_1,a_2,\cdots` which occur in the denominators of the fractional terms. The :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.elements` property returns a generator of the elements, e.g. for ``ContinuedFraction(649, 200)`` we have:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.elements
   <generator object ContinuedFraction.elements at 0x108c4b100>
   >>> tuple(cf.elements)
   (3, 4, 12, 4)

This means that to inspect the elements one must go through the core continued fraction division algorithm for rational numbers, as implemented in :py:func:`continuedfractions.lib.continued_fraction_rational`. Although this can end up being expensive in computations, depending on how you are using the elements array, the advantage is that manual changes to the numerator and/or denominator, which is supported by the :py:class:`fractions.Fraction` class, will be immediately reflected in the elements that are generated.

.. code:: python

   >>> cf = ContinuedFraction(3, 2)
   >>> tuple(cf.elements)
   (1, 2)
   >>> cf._numerator, cf._denominator = 5, 2
   >>> cf
   ContinuedFraction(5, 2)
   >>> tuple(cf.elements)
   (2, 2)

The **order** of a continued fraction is defined to be number of its tail elements, i.e. the elements defining the fractional part of the number represented by the continued fraction. Thus, for ``ContinuedFraction(649, 200)`` the order is ``3``:

.. code:: python

   >>> cf.order
   3

All :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances will have a finite sequence of elements and thus a finite order. The integers represent the special case of zero-order continued fractions.

.. code:: python

   >>> ContinuedFraction(3).order
   0

The elements and orders of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances are well behaved with respect to all rational operations supported by
:py:class:`fractions.Fraction`:

.. code:: python

   >>> tuple(ContinuedFraction(415, 93).elements)
   (4, 2, 6, 7)
   >>> ContinuedFraction(649, 200) + ContinuedFraction(415, 93)
   ContinuedFraction(143357, 18600)
   >>> tuple((ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).elements)
   (7, 1, 2, 2, 2, 1, 1, 11, 1, 2, 12)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).order
   10

For convenience a :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.counter` property is also available to keep counts of elements:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.counter
   Counter({4: 2, 3: 1, 12: 1})

The result is a :py:class:`collections.Counter` object, where the counts are displayed in order of the most common elements to the least (via :py:meth:`collections.Counter.most_common`).

The counter is effectively refreshed on each access, so that the effects of any operations that modify the underlying instance are immediately reflected.

.. code:: python

   >>> cf.extend(1, 2, 3)
   >>> cf
   ContinuedFraction(7603, 2343)
   >>> cf.counter
   Counter({3: 2, 4: 2, 12: 1, 1: 1, 2: 1})
   >>> cf.truncate(1, 2, 3)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf.counter
   Counter({4: 2, 3: 1, 12: 1})

.. _continued-fractions.convergents-and-rational-approximations:

Convergents and Rational Approximations
=======================================

For an integer :math:`k \geq 0` the :math:`k`-th **convergent** :math:`C_k` of a (simple) continued fraction :math:`[a_0; a_1,\ldots]` of a real number :math:`x` is the rational number :math:`\frac{p_k}{q_k}` with the simple continued fraction :math:`[a_0; a_1,\ldots,a_k]` formed from the first :math:`k + 1` elements of the original:

.. math::

   C_k = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 \ddots \cfrac{1}{a_{k-1} + \cfrac{1}{a_k}}}}

For a finite continued fraction of order :math:`n` there will be :math:`n + 1` convergents :math:`C_0, C_1, \ldots, C_n`, and the :math:`(n + 1)`-st convergent :math:`C_n = x`. The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class provides a :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.convergent` instance method to compute the :math:`k`-th convergent for :math:`k=0,1,\ldots,n`.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.convergent(0), cf.convergent(1), cf.convergent(2), cf.convergent(3)
   (ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))

Using the continued fraction :math:`[3; 4, 12, 4]` of :math:`\frac{649}{200}` as an example, we can verify that these convergents are mathematically correct.

.. math::
   :nowrap:

   \begin{alignat*}{2}
   & C_0 &&= [3;] = 3 = \frac{3}{1} = 3.0 \\
   & C_1 &&= [3; 4] = 3 + \cfrac{1}{4} = \frac{13}{4} = 3.25 \\
   & C_2 &&= [3; 4, 12] = 3 + \cfrac{1}{4 + \cfrac{1}{12}} = \frac{159}{49} = 3.2448979591836733 \\
   & C_3 &&= [3; 4, 12, 4] = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{649}{200} = 3.245
   \end{alignat*}

.. note::

   The index of a convergent of a continued fraction may be different from its order as a continued fraction, e.g. for the rational :math:`-\frac{415}{93}` which has the continued fraction :math:`[-5; 1, 1, 6, 7]`, the :math:`1`-st convergent is the integer :math:`-4` with the continued fraction :math:`[-5; 1] = [-4;]` of order :math:`0`, and the :math:`2`-nd convergent is the rational :math:`-\frac{9}{2}` with the continued fraction :math:`[-5; 1, 1] = [-5; 2]` of order :math:`1`.

.. _continued-fractions.fast-algorithms:

Fast Algorithms for Computing Convergents
-----------------------------------------

Convergents have very important properties that are key to fast approximation algorithms. A key property in this regard is a recurrence relation between the convergents given by:

.. math::
   
   \begin{align}
   p_k &= a_kp_{k - 1} + p_{k - 2} \\
   q_k &= a_kq_{k - 1} + q_{k - 2},        \hskip{3em}    k \geq 2
   \end{align}

where :math:`p_0 = a_0`, :math:`q_0 = 1`, :math:`p_1 = p_1p_0 + 1`, and :math:`q_1 = p_1`. This means that the :math:`k`-th convergent can be computed from the :math:`(k - 1)`-st and :math:`(k - 2)`-nd convergents. This formula is faithfully implemented, iteratively, by the :py:meth:`~continuedfractions.lib.convergent` method.

The same formula is also involved in the implementation of the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.convergents` property, which returns a generator of an enumerated sequence of all the convergents of the continued fraction:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf_convergents = dict(cf.convergents)
   >>> cf_convergents
   {0: ContinuedFraction(3, 1), 1: ContinuedFraction(13, 4), 2: ContinuedFraction(159, 49), 3: ContinuedFraction(649, 200)}

The result is an enumerated sequence of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances, where the enumeration is by convergent index.

The difference between consecutive convergents is given by the formula:

.. math::

   \frac{p_k}{q_k} - \frac{p_{k - 1}}{q_{k - 1}} = \frac{(-1)^{k + 1}}{q_kq_{k - 1}}, \hskip{3em} k \geq 1

and this can be illustrated with the convergents of the continued fraction :math:`[-5; 1, 1, 6, 7]` of :math:`-\frac{415}{93}`:

.. code:: python

   >>> cf = ContinuedFraction(-415, 93)
   >>> cf_convergents = dict(cf.convergents)
   >>> cf_convergents
   {0: ContinuedFraction(-5, 1), 1: ContinuedFraction(-4, 1), 2: ContinuedFraction(-9, 2), 3: ContinuedFraction(-58, 13), 4: ContinuedFraction(-415, 93)}
   >>> cf_convergents[1] - cf_convergents[0]
   ContinuedFraction(1, 1)
   >>> cf_convergents[2] - cf_convergents[1]
   ContinuedFraction(-1, 2)
   >>> cf_convergents[3] - cf_convergents[2]
   ContinuedFraction(1, 26)
   >>> cf_convergents[4] - cf_convergents[3]
   ContinuedFraction(-1, 1209)

.. _continued-fractions.rational-approximation:

Rational Approximation
----------------------

A second key property of convergents is related to `best rational approximations <https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations>`_ of real numbers: there are different definitions of this, but a common one is that a rational number :math:`\frac{p}{q}`, where :math:`q > 0`, is a best rational approximation of a real number :math:`x`, if :math:`\frac{p}{q}` is closer to :math:`x`, as measured by :math:`\lvert \frac{p}{q} - x \rvert`, than any other rational number :math:`\frac{p\prime}{q\prime}` (:math:`q\prime > 0`) with denominator :math:`q\prime \leq q`.

Convergents have this property: we can illustrate this with a little example using the rational number :math:`-\frac{415}{93}`, which has the continued fraction :math:`[-5; 1, 1, 6, 7]`, and its 3rd convergent :math:`-\frac{58}{13}`, which has the continued fraction :math:`[-5; 1, 1, 6]`.

.. code:: python

   >>> cf = ContinuedFraction(-415, 93)
   >>> cf.convergent(3)
   ContinuedFraction(-58, 13)
   # ``Decimal`` precision set to 28 digits (default)
   >>> cf.convergent(3).as_decimal()
   Decimal('-4.461538461538461538461538462')
   >>> abs(cf - cf.convergent(3))
   ContinuedFraction(1, 1209)
   >>> abs(cf - cf.convergent(3)).as_decimal()
   Decimal('0.0008271298593879239040529363110')
   >>> abs(cf - ContinuedFraction(-58, 12))
   ContinuedFraction(23, 62)
   >>> abs(cf - ContinuedFraction(-58, 12)).as_decimal()
   Decimal('0.3709677419354838709677419355')

Convergents have a stronger version of this property: namely a rational number :math:`\frac{p}{q}` is a convergent of a (simple) continued fraction :math:`[a_0; a_1, \ldots]` of a real number :math:`x` if and only if it is a best rational approximation of :math:`x` compared to any other rational :math:`\frac{p\prime}{q\prime}` (:math:`q\prime > 0`) with denominator :math:`q\prime \leq q`. The sequence of convergents :math:`(C_k)` converges to :math:`x` as :math:`k \to \infty` - this is expressed formally by:

.. math::

   \lim_{k \to \infty} C_k = \lim_{k \to \infty} \frac{p_k}{q_k} = x, \hskip{3em} k \geq 1

A simple example of convergent approximations of real numbers is :math:`\sqrt{2}`, which has the the continued fraction:

.. math::

   \sqrt{2} = 1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{2 + \ddots}}}

written more compactly as :math:`[1; \bar{2}]`, where :math:`\bar{2}` represents the infinite (periodic) sequence :math:`2, 2, 2, \ldots`. The convergents of :math:`\sqrt{2}` can be constructed using the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method:

.. code:: python

   # 1st convergent of sqrt(2)
   >>> ContinuedFraction.from_elements(1, 2)
   ContinuedFraction(3, 2)
   >>> ContinuedFraction.from_elements(1, 2).as_decimal()
   >>> Decimal('1.5')

   # 2nd convergent of sqrt(2)
   >>> ContinuedFraction.from_elements(1, 2, 2)
   ContinuedFraction(7, 5)
   >>> ContinuedFraction.from_elements(1, 2, 2).as_decimal()
   >>> Decimal('1.4')

   # 3rd convergent of sqrt(2)
   >>> ContinuedFraction.from_elements(1, 2, 2, 2)
   ContinuedFraction(17, 12)
   >>> ContinuedFraction.from_elements(1, 2, 2, 2).as_decimal()
   >>> Decimal('1.416666666666666666666666667')

   ...

   # 10th convergent of sqrt(2)
   >>> ContinuedFraction.from_elements(1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2)
   ContinuedFraction(8119, 5741)
   >>> ContinuedFraction.from_elements(1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2).as_decimal()
   >>> Decimal('1.414213551646054694304128201')

With the 10th convergent :math:`\frac{8119}{5741}` of :math:`\sqrt{2}` we have obtained an approximation that is accurate to :math:`6` decimal places in the fractional part. We'd ideally like to have as few elements as possible in our :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximation of :math:`\sqrt{2}` for a desired level of accuracy, but this partly depends on how fast the partial, finite continued fractions represented by the chosen sequences of elements in our approximations are converging to the true value of :math:`\sqrt{2}` - these partial, finite continued fractions in a given continued fraction are called :ref:`convergents <continued-fractions.convergents-and-rational-approximations>`, and will be discussed in more detail later on.

If we use the 100th convergent (with :math:`101` elements consisting of the integer part  :math:`1`, plus a tail of one hundred 2s), we get more accurate results:

.. code:: python

   # Create a `ContinuedFraction` from the sequence 1, 2, 2, 2, ..., 2, with one hundred 2s in the tail
   >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
   ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
   >>> tuple(sqrt2_100.elements)
   # -> (1, 2, 2, 2, ..., 2) where there are `100` 2s after the `1`
   >>> sqrt2_100.as_decimal()
   Decimal('1.414213562373095048801688724')

The decimal value of ``ContinuedFraction.from_elements(1, *[2] * 100)`` in this construction is now accurate up to 27 digits in the fractional part, but the decimal representation stops there. This is because the :py:mod:`decimal` library uses a default `contextual precision <https://docs.python.org/3/library/decimal.html#decimal.DefaultContext>`_ of 28 digits, including the integer part. The :py:mod:`decimal` precision can be increased, and the accuracy of the "longer" approximation above can be compared, as follows:

.. code:: python

    # `decimal.Decimal.getcontext().prec` stores the current context precision
    >>> import decimal
    >>> decimal.getcontext().prec
    28
    # Increase it to 100 digits, and try again
    >>> decimal.getcontext().prec = 100
    >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
    >>> sqrt2_100
    ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
    >>> sqrt2_100.as_decimal()
    Decimal('1.414213562373095048801688724209698078569671875376948073176679737990732478462093522589829309077750929')

Now, the decimal value of ``ContinuedFraction.from_elements(1, *[2] * 100)`` is accurate up to 75 digits in the fractional part, but deviates from the `true value <https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil>`_ after the 76th digit onwards.

.. _continued-fractions.even-and-odd-order-convergents:

Even- and Odd-Indexed Convergents
---------------------------------

The even- and odd-indexed convergents behave differently: the even-indexed convergents :math:`C_0,C_2,C_4,\ldots` strictly increase from below :math:`x`, while the odd-indexed convergents :math:`C_1,C_3,C_5,\ldots` strictly decrease from above :math:`x`, both at a decreasing rate. This is captured by the formula:

.. math::

   \frac{p_k}{q_k} - \frac{p_{k - 2}}{q_{k - 2}} = \frac{(-1)^ka_k}{q_kq_{k - 2}}, \hskip{3em} k \geq 2

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class provides properties for generating even-indexed convergents (:py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.even_order_convergents`) and odd-indexed convergents (:py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.odd_convergents`), as illustrated below.

.. code:: python

   >>> dict(ContinuedFraction(649, 200).even_order_convergents)
   {0: ContinuedFraction(3, 1), 2: ContinuedFraction(159, 49)}
   >>> dict(ContinuedFraction(649, 200).odd_convergents)
   {1: ContinuedFraction(13, 4), 3: ContinuedFraction(649, 200)}

As with the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.convergents` property the result is a generator of enumerated sequence of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances, where the enumeration is by convergent index.

The different behaviour of even- and odd-indexed convergents can be illustrated by a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximation of :math:`\sqrt{2}` with one hundred 2s in the tail, using dictionaries to store the even- and odd-indexed convergents:

.. code:: python

   # Increase the current context precision to 100 digits
   >>> decimal.getcontext().prec = 100
   #
   # Construct an approximation for the square root of 2, with one hundred 2s in the tail
   >>> cf = ContinuedFraction.from_elements(1, *([2] * 100))
   >>> cf
   >>> ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
   >>> cf.as_decimal()
   Decimal('1.414213562373095048801688724209698078569671875376948073176679737990732478462093522589829309077750929')
   #
   # Differences between consecutive even-indexed convergents
   >>> cf_even_convergents = dict(cf.even_order_convergents)
   >>> cf_even_convergents[2] - cf_even_convergents[0]
   >>> ContinuedFraction(2, 5)
   >>> cf_even_convergents[4] - cf_even_convergents[2]
   >>> ContinuedFraction(2, 145)
   >>> cf_even_convergents[6] - cf_even_convergents[4]
   >>> ContinuedFraction(2, 4901)
   >>> cf_even_convergents[8] - cf_even_convergents[6]
   >>> ContinuedFraction(2, 166465)
   >>> cf_even_convergents[10] - cf_even_convergents[8]
   >>> ContinuedFraction(2, 5654885)
   #
   # Differences between consecutive odd-indexed convergents
   >>> cf_odd_convergents = dict(cf.odd_order_convergents)
   >>> cf_odd_convergents[3] - cf_odd_convergents[1]
   >>> ContinuedFraction(-1, 12)
   >>> cf_odd_convergents[5] - cf_odd_convergents[3]
   >>> ContinuedFraction(-1, 420)
   >>> cf_odd_convergents[7] - cf_odd_convergents[5]
   >>> ContinuedFraction(-1, 14280)
   >>> cf_odd_convergents[9] - cf_odd_convergents[7]
   >>> ContinuedFraction(-1, 485112)

.. _continued-fractions.semiconvergents:

Semiconvergents
---------------

`Semiconvergents <https://en.wikipedia.org/wiki/Continued_fraction#Semiconvergents>`_ are :ref:`mediants <sequences.mediants>` of consecutive convergents of continued fractions. More precisely, if :math:`\frac{p_{k - 1}}{ q_{k - 1}}` and :math:`\frac{p_k}{q_k}` are consecutive convergents of a (possibly infinite) continued fraction :math:`[a_0;a_1,a_2,\ldots,a_k, a_{k + 1}, \ldots]`, and :math:`m` is any positive integer, then the fraction:

.. math::

    \frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k}

is called a **semiconvergent** of :math:`\frac{p_{k - 1}}{q_{k - 1}}` and :math:`\frac{p_k}{q_k}`. This is also the :math:`m`-th :ref:`right-mediant <sequences.mediants.generalised>` of the two (consecutive) convergents, and is an intermediate fraction between them (the mediant property). So, assuming that :math:`\frac{p_{k - 1}}{q_{k - 1}} \leq \frac{p_k}{q_k}`, for any positive integer :math:`m`, we have:

.. math::

   \frac{p_{k - 1}}{q_{k - 1}} \leq \frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k} \leq \frac{p_k}{q_k}

If on the other hand :math:`\frac{p_{k - 1}}{q_{k - 1}} \geq \frac{p_k}{q_k}` the inequality above would be reversed. 

Some definitions of semiconvergents are more restricted: one such definition is the same as above, except that :math:`m` is required to be an integer in the range :math:`0..a_{k + 1}`, i.e. :math:`0 \leq m \leq a_{k + 1}`, where the corner cases are :math:`m = 0` in which case the semiconvergent is equal to :math:`\frac{p_{k - 1}}{q_{k - 1}}`, and :math:`m = a_{n + 1}` (if this is defined) in which the case the semiconvergent is equal to :math:`\frac{p_{k + 1}}{q_{k + 1}}`. Another restrictive definition is also the same as the first definition above except that :math:`m` is required to be an integer in the range :math:`1..a_{k + 1} - 1`, i.e. :math:`0 < m < a_{k + 1}`. In this latter definition, the two corner cases listed above are excluded.

The first, more general definition is used here, and has been implemented in the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class as the (cached) :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.semiconvergent` method. This takes two arguments: (1) a positive integer :math:`k` determining two consecutive convergents :math:`\frac{p_{k - 1}}{q_{k - 1}}, \frac{p_k}{q_k}` for which to take a semiconvergent, and (2) a positive integer :math:`m` for the index of the semiconvergent (see the definition of :ref:`"right-mediant"  <sequences.mediants.generalised>`).

A few examples are given below for the continued fraction :math:`[-5; 1, 1, 6, 7]` for :math:`-\frac{415}{93}`.

.. code:: python

   >>> cf = ContinuedFraction(-415, 93)
   >>> tuple(cf.elements)
   (-5, 1, 1, 6, 7)
   >>> dict(cf.convergents)
   {0: ContinuedFraction(-5, 1), 1: ContinuedFraction(-4, 1), 2: ContinuedFraction(-9, 2), 3: ContinuedFraction(-58, 13), 4: ContinuedFraction(-415, 93)}
   >>> cf.semiconvergent(3, 1)
   ContinuedFraction(-67, 15)
   >>> cf.semiconvergent(3, 2)
   ContinuedFraction(-125, 28)
   >>> cf.semiconvergent(3, 3)
   ContinuedFraction(-183, 41)
   >>> cf.semiconvergent(3, 4)
   ContinuedFraction(-241, 54)
   >>> cf.semiconvergent(3, 5)
   ContinuedFraction(-299, 67)
   >>> cf.semiconvergent(3, 6)
   ContinuedFraction(-357, 80)
   >>> cf.semiconvergent(3, 7)
   ContinuedFraction(-415, 93)

.. note::

   The continued fraction of an integer is of zero order, and thus has only one convergent - itself - and no semiconvergents. Attempting to call :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.semiconvergent` on any integer-valued :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance, for any value of :math:`k` and :math:`m`, produces a :py:class:`ValueError`.

   .. code:: python

      >>> ContinuedFraction(1).semiconvergent(0, 1)
      ...
      ValueError: `k` and `m` must be positive integers and `k` must be an integer in the range `1..n` where `n` is the order of the continued fraction

In relation to consecutive convergents :math:`\frac{p_{k - 1}}{q_{k - 1}}` and :math:`\frac{p_k}{q_k}` the :math:`m`-th semiconvergent :math:`\frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k}` is the mediant of their :math:`(m - 1)`-st semiconvergent :math:`\frac{p_{k - 1} + (m - 1)p_k}{q_{k - 1} + (m - 1)q_k}` and the :math:`k`-th convergent :math:`\frac{p_k}{q_k}`. The semiconvergent sequence :math:`\left( \frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k} \right)` is monotonic in :math:`m`, bounded on one side by :math:`\frac{p_k}{q_k}` (the side depends on whether :math:`k` is odd or even), and has the limit :math:`\frac{p_k}{q_k}` as :math:`m \to \infty`. This can be seen in the example above.

The semiconvergents have the same alternating behaviour in :math:`k` as the convergents: the difference between the :math:`m`-th semiconvergent :math:`\frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k}` and the :math:`(m - 1)`-st semiconvergent :math:`\frac{p_{k - 1} + (m - 1)p_k}{q_{k - 1} + (m - 1)q_k}` is given by:

.. math::

   \begin{align}
   \frac{p_{k - 1} + mp_k}{q_{k - 1} + mq_k} - \frac{p_{k - 1} + (m - 1)p_k}{q_{k - 1} + (m - 1)q_k} &=
   \frac{p_kq_{k - 1} - p_{k - 1}q_k}{q_{k - 1}^2 + (2m - 1)q_kq_{k - 1} + m(m - 1)q_k^2} \\ &=
   \frac{(-1)^{k + 1}}{q_{k - 1}^2 + (2m - 1)q_kq_{k - 1} + m(m - 1)q_k^2}
   \end{align}

This can be illustrated again using the continued fraction for :math:`-\frac{415}{93}`:

.. code:: python

   >>> cf = ContinuedFraction(-415, 93)
   >>> tuple(cf.elements)
   (-5, 1, 1, 6, 7)
   >>> dict(cf.convergents)
   {0: ContinuedFraction(-5, 1), 1: ContinuedFraction(-4, 1), 2: ContinuedFraction(-9, 2), 3: ContinuedFraction(-58, 13), 4: ContinuedFraction(-415, 93)}
   >>> cf.semiconvergent(1, 1), cf.semiconvergent(1, 2)
   (ContinuedFraction(-9, 2), ContinuedFraction(-13, 3))
   >>> cf.semiconvergent(1, 2) - cf.semiconvergent(1, 1)
   ContinuedFraction(1, 6)
   >>> cf.semiconvergent(2, 1), cf.semiconvergent(2, 2)
   (ContinuedFraction(-13, 3), ContinuedFraction(-22, 5))
   >>> cf.semiconvergent(2, 2) - cf.semiconvergent(2, 1)
   ContinuedFraction(-1, 15)
   >>> cf.semiconvergent(3, 1), cf.semiconvergent(3, 2)
   (ContinuedFraction(-67, 15), ContinuedFraction(-125, 28))
   >>> cf.semiconvergent(3, 2) - cf.semiconvergent(3, 1)
   ContinuedFraction(1, 420)
   >>> cf.semiconvergent(4, 1), cf.semiconvergent(4, 2)
   (ContinuedFraction(-473, 106), ContinuedFraction(-888, 199))
   >>> cf.semiconvergent(4, 2) - cf.semiconvergent(4, 1)
   ContinuedFraction(-1, 21094)

.. note::

   When calling :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.semiconvergent` the value of :math:`k`, which determines two consecutive convergents :math:`\frac{p_{k - 1}}{q_{k - 1}}, \frac{p_k}{q_k}` of a continued fraction, cannot exceed the order of the continued fraction.

.. _continued-fractions.remainders:

Remainders
==========

The :math:`k`-th remainder :math:`R_k` of a (simple) continued fraction :math:`[a_0; a_1,\ldots]` of a real number :math:`x` is the (simple) continued fraction :math:`[a_k;a_{k + 1},\ldots]`, obtained from the original by "removing" the elements of the :math:`(k - 1)`-st convergent :math:`C_{k - 1} := [a_0;a_1,\ldots,a_{k - 1}]`:

.. math::

   R_k = a_k + \cfrac{1}{a_{k + 1} + \cfrac{1}{a_{k + 2} \ddots }}

where :math:`R_0 = x`. As with convergents, we can also use :math:`R_k` to denote the number represented by the associated continued fraction :math:`[a_k;a_{k + 1},\ldots]`, and this number is rational if and only if the continued fraction is of finite order.

If :math:`[a_0; a_1,\ldots]` is of finite order :math:`n` then :math:`R_k` is of order :math:`(n - k)`. The remainders of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances can be obtained via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.remainder` method, which takes a non-negative integer not exceeding the order of the original.

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
   (ContinuedFraction(649, 200), ContinuedFraction(200, 49), ContinuedFraction(49, 4), ContinuedFraction(4, 1))

It is also possible to get all of the remainders at once using the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.remainders` property, which returns a generator of an enumerated sequence of the remainders in descending order of index:

.. code:: python

   >>> dict(ContinuedFraction('3.245').remainders)
   {3: ContinuedFraction(4, 1), 2: ContinuedFraction(49, 4), 1: ContinuedFraction(200, 49), 0: ContinuedFraction(649, 200)}

Using the simple continued fraction of :math:`\frac{649}{200}` we can verify that these remainders are mathematically correct.

.. math::
   :nowrap:

   \begin{alignat*}{2}
   & R_0 &&= [3; 4, 12, 4] = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{649}{200} \\
   & R_1 &&= [4; 12, 4] = {4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{200}{49} \\
   & R_2 &&= [12; 4] = {12 + \frac{1}{4}} = \frac{49}{4} \\
   & R_3 &&= [4;] = 4 = \frac{4}{1}
   \end{alignat*}

Given a (possibly infinite) continued fraction :math:`[a_0; a_1, a_2,\ldots]` the remainders :math:`R_0,R_1,\ldots` have the property that:

.. math::

   R_{k - 1} = a_{k - 1} + \frac{1}{R_k}, \hskip{3em} k \geq 1

where :math:`\frac{1}{R_k}` denotes the inverted continued fraction :math:`[0; a_k, a_{k + 1},\ldots]`. If the continued fraction :math:`[a_0; a_1, a_2,\ldots]` is finite of order :math:`n` and we let :math:`R_k = \frac{s_k}{t_k}` then:

.. math::

   R_{k - 1} = \frac{s_{k - 1}}{t_{k - 1}} = \frac{a_{k - 1}s_k + t_k}{s_k}, \hskip{3em} k \geq 1

This allows successive remainders to computed starting from :math:`R_n = [a_n;]` and working backwards to :math:`R_0 = [a_0; a_1, \ldots, a_n]`, as implemented in the remainders library function :py:func:`~continuedfractions.lib.remainders`, which is then called by the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.remainders` property.

.. _continued-fractions.khinchin-mean-constant:

Khinchin Mean & Khinchin's Constant
====================================

For a (possibly infinite) continued fraction :math:`[a_0; a_1, a_2,\ldots]` and a positive integer :math:`n` we define its :math:`n`-th **Khinchin mean** :math:`K_n` as the geometric mean of its first :math:`n` elements starting from :math:`a_1` (excluding the leading element :math:`a_0`):

.. math::

   K_n := \sqrt[n]{a_1a_2 \cdots a_n} = \left( a_1a_2 \cdots a_n \right)^{\frac{1}{n}}, \hskip{3em} n \geq 1

So :math:`K_n` is simply the geometric mean of the integers :math:`a_1, a_2,\ldots,a_n`, for :math:`n \geq 1`.

It has been proved that for irrational numbers, which have infinite continued fractions, there are infinitely many for which the quantity :math:`K_n` approaches a constant :math:`K_0 \approx 2.685452\ldots`, called `Khinchin's constant <https://en.wikipedia.org/wiki/Khinchin%27s_constant>`_, independent of the number. So:

.. math::

   \lim_{n \to \infty} K_n = \lim_{n \to \infty} \sqrt[n]{a_1a_2 \cdots a_n} = K_0 \approx 2.685452\ldots

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class provides a way of examining the behaviour of :math:`K_n` via the :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.khinchin_mean` property, as indicated in the examples below.

.. code:: python

   >>> tuple(ContinuedFraction(649, 200).elements)
   (3, 4, 12, 4)
   >>> ContinuedFraction(649, 200).khinchin_mean
   Decimal('5.76899828122963409526846589869819581508636474609375')
   >>> tuple(ContinuedFraction(415, 93).elements)
   (4, 2, 6, 7)
   >>> ContinuedFraction(415, 93).khinchin_mean
   Decimal('4.37951913988788898990378584130667150020599365234375')
   >>> tuple((ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).elements)
   (7, 1, 2, 2, 2, 1, 1, 11, 1, 2, 12)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).khinchin_mean
   Decimal('2.15015313349074244086978069390170276165008544921875')
   >>> ContinuedFraction(5000).khinchin_mean

For rational numbers, which have finite continued fractions, the Khinchin means are not defined for all :math:`n`, so this property is not all that useful for rationals. However, for approximations of irrationals the property is useful as given in the examples below using continued fraction approximations for :math:`\pi = [3; 7, 15, 1, 292, \ldots]`.

.. code:: python

   # 4th Khinchin mean for `\pi` using a 5-element continued fraction approximation
   >>> ContinuedFraction.from_elements(3, 7, 15, 1, 292).khinchin_mean
   Decimal('13.2325345812843568893413248588331043720245361328125')
   # 19th Khinchin mean for `\pi` using a 20-element continued fraction approximation
   >>> ContinuedFraction.from_elements(3, 7, 15, 1, 292, 1, 1, 1, 2, 1, 3, 1, 14, 2, 1, 1, 2, 2, 2, 2).khinchin_mean
   Decimal('2.60994679070748158977721686824224889278411865234375')

and :math:`\gamma = [0; 1, 1, 2, 1,\ldots]`, the `Euler-Mascheroni constant <https://en.wikipedia.org/wiki/Euler%27s_constant>`_:

.. code:: python

   # 4th Khinchin mean for `\gamma` using a 5-element continued fraction approximation
   >>> ContinuedFraction.from_elements(0, 1, 1, 2, 1).khinchin_mean
   Decimal('1.4422495703074085238171164746745489537715911865234375')
   # 19th Khinchin mean for `\gamma` using a 20-element continued fraction approximation
   >>> ContinuedFraction.from_elements(0, 1, 1, 2, 1, 2, 1, 4, 3, 13, 5, 1, 1, 8, 1, 2, 4, 1, 1, 40).khinchin_mean
   Decimal('2.308255739839563336346373034757561981678009033203125')

The constant :math:`\gamma`, which has not been proved to be irrational, is defined as:

.. math::

   \begin{align}
   \gamma &= \lim_{n\to\infty} \left( H_n - \log n \right) \\
          &= \lim_{n\to\infty} \left(\sum_{k=1}^n \frac1{k} -\log n\right) \\
          &=\int_1^\infty\left(\frac1{\lfloor x\rfloor} -\frac1x\right)\,dx
   \end{align}

where :math:`H_n = \sum_{k=1}^n \frac1{k} = 1 + \frac{1}{2} + \frac{1}{3} + \cdots \frac{1}{n}` is the :math:`n`-th harmonic number.

.. _continued-fractions.references:

References
==========

[1] Baker, A. A. (2002). A concise introduction to the theory of numbers. Cambridge University Press.

[2] Barrow, J. D. (2000, June 1). Chaos in Numberland: The secret life of continued fractions. Plus.Maths.org. Retrieved February 19, 2024, from https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractions

[3] Hatcher, A. (2024, September). Topology of Numbers. American Mathematical Society. https://pi.math.cornell.edu/~hatcher/TN/TNbook.pdf

[4] Python Software Foundation (n.d.). Decimal - Decimal fixed point and floating point arithmetic. Python 3.12.3 Documentation. Retrieved February 21, 2024, from https://docs.python.org/3/library/decimal.html

[5] Python Software Foundation (n.d.). Floating Point Arithmetic: Issues and Limitations. Python 3.12.3 Documentation. Retrieved February 20, 2024, from https://docs.python.org/3/tutorial/floatingpoint.html

[6] Python Software Foundation (n.d.). Fractions - Rational numbers. Python 3.12.3 Documentation. Retrieved February 21, 2024, from https://docs.python.org/3/library/fractions.html

[7] Khinchin, A. Y. (1997). Continued Fractions. Dover Publications.

[8] Nemiroff, R. J. (n.d.). The Square Root of Two to 1 Million Digits. Astronomy Picture of the Day. Retrieved March 13, 2024, from https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil
