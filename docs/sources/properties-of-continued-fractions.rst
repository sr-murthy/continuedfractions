=================================
Properties of Continued Fractions
=================================

A number of basic properties of continued fractions are encapsulated in ``ContinuedFraction``, as described below.

.. _properties-of-continued-fractions.elements-and-orders:

Elements and Orders
===================

The **elements** (or coefficients) of a (possibly infinite) continued fraction :math:`[a_0;a_1,a_2\cdots]` of a real number :math:`x` include the leading integer :math:`a_0 = \lfloor x \rfloor` (largest integer part of :math:`x`), and the whole numbers :math:`a_1,a_2,\cdots` in the denominators of the fractional terms. For ``ContinuedFraction`` objects the ``.elements`` property can be used to look at their elements, e.g. for ``ContinuedFraction(649, 200)`` we have:

.. code:: python

   >>> cf = ContinuedFraction(649, 200)
   >>> cf.elements
   (3, 4, 12, 4)

The **order** of a continued fraction is defined to be number of its elements **after** the first. Thus, for ``ContinuedFraction(649, 200)`` the order is ``3``:

.. code:: python

   >>> cf.order
   3

The elements and order of ``ContinuedFraction`` objects are well behaved with respect to all rational operations supported by
``fractions.Fraction``:

.. code:: python

   >>> ContinuedFraction(415, 93).elements
   (4, 2, 6, 7)
   >>> ContinuedFraction(649, 200) + ContinuedFraction(415, 93)
   ContinuedFraction(143357, 18600)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).elements
   (7, 1, 2, 2, 2, 1, 1, 11, 1, 2, 12)
   >>> (ContinuedFraction(649, 200) + ContinuedFraction(415, 93)).order
   10

.. _properties-of-continued-fractions.convergents-and-rational-approximations:

Convergents and Rational Approximations
=======================================

For an integer :math:`k >= 0` the :math:`k`-th **convergent** :math:`C_k` of a continued fraction :math:`[a_0; a_1,\ldots]` of a real number :math:`x` is defined to be the rational number and finite continued fraction represented by :math:`[a_0; a_1,\ldots,a_k]`, formed from the first :math:`k + 1` elements of the original.

.. math::

   C_k = a_0 + \cfrac{1}{a_1 + \cfrac{1}{a_2 \ddots \cfrac{1}{a_{k-1} + \cfrac{1}{a_k}}}}

Each convergent :math:`C_k` represents a **rational approximation** :math:`\frac{p_k}{q_k}` of :math:`x`, and we can define an error term :math:`\epsilon_k = x - C_k = x - \frac{p_k}{q_k}`. If we assume :math:`x > 0` then the convergents form a strictly increasing sequence of rational numbers converging to :math:`x` as :math:`n \longrightarrow \infty`. So, formally:

.. math::

   \frac{p_0}{q_0} < \frac{p_1}{q_1} < \cdots \frac{p_n}{q_n} < \cdots

where

.. math::

   \lim_{n \to \infty} \frac{p_n}{q_n} = x

This is equivalent to the limit :math:`\lim_{n \to \infty} \epsilon_n = 0`. If :math:`x` is irrational then the convergents may alternate about :math:`x`, but still converge to it. If and only if :math:`x` is rational do we have the case that the convergent sequence is finite and terminates in :math:`x`.

The ``ContinuedFraction`` class provides a ``.convergents`` property for objects, which returns an immutable map
(`types.MappingProxyType <https://docs.python.org/3/library/types.html#types.MappingProxyType>`_) of all :math:`k`-order convergents, indexed (keyed) by integers :math:`k=0,1,\ldots,n`, where :math:`n` is the order of the continued fraction.

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

Obviously, we can only handle finite continued fractions in Python, so the convergents produced by ``ContinuedFraction`` will always be finite in number, regardless of whether the real numbers they approximate are rational or irrational. We can verify some of these properties for convergents, e.g. that :math:`C_0 < C_1 < \cdots < C_n`, for ``ContinuedFraction(649, 200)`` and also ``ContinuedFraction(math.pi)``:

.. code:: python

   >>> assert cf.convergents[0] < cf.convergents[1] < cf.convergents[2] < cf.convergents[3] == cf
   # True
   >>> pi_cf = ContinuedFraction(math.pi)
   >>> pi_cf.convergents
   mappingproxy({0: Fraction(3, 1), 1: Fraction(22, 7), 2: Fraction(333, 106), 3: Fraction(355, 113), ... , 27: Fraction(3141592653589793, 1000000000000000)})
   >>> assert pi_cf.convergents[27] < math.pi
   # True

**Note**: As the convergents are constructed during ``ContinuedFraction`` object initialisation, the objects that represent them cannot be of type ``ContinuedFraction``, due to recursion errors. Thus, it was decided to keep them as ``fractions.Fraction`` objects.

.. _properties-of-continued-fractions.segments-and-remainders:

Segments and Remainders
=======================

Convergents are linked to the concept of **segments**, which are finite subsequences of elements of a given continued fraction. More precisely, we can define the :math:`k`-th segment :math:`S_k` of a continued fraction :math:`[a_0; a_1,\ldots]` as the sequence of its first :math:`k + 1` elements, namely :math:`a_0,a_1,\ldots,a_k`, which uniquely determines the :math:`k`-order convergent :math:`C_k` of the continued fraction, as defined above.

The segments of ``ContinuedFraction`` objects can be obtained via the ``.segment()`` method, which takes a non-negative integer not exceeding the order.

.. code:: python

   >>> cf.segment(0), cf.segment(1), cf.segment(2), cf.segment(3)
   (ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))3

**Note**: Unlike the :math:`k`-order convergents the segments are ``ContinuedFraction`` objects and uniquely represent them as such.

A related concept is that of **remainders** of continued fractions, which are (possibly infinite) subsequences of elements of a given continued fraction, starting a given element. More precisely, we can define the :math:`k`-th remainder :math:`R_k` of a continued fraction represented by :math:`[a_0; a_1,\ldots]` as the sequence of elements :math:`a_k,a_{k + 1},\ldots` starting from the :math:`k`-th element.

.. math::

   R_k = a_k + \cfrac{1}{a_{k + 1} + \cfrac{1}{a_{k + 2} \ddots }}

The remainders of ``ContinuedFraction`` objects can be obtained via the ``.remainder()`` method, which takes a non-negative integer not exceeding the order.

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

.. _properties-of-continued-fractions.references:

References
==========

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
