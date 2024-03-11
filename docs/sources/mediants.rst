========
Mediants
========

Another feature which the package includes is `mediants <https://en.wikipedia.org/wiki/Mediant_(mathematics)>`_, which are useful not for only approximations but also have very interesting connections to other areas of number theory, including ordered sequences of rational numbers.

.. _mediants.mediants-and-their-properties:

Mediants and their Properties
-----------------------------

The (simple) **mediant** of two rational numbers :math:`\frac{a}{b}` and :math:`\frac{c}{d}`, where :math:`b, d \neq 0`, is defined as the rational number:

.. math::

   \frac{a + c}{b + d}

Assuming that :math:`\frac{a}{b} < \frac{c}{d}` and :math:`bd > 0` the mediant above has the property that:

.. math::

   \frac{a}{b} < \frac{a + c}{b + d} < \frac{c}{d}

Mediants can give good rational approximations to real numbers of interest.

The ``ContinuedFraction`` class provides a ``.mediant()`` method which can be used to calculate mediants with other ``ContinuedFraction`` or ``fractions.Fraction`` objects. The result is also a ``ContinuedFraction`` object. A few examples are given below of how to calculate mediants.

.. code:: python

   >>> ContinuedFraction('0.5').mediant(Fraction(2, 3))
   ContinuedFraction(3, 5)
   >>> ContinuedFraction('0.6').elements
   (0, 1, 1, 2)
   >>> ContinuedFraction(1, 2).mediant(ContinuedFraction('2/3'))
   ContinuedFraction(3, 5)
   >>> assert ContinuedFraction(1, 2) < ContinuedFraction(1, 2).mediant(Fraction(3, 4)) < ContinuedFraction(3, 4)
   # True


In particular, the mediant :math:`\frac{a + c}{b + d}` of :math:`\frac{a}{b}` and :math:`\frac{c}{d}` has the property that **if** :math:`bc - ad = 1` then :math:`\frac{a + c}{b + d}` is the fraction with the smallest denominator lying in the (open) interval :math:`(\frac{a}{b}, \frac{c}{d})`. As :math:`\frac{1}{2}` and :math:`\frac{2}{3}` satisfy the relation :math:`bc - ad = 2\cdot2 - 1\cdot3 = 4 - 3 = 1` it follows that their mediant :math:`\frac{3}{5}` is the "next" (or "first")  fraction after :math:`\frac{1}{2}`, but before :math:`\frac{2}{3}`, compared to any other fraction in that interval with a denominator :math:`\geq b + d = 5`.

This is an ordering property that links mediants to ordered sequences of rational numbers such as `Farey sequences <https://en.wikipedia.org/wiki/Farey_sequence>`_, and tree orderings such as the `Stern-Brocot tree <https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree>`_.

.. _mediants.generalised-mediants:

Generalised Mediants
--------------------

The concept of the simple mediant of two fractions of :math:`\frac{a}{b}` and :math:`\frac{c}{d}` as given above can be generalised to :math:`k`-th **left-** and **right-mediants**: for a positive integer :math:`k` the :math:`k`-th left mediant of :math:`\frac{a}{b}` and :math:`\frac{c}{d}` can be defined as:

.. math::

   \frac{ka + c}{kb + d}

while the :math:`k`-th right mediant can be defined as:

.. math::

   \frac{a + kc}{b + kd}

For :math:`k = 1` the left- and right-mediants are identical, but as :math:`k \longrightarrow \infty` they separate into two different, strictly monotonic, sequences converging to opposite limits: the left-mediants form a strictly decreasing sequence lower-bounded by :math:`\frac{a}{b}`, thus converging to :math:`\frac{a}{b}`:

.. math::

   \frac{a}{b} < \cdots < \frac{3a + c}{3b + d} < \frac{2a + c}{2b + d} < \frac{a + c}{b + d} < \frac{c}{d}

.. math::

   \lim_{k \to \infty} \frac{ka + c}{kb + d} = \lim_{k \to \infty} \frac{a + \frac{c}{k}}{b + \frac{d}{k}} = \frac{a}{b}

while the right-mediants form a strictly increasing sequence upper-bounded by :math:`\frac{c}{d}`, thus converging to :math:`\frac{c}{d}`:

.. math::

   \frac{a}{b} < \frac{a + c}{b + d} < \frac{a + 2c}{b + 2d} < \frac{a + 3c}{b + 3d} < \cdots < \frac{c}{d}

.. math::

   \lim_{k \to \infty} \frac{a + kc}{b + kd} = \lim_{k \to \infty} \frac{\frac{a}{k} + c}{\frac{b}{k} + d} = \frac{c}{d}

We can illustrate this using the ``ContinuedFraction.mediant`` method using the ``dir`` option to set the “direction” of the mediant, starting with the right mediants, which don't need to specified with ``dir='right'`` as that is the default value, and using ``k`` to set the mediant order, which defaults to ``k=1``.

.. code:: python

   # Right mediants
   >>> c1 = ContinuedFraction(1, 2)
   >>> c2 = ContinuedFraction(3, 5)
   >>> c1.mediant(c2)
   ContinuedFraction(4, 7)
   >>> c1.mediant(c2).as_decimal()
   Decimal('0.5714285714285714285714285714')
   >>> c1.mediant(c2, k=10)
   ContinuedFraction(31, 52)
   >>> c1.mediant(c2, k=100).as_decimal()
   Decimal('0.5996015936254980079681274900')
   >>> c1.mediant(c2, k=10 ** 6)
   ContinuedFraction(3000001, 5000002)
   >>> c1.mediant(c2, k=10 ** 6).as_decimal()
   Decimal('0.5999999600000159999936000026')

And then the left mediants, specified with ``dir='left'``.

.. code:: python

   # Left mediants
   >>> c1.mediant(c2, dir='left')
   ContinuedFraction(4, 7)
   >>> c1.mediant(c2, dir='left', k=10)
   ContinuedFraction(13, 25)
   >>> c1.mediant(c2, dir='left', k=10).as_decimal()
   Decimal('0.52')
   >>> c1.mediant(c2, dir='left', k=100)
   ContinuedFraction(103, 205)
   >>> c1.mediant(c2, dir='left', k=100).as_decimal()
   Decimal('0.5024390243902439024390243902'
   >>> c1.mediant(c2, dir='left', k=10 ** 6)
   ContinuedFraction(1000003, 2000005)
   >>> c1.mediant(c2, dir='left', k=10 ** 6).as_decimal()
   Decimal('0.5000002499993750015624960938')

.. _mediants.references:

References
==========

[1] Baker, Alan. A concise introduction to the theory of numbers. Cambridge: Cambridge Univ. Pr., 2002.

[2] Khinchin, A. Ya. Continued Fractions. Dover Publications, 1997.

[3] Wikipedia. “Continued Fraction”. https://en.wikipedia.org/wiki/Continued_fraction. Accessed 19 February 2024.

[4] Wikipedia. “Farey sequence”. https://en.wikipedia.org/wiki/Farey_sequence. Accessed 10 March 2024.

[5] Wikipedia. “Mediant (mathematics)”. https://en.wikipedia.org/wiki/Mediant_(mathematics). Accessed 23 February 2024.

[6] Wikipedia. “Stern-Brocot Tree”. https://en.wikipedia.org/wiki/Stern%E2%80%93Brocot_tree. Accessed 23 February 2024.
