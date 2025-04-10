.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

=============================
Exploring Continued Fractions
=============================

Python objects of the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class encapsulate a number of basic and interesting properties of simple continued fractions that can be easily explored.

.. note::

   All references to continued fractions are to the simple forms.

.. _exploring-continued-fractions.elements-and-orders:

Elements and Order
==================

The **elements** (or coefficients) of a (possibly infinite), simple continued fraction :math:`[a_0;a_1,a_2\cdots]` of a real number :math:`x` include the head :math:`a_0 = [x]`, which is the integer part of :math:`x`, and the tail elements :math:`a_1,a_2,\cdots` which occur in the denominators of the fractional terms. The :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.elements` property can be used to look at their elements, e.g. for ``ContinuedFraction(649, 200)`` we have:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.elements
   (3, 4, 12, 4)

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

   >>> ContinuedFraction(415, 93).elements
   (4, 2, 6, 7)
   >>> ContinuedFraction(649, 200) + ContinuedFraction(415, 93)
   ContinuedFraction(143357, 18600)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).elements
   (7, 1, 2, 2, 2, 1, 1, 11, 1, 2, 12)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).order
   10

.. _exploring-continued-fractions.counting-elements:

Counting Elements
=================

A :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.counter` property is available to keep counts of elements:

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
   Counter({3: 2, 4: 2, 12: 1, 1: 1, 2: 1})
   >>> cf.truncate(1, 2, 3)
   >>> cf
   ContinuedFraction(649, 200)
   >>> cf.counter
   Counter({4: 2, 3: 1, 12: 1})

The :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.counter` property makes it possible to look for patterns in how elements change when performing rational operations with continued fractions, in a convenient way:

.. code:: python

   >>> cf2 = ContinuedFraction(415, 93)
   >>> cf2.counter
   Counter({4: 1, 2: 1, 6: 1, 7: 1})
   >>> (cf + cf2).counter
   Counter({1: 4, 2: 4, 7: 1, 11: 1, 12: 1})
   >>>  (cf - cf2).counter
   Counter({1: 6, -2: 1, 3: 1, 72: 1, 10: 1})
   >>> (cf1 / cf2).counter
   Counter({1: 8, 2: 2, 0: 1, 102: 1, 6: 1})
   >>> (cf1 * cf2).counter
   Counter({5: 2, 14: 1, 2: 1, 12: 1, 4: 1, 1: 1})

.. _exploring-continued-fractions.convergents-and-rational-approximations:

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

.. _exploring-continued-fractions.fast-algorithms:

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

.. _exploring-continued-fractions.rational-approximation:

Rational Approximation
----------------------

A second key property of convergents is related to `best rational approximations <https://en.wikipedia.org/wiki/Continued_fraction#Best_rational_approximations>`_ of real numbers: there are different definitions of this, but a common one is that a rational number :math:`\frac{p}{q}`, where :math:`q > 0`, is a best rational approximation of a real number :math:`x`, if :math:`\frac{p}{q}` is closer to :math:`x`, as measured by :math:`\lvert \frac{p}{q} - x \rvert`, than any other rational number :math:`\frac{p\prime}{q\prime}` (:math:`q\prime > 0`) with denominator :math:`q\prime \leq q`.

Convergents have this property: we can illustrate this with a little example using the rational number :math:`-\frac{415}{93}`, which has the continued fraction :math:`[-5; 1, 1, 6, 7]`, and its 3rd convergent :math:`-\frac{58}{13}`, which has the continued fraction :math:`[-5; 1, 1, 6]`.

.. code:: python

   >>> cf = ContinuedFraction(-415, 93)
   >>> cf.convergent(3)
   ContinuedFraction(-58, 13)
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

We can show, for example, that the square root :math:`\sqrt{n}` of any non-square (positive) integer :math:`n` is irrational by considering positive integers of the form :math:`n = (ka)^2 + r`, for integers :math:`k, a, r > 0` and :math:`(k, a) = 1`. From this we have:

.. math::
   :nowrap:

   \begin{alignat*}{1}
   & r &&= n - (ka)^2 = \left(\sqrt{n} + ka\right)\left(\sqrt{n} - ka\right) \\
   & \sqrt{n} &&= ka + \frac{r}{2ka + \sqrt{n}}
   \end{alignat*}

