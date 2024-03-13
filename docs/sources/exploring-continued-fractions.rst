=============================
Exploring Continued Fractions
=============================

Python objects of the :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` class encapsluate a number of basic and interesting properties of continued fractions that can be easily explored.

.. _exploring-continued-fractions.elements-and-orders:

Elements and Orders
===================

The **elements** (or coefficients) of a (possibly infinite) continued fraction :math:`[a_0;a_1,a_2\cdots]` of a real number :math:`x` include the head :math:`a_0 = [x]`, which is the integer part of :math:`x`, and the tail elements :math:`a_1,a_2,\cdots` which occur in the denominators of the fractional terms. The :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.elements` property can be used to look at their elements, e.g. for ``ContinuedFraction(649, 200)`` we have:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.elements
   (3, 4, 12, 4)

The **order** of a continued fraction is defined to be number of its elements **after** the first. Thus, for ``ContinuedFraction(649, 200)`` the order is ``3``:

.. code:: python

   >>> cf.order
   3

All :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects will have a finite sequence of elements and thus a finite order, even if mathematically the numbers they represent may be irrational. The integers represent the special case of zero-order continued fractions.

.. code:: python

   >> ContinuedFraction(3).order
   0

The elements and orders of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects are well behaved with respect to all rational operations supported by
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

.. _exploring-continued-fractions.convergents-and-rational-approximations:

Convergents and Rational Approximations
=======================================

For an integer :math:`k >= 0` the (simple) :math:`k`-th **convergent** :math:`C_k` of a continued fraction :math:`[a_0; a_1,\ldots]` of a real number :math:`x` is defined to be the rational number and finite, simple continued fraction represented by :math:`[a_0; a_1,\ldots,a_k]`, formed from the first :math:`k + 1` elements of the original.

.. math::

   C_k = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 \ddots \cfrac{1}{a_{k-1} + \cfrac{1}{a_k}}}}

We note that if a continued fraction :math:`[a_0; a_1,\ldots]` has a finite order :math:`n` then :math:`C_n` is just the rational number represented by :math:`[a_0; a_1,\ldots,a_n]`.

Each convergent :math:`C_k` represents a **rational approximation** :math:`\frac{p_k}{q_k}` of the given real number :math:`x`, and we can define an error term :math:`\epsilon_k = x - C_k = x - \frac{p_k}{q_k}`. If we assume :math:`x > 0` then the convergents form a sequence of rational numbers converging to :math:`x` as :math:`k \longrightarrow \infty`. So, formally:

.. math::

   \lim_{k \to \infty} C_k = \lim_{k \to \infty} \frac{p_k}{q_k} = x

This is equivalent to the limit :math:`\lim_{k \to \infty} \epsilon_k = 0`: if :math:`x` is rational the error term will vanish for some :math:`k >= 0` at which point the convergent :math:`C_k = x`. But if :math:`x` is irrational there will be infinitely many convergents, and their sequence may alternate about :math:`x`, but still converge to it.

The  :py:attr:`~continuedfractions.continuedfraction.ContinuedFraction.convergents` property for objects stores the convergents as an immutable map
(:py:class:`types.MappingProxyType`) of all :math:`k`-order convergents, indexed (keyed) by integers :math:`k=0,1,\ldots,n`, where :math:`n` is the order of the continued fraction.

.. code:: python

   >>> cf.convergents
   mappingproxy({0: Fraction(3, 1), 1: Fraction(13, 4), 2: Fraction(159, 49), 3: Fraction(649, 200)})
   >>> cf.convergents[2]
   Fraction(159, 49)
   >>> import operator
   >>> # Get the float value of this fraction
   >>> operator.truediv(*cf.convergents[2].as_integer_ratio())
   3.2448979591836733

Using the continued fraction representation :math:`[3; 4, 12, 4]` of :math:`\frac{649}{200}` we can verify that these convergents are correct.

.. math::
   :nowrap:

   \begin{alignat*}{2}
   & C_0 &&= [3;] = 3 = \frac{3}{1} = 3.0 \\
   & C_1 &&= [3; 4] = 3 + \cfrac{1}{4} = \frac{13}{4} = 3.25 \\
   & C_2 &&= [3; 4, 12] = 3 + \cfrac{1}{4 + \cfrac{1}{12}} = \frac{159}{49} = 3.2448979591836733 \\
   & C_3 &&= [3; 4, 12, 4] = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{649}{200} = 3.245
   \end{alignat*}

Obviously, we can only handle finite continued fractions in Python, so the convergents produced by :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` will always be finite in number, regardless of whether the real numbers they approximate are rational or irrational. We can verify the convergents for ``ContinuedFraction(math.pi)`` approach ``math.pi``:

.. code:: python

   >>> pi_cf = ContinuedFraction(math.pi)
   >>> pi_cf.convergents
   mappingproxy({0: Fraction(3, 1), 1: Fraction(22, 7), 2: Fraction(333, 106), 3: Fraction(355, 113), ... , 27: Fraction(3141592653589793, 1000000000000000)})
   >>> assert pytest.approx(pi_cf.convergents[27], abs=1e-28) == math.pi
   # True

**Note**: As the convergents are constructed during :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` object initialisation, the objects that represent them cannot be of type :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`, due to recursion errors. Thus, it was decided to keep them as :py:class:`fractions.Fraction` objects. This is also sufficient for the purposes of approximation. To use convergents as :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects use the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.segment` method, which is discussed next.

.. _exploring-continued-fractions.segments-and-remainders:

Segments and Remainders
=======================

Convergents are linked to the concept of **segments**, which are finite subsequences of elements of a given continued fraction. More precisely, we can define the :math:`k`-th segment :math:`S_k` of a continued fraction :math:`[a_0; a_1,\ldots]` as the sequence :math:`(a_0,a_1,\ldots,a_k)` of its first :math:`k + 1` elements, which uniquely determines the :math:`k`-order (simple) convergent :math:`C_k` of the continued fraction, as defined above.

The segments of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects can be obtained via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.segment` method, which takes a non-negative integer not exceeding the order.

.. code:: python

   >>> cf.segment(0), cf.segment(1), cf.segment(2), cf.segment(3)
   (ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))3

**Note**: Unlike the :math:`k`-order convergents the segments are :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects, and can be used as a proxy for the convergents.

A related concept is that of **remainders** of continued fractions, which are (possibly infinite) subsequences of elements of a given continued fraction, starting from a given element, usually the leading element :math:`a_0`. More precisely, we can define the :math:`k`-th remainder :math:`R_k` of a continued fraction :math:`[a_0; a_1,\ldots]` as the continued fraction :math:`[a_k;a_{k + 1},\ldots]`, obtained by "removing" the elements of the :math:`(k - 1)`-st segment :math:`S_{k - 1} = (a_0,a_1,\ldots,a_{k - 1})` from :math:`[a_0; a_1,\ldots]`.

.. math::

   R_k = a_k + \cfrac{1}{a_{k + 1} + \cfrac{1}{a_{k + 2} \ddots }}

The remainders of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects can be obtained via the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.remainder` method, which takes a non-negative integer not exceeding the order.

.. code:: python

   >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
   (ContinuedFraction(649, 200), ContinuedFraction(200, 49), ContinuedFraction(49, 4), ContinuedFraction(4, 1))

Using the continued fraction representation of :math:`\frac{649}{200}` we can verify that these remainders are correct.

.. math::
   :nowrap:

   \begin{alignat*}{2}
   & R_0 &&= [3; 4, 12, 4] = 3 + \cfrac{1}{4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{649}{200} \\
   & R_1 &&= [4; 12, 4] = {4 + \cfrac{1}{12 + \cfrac{1}{4}}} = \frac{200}{49} \\
   & R_2 &&= [12; 4] = {12 + \frac{1}{4}} = \frac{49}{4} \\
   & R_3 &&= [4;] = 4 = \frac{4}{1}
   \end{alignat*}

Given a (possibly infinite) continued fraction :math:`[a_0; a_1, a_2,\ldots]` the remainders :math:`R_1,R_2,\ldots` satisfy the following relation:

.. math::

   R_k = \frac{1}{R_{k - 1} - a_{k - 1}}, \hskip{1em} k \geq 1


Khinchin Means & Khinchin's Constant
====================================

For a (possibly infinite) continued fraction :math:`[a_0; a_1, a_2,\ldots]` and a positive integer :math:`n` we define its :math:`n`-th **Khinchin mean** :math:`K_n` as the geometric mean of its first :math:`n` elements starting from :math:`a_1` (excluding the leading element :math:`a_0`):

.. math::

   K_n := \sqrt[n]{a_1a_2 \cdots a_n} = \left( a_1a_2 \cdots a_n \right)^{\frac{1}{n}}, \hskip{1em} n \geq 1

So :math:`K_n` is simply the geometric mean of the integers :math:`a_1, a_2,\ldots,a_n`, for :math:`n \geq 1`.

It has been proved that for irrational numbers, which have infinite continued fraction representations, there are infinitely many for which the quantity :math:`K_n` approaches a constant :math:`K_0 \approx 2.685452\ldots`, called `Khinchin's constant <https://en.wikipedia.org/wiki/Khinchin%27s_constant>`_, independent of the number. So:

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

For rational numbers, which have finite continued fraction representations, the Khinchin means are not defined for all :math:`n`, so this property is not all that useful for rationals. However, for approximations of irrationals the property is useful as given in the examples below using continued fraction approximations for :math:`\pi = [3; 7, 15, 1, 292, \ldots]`.

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

[1] Baker, Alan. A concise introduction to the theory of numbers. Cambridge: Cambridge Univ. Pr., 2002.

[2] Barrow, John D. “Chaos in Numberland: The secret life of continued fractions.” plus.maths.org, 1 June 2000,
https://plus.maths.org/content/chaos-numberland-secret-life-continued-fractionsURL.

[3] Emory University Math Center. “Continued Fractions.” The Department of Mathematics and Computer Science, https://mathcenter.oxford.emory.edu/site/math125/continuedFractions/. Accessed 19 Feb 2024.

[4] Khinchin, A. Ya. Continued Fractions. New York: Dover Publications, 1997.

[5] Python 3.12.2 Docs. “decimal - Decimal fixed point and floating point arithmetic.” https://docs.python.org/3/library/decimal.html. Accessed 21 February 2024.

[6] Python 3.12.2 Docs. “Floating Point Arithmetic: Issues and Limitations.” https://docs.python.org/3/tutorial/floatingpoint.html. Accessed 20 February 2024.

[7] Python 3.12.2 Docs. “fractions - Rational numbers.” https://docs.python.org/3/library/fractions.html. Accessed 21 February
2024.

[8] Wikipedia. “Continued Fraction”. https://en.wikipedia.org/wiki/Continued_fraction. Accessed 19 February 2024.

[9] Wikipedia. "Euler's constant". https://en.wikipedia.org/wiki/Euler%27s_constant. Accessed 11 March 2024.

[10] Wikipedia. "Khinchin's constant". https://en.wikipedia.org/wiki/Khinchin%27s_constant. Accessed 11 March 2024.

[11] Wikipedia. “Mediant (mathematics)”. https://en.wikipedia.org/wiki/Mediant_(mathematics). Accessed 23 February 2024.

[12] Wikipedia. “Stern-Brocot Tree”. https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree. Accessed 23 February 2024.