Expanding the expression for :math:`\sqrt{n}` recursively we have the following infinite periodic continued fraction for :math:`\sqrt{n}`:

.. math::

   \sqrt{n} = ka + \cfrac{r}{2ka + \cfrac{r}{2ka + \cfrac{r}{2ka + \ddots}}}

With :math:`k = a = r = 1` we can represent :math:`\sqrt{2}` as the continued fraction:

.. math::

   \sqrt{2} = 1 + \cfrac{1}{2 + \cfrac{1}{2 + \cfrac{1}{2 + \ddots}}}

written more compactly as :math:`[1; \bar{2}]`, where :math:`\bar{2}` represents the infinite (periodic) sequence :math:`2, 2, 2, \ldots`.

We can illustrate rational approximation with the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.from_elements` method by continuing the :ref:`earlier example <creating-continued-fractions.irrational-numbers>` for :math:`\sqrt{2}` but instead using by iteratively constructing more accurate continued fraction representations with higher convergents:

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

With the 10th convergent of :math:`\sqrt{2}` we have obtained an approximation that is accurate to :math:`6` decimal places in the fractional part. We'd ideally like to have as few elements as possible in our :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` approximation of :math:`\sqrt{2}` for a desired level of accuracy, but this partly depends on how fast the partial, finite continued fractions represented by the chosen sequences of elements in our approximations are converging to the true value of :math:`\sqrt{2}` - these partial, finite continued fractions in a given continued fraction are called :ref:`convergents <exploring-continued-fractions.convergents-and-rational-approximations>`, and will be discussed in more detail later on.

If we use the 100th convergent (with :math:`101` elements consisting of the integer part  :math:`1`, plus a tail of one hundred 2s), we get more accurate results:

.. code:: python

   # Create a `ContinuedFraction` from the sequence 1, 2, 2, 2, ..., 2, with one hundred 2s in the tail
   >>> sqrt2_100 = ContinuedFraction.from_elements(1, *[2] * 100)
   ContinuedFraction(228725309250740208744750893347264645481, 161733217200188571081311986634082331709)
   >>> sqrt2_100.elements
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

.. _exploring-continued-fractions.even-and-odd-order-convergents:

Even- and Odd-Indexed Convergents
---------------------------------

The even- and odd-indexed convergents behave differently: the even-indexed convergents :math:`C_0,C_2,C_4,\ldots` strictly increase from below :math:`x`, while the odd-indexed convergents :math:`C_1,C_3,C_5,\ldots` strictly decrease from above :math:`x`, both at a decreasing rate. This is captured by the formula:

.. math::

   \frac{p_k}{q_k} - \frac{p_{k - 2}}{q_{k - 2}} = \frac{(-1)^ka_k}{q_kq_{k - 2}}, \hskip{3em} k \geq 2

The :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class provides properties for generating even-indexed convergents (:py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.even_convergents`) and odd-indexed convergents (:py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.odd_convergents`), as illustrated below.

.. code:: python

   >>> dict(ContinuedFraction(649, 200).even_convergents)
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
   >>> cf_even_convergents = dict(cf.even_convergents)
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
   >>> cf_odd_convergents = dict(cf.odd_convergents)
   >>> cf_odd_convergents[3] - cf_odd_convergents[1]
   >>> ContinuedFraction(-1, 12)
   >>> cf_odd_convergents[5] - cf_odd_convergents[3]
   >>> ContinuedFraction(-1, 420)
   >>> cf_odd_convergents[7] - cf_odd_convergents[5]
   >>> ContinuedFraction(-1, 14280)
   >>> cf_odd_convergents[9] - cf_odd_convergents[7]
   >>> ContinuedFraction(-1, 485112)

.. _exploring-continued-fractions.semiconvergents:

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
   >>> cf.elements
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
   >>> cf.elements
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

.. _exploring-continued-fractions.remainders:

Remainders
==========

The :math:`k`-th remainder :math:`R_k` of a (simple) continued fraction :math:`[a_0; a_1,\ldots]` of a real number :math:`x` is the (simple) continued fraction :math:`[a_k;a_{k + 1},\ldots]`, obtained from the original by "removing" the elements of the :math:`(k - 1)`-st convergent :math:`C_{k - 1} := [a_0;a_1,\ldots,a_{k - 1}]`:

.. math::

   R_k = a_k + \cfrac{1}{a_{k + 1} + \cfrac{1}{a_{k + 2} \ddots }}

where :math:`R_0 = x`. As with convergents, we can also use :math:`R_k` to denote the number represented by the associated continued fraction :math:`[a_k;a_{k + 1},\ldots]`, and this number is rational if and only if the continued fraction is of finite order.

If :math:`[a_0; a_1,\ldots]` is of finite order :math:`n` then :math:`R_k` is of order :math:`(n - k)`. The remainders of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instances can be obtained via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.remainder` method, which takes a non-negative integer not exceeding the order of the original.

.. code:: python

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

Given a (possibly infinite) continued fraction :math:`[a_0; a_1, a_2,\ldots]` the remainders :math:`R_0,R_1,\ldots` satisfy the recurrence relation:

.. math::

   R_{k - 1} = a_{k - 1} + \frac{1}{R_k}, \hskip{3em} k \geq 1

where :math:`\frac{1}{R_k}` denotes the inverted continued fraction :math:`[0; a_k, a_{k + 1},\ldots]`. If the continued fraction :math:`[a_0; a_1, a_2,\ldots]` is finite of order :math:`n` and we let :math:`R_k = \frac{s_k}{t_k}` then the recurrence relation above can be written as:

.. math::

   R_{k - 1} = \frac{s_{k - 1}}{t_{k - 1}} = \frac{a_{k - 1}s_k + t_k}{s_k}, \hskip{3em} k \geq 1

This allows successive remainders to computed starting from :math:`R_n = [a_n;]` and working backwards to :math:`R_0 = [a_0; a_1, \ldots, a_n]`, as implemented in the remainders library function :py:func:`~continuedfractions.lib.remainders`, which is then called by the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.remainders` property.

.. _exploring-continued-fractions.khinchin-mean-constant:

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

   >>> ContinuedFraction(649, 200).elements
   (3, 4, 12, 4)
   >>> ContinuedFraction(649, 200).khinchin_mean
   Decimal('5.76899828122963409526846589869819581508636474609375')
   >>> ContinuedFraction(415, 93).elements
   (4, 2, 6, 7)
   >>> ContinuedFraction(415, 93).khinchin_mean
   Decimal('4.37951913988788898990378584130667150020599365234375')
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).elements
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

.. _exploring-continued-fractions.references:

References
==========

[1] Baker, A. A. (2002). A concise introduction to the theory of numbers. Cambridge University Press.

[2] Barrow, J. D. (2000, June 1). Chaos in Numberland: The secret life of continued fractions. Plus.Maths.org. Retrieved February 19, 2024, from https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractions

[3] Continued Fraction. (2024, March 31). In Wikipedia. https://en.wikipedia.org/wiki/Continued_fraction

[4] Python Software Foundation (n.d.). Decimal - Decimal fixed point and floating point arithmetic. Python 3.12.3 Documentation. Retrieved February 21, 2024, from https://docs.python.org/3/library/decimal.html

[5] Euler's constant. (2024, May 10). In Wikipedia. https://en.wikipedia.org/wiki/Euler%27s_constant

[6] Python Software Foundation (n.d.). Floating Point Arithmetic: Issues and Limitations. Python 3.12.3 Documentation. Retrieved February 20, 2024, from https://docs.python.org/3/tutorial/floatingpoint.html

[7] Python Software Foundation (n.d.). Fractions - Rational numbers. Python 3.12.3 Documentation. Retrieved February 21, 2024, from https://docs.python.org/3/library/fractions.html

[8] Khinchin's constant. (2024, May 3). In Wikipedia. https://en.wikipedia.org/wiki/Khinchin%27s_constant

[9] Khinchin, A. Y. (1997). Continued Fractions. Dover Publications.

[10] Nemiroff, R. J. (n.d.). The Square Root of Two to 1 Million Digits. Astronomy Picture of the Day. Retrieved March 13, 2024, from https://apod.nasa.gov/htmltest/gifcity/sqrt2.1mil
