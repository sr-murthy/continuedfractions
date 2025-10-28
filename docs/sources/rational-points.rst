.. meta::

   :google-site-verification: 3F2Jbz15v4TUv5j0vDJAA-mSyHmYIJq0okBoro3-WMY

============================
Rational Points in the Plane
============================

The :doc:`rational_points <continuedfractions/rational-points>` library provides a simple, low-level, but rich object-oriented interface for creating and operating on rational points in the ordinary :math:`xy`-plane, that is, points :math:`P = (x, y) \in \mathbb{R}^2` with rational coordinates :math:`x = \frac{a}{c}, y=\frac{b}{d} \in \mathbb{Q}` (where :math:`x,y` are necessarily reduced form fractions), which are thus elements of :math:`\mathbb{Q}^2`. One of the goals is to allow rational points to be described by pairs of :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`  objects, and compute with them in an intuitive, stateful way. There are also some features for computing certain arithmetical properties of rational points in the setting of projective space :math:`\mathbb{P}^2(\mathbb{Q})`.

.. note::

   The term "rational point" (and "rational points") in this documentation refers to such points exclusively, and the notation :math:`\mathbb{Q}^2` will be used when convenient.

The main feature is the :py:class:`~continuedfractions.rational_points.RationalPoint` class, and this is discussed in more detail below.

.. _rational-points.creating-rational-points:

Creating Rational Points
------------------------

A rational point object can be created by calling :py:class:`~continuedfractions.rational_points.RationalPoint` with a pair of rational-valued arguments, which in Python can be any instances of :py:class:`numbers.Rational`: specifically the class can be called with any pair of objects of individual type :py:class:`int`, :py:class:`~fractions.Fraction`, or :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`.

Some examples are given below:

.. code:: python

   >>> from fractions import Fraction as F
   >>> from continuedfractions import ContinuedFraction as CF
   >>> from continuedfractions.rational_points import RationalPoint as RP
   >>> O = RP(0, 0)
   >>> O
   RationalPoint(0, 0)
   >>> I = RP(1, 1)
   >>> I
   RationalPoint(1, 1)
   >>> P = RP(F(3, 5), F(-4, 5))
   >>> P
   RationalPoint(3/5, -4/5)
   >>> Q = RP(1, CF(2, 3))
   >>> Q
   RationalPoint(1, 2/3)

It is not possible to create objects with non-rational values, or with fewer or more than 2 values:

.. code:: python

   >>> RP(1)
   ...
   ValueError: A `RationalPoint` object must be specified as a pair of rational numbers `r` and `s`, each of type either integer (`int`), or fraction (`Fraction` or `ContinuedFraction`).
   >>> RP(1, 2, 3)
   ...
   ValueError: A `RationalPoint` object must be specified as a pair of rational numbers `r` and `s`, each of type either integer (`int`), or fraction (`Fraction` or `ContinuedFraction`).
   >>> RP(F(1, 3), .5)
   ...
   ValueError: A `RationalPoint` object must be specified as a pair of rational numbers `r` and `s`, each of type either integer (`int`), or fraction (`Fraction` or `ContinuedFraction`).

The zero rational point :math:`(0, 0)` can also be obtained via the :py:meth:`~continuedfractions.rational_points.RationalPoint.zero` class method:

.. code:: python

   >>> RP.zero()
   RationalPoint(0, 0)

.. _rational-points.internal-rep-and-coordinates:

Internal Representation & Coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Internally, the rational components of a :py:class:`~continuedfractions.rational_points.RationalPoint` object are stored as :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` objects, and are accessible individually via the superclass :py:attr:`~continuedfractions.rational_points.Dim2RationalCoordinates.x` and :py:attr:`~continuedfractions.rational_points.Dim2RationalCoordinates.y` properties, and via the :py:attr:`~continuedfractions.rational_points.RationalPoint.coordinates` property, as illustrated below:

.. code:: python

   >>> P = RP(F(3, 5), F(4, 5))
   >>> P.x
   ContinuedFraction(3, 5)
   >>> P.y
   ContinuedFraction(4, 5)
   >>> P.coordinates
   Dim2RationalCoordinates(3/5, 4/5)

The :py:attr:`~continuedfractions.rational_points.RationalPoint.coordinates` property returns a :py:class:`~continuedfractions.rational_points.Dim2RationalCoordinates` object, which is a simple custom :py:class:`tuple` type for 2D rational coordinates, which can also be used to access the rational point coordinates:

.. code:: python

   >>> P = RP(F(3, 5), F(4, 5))
   >>> P.coordinates.x
   ContinuedFraction(3, 5)
   >>> P.coordinates.y
   ContinuedFraction(4, 5)

As a subtype of :py:class:`tuple` the :py:class:`~continuedfractions.rational_points.RationalPoint` instances satisfy all tuple properties and operations except for the concatenation operation ``+`` which is reserved for :py:class:`~continuedfractions.rational_points.RationalPoint` instances only:

.. code:: python

   >>> RP(F(1, 2), 3) + (4, 5)
   ...
   TypeError: Addition is defined only between two `RationalPoint` instances.

.. _rational-points.rational-ops:

Rational Operations
-------------------

The rational operations for :py:class:`~continuedfractions.rational_points.RationalPoint` objects have been implemented to be consistent with :math:`\mathbb{Q}^2` forming a (:math:`2`-dimensional) vector space over :math:`\mathbb{Q}`, and include (i) component-wise addition and subtraction, (ii) negation, and (iii) scalar left-multiplication :math:`(\lambda, r) \longmapsto \lambda P` of rational points :math:`P` by rationals :math:`\lambda \in \mathbb{Q}` (the latter meaning in practice that scalars can be any instances of type :py:class:`numbers.Rational`).

Some examples are given below.

.. code:: python

   >>> P, Q = RP(F(1, 2), F(3, 5)), RP(-2, F(9, 10))
   >>> P
   RationalPoint(1/2, 3/5)
   >>> Q
   RationalPoint(-2, 9/10)
   >>> P + Q
   >>> RationalPoint(-3/2, 3/2)
   >>> 2 * P
   RationalPoint(1, 6/5)
   >>> 3 * Q
   RationalPoint(-6, 27/10)
   >>> 2 * P + 3 * Q
   RationalPoint(-5, 39/10)
   >>> P - Q
   RationalPoint(5/2, -3/10)
   >>> -Q
   RationalPoint(2, -9/10)
   >>> assert P - Q == -Q + P
   # True

Consistent with :math:`\mathbb{Q}^2` being an Abelian group the addition, subtraction, negation, and rational scalar mutiplication operations always produce :py:class:`~continuedfractions.rational_points.RationalPoint` instances. The zero element (the additive identity in :math:`\mathbb{Q}^2` and also the origin of :math:`\mathbb{Q}^2` as a vector space) is represented by the value ``RationalPoint(0, 0)``, as can easily be verified. In particular, addition and subtraction are limited to  :py:class:`~continuedfractions.rational_points.RationalPoint` instances, and raise a :py:class:`TypeError` if any other types are attempted, while 
multiplication is limited to left-multiplication by instances of type :py:class:`int`, :py:class:`~fractions.Fraction` or :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`. Multiplication can take the form of scalar left-multiplication, and its inverse operation, (non-zero) scalar division (by non-zero instances of :py:class:`int`, :py:class:`~fractions.Fraction`, or :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`, is also supported:

.. code:: python

   >>> 2 * RP(F(1, 2), 2)
   >>> RationalPoint(1, 4)
   >>> RP(F(1, 2), 2) * 2
   ...
   NotImplementedError: Only rational scalar left-multiplication is supported. This means the left-most operand must be an instance of `numbers.Rational`, i.e. an `int`, `fractions.Fraction` or `ContinuedFraction`.
   >>> P, Q = RP(F(3, 5), F(4, 5)), RP(F(5, 13), F(12, 13)); P, Q
   (RationalPoint(3/5, 4/5), RationalPoint(5/13, 12/13))
   >>> (P + Q) / 2
   RationalPoint(32/65, 56/65) 

In relation to addition, specifically, there is a :py:meth:`~continuedfractions.rational_points.RationalPoint.sum` method, which supports variadic addition of rational points:

.. code:: python

   >>> RP.sum(RP(0, 0), RP(1, F(-1, 2), RP(F(3, 5, F(4, 5)), RP(F(5, 12), 6))))
   RationalPoint(121/60, 63/10)

This should be the preferred method as the Python built-in :py:func:`sum` function sets an internal :py:class:`int` start value of ``0``, which causes it to fail on :py:class:`~continuedfractions.rational_points.RationalPoint` instances.

.. _rational-points.plane-geometry:

Simple Plane Geometry: Properties and Methods
---------------------------------------------

While this is not intended to be a comprehensive library for 2D linear algebra, some basic functionality for treating rational points as (position) vectors of :math:`\mathbb{Q}^2` exists in the form of simple properties and methods, such as gradients, collinearity, angles, dot products, determinants, norms, straight-line distances, and perpendicular distances in relation to other rational points. And some simple linear transformations such as scaling, counter-clockwise rotation through :math:`90` degrees, permuting coordinates are available, in addition to the affine transformation of translation in coordinates.

Norms and distances are discussed :ref:`here <rational-points.euclidean-metrics>` and, in relation to the rectilinear norm, :ref:`here <rational-points.rectilinear-metrics>`.

.. _rational-points.gradients:

Gradients
~~~~~~~~~

Gradients (or slopes) of lines connecting rational points with either the origin :math:`(0, 0)` or other rational points can be computed with the :py:meth:`~continuedfractions.rational_points.RationalPoint.gradient` method. Some examples are given below:

.. code:: python

   >>> RP(1, 1).gradient()
   ContinuedFraction(1, 1)
   >>> RP(1, 1).gradient(other=RP(0, 1))
   ContinuedFraction(0, 1)
   >>> RP(1, 1).gradient(other=RP(2, F(3, 2)))
   ContinuedFraction(1, 2)
   >>> RP(1, 1).gradient(other=RP(2, 3))
   ContinuedFraction(2, 1)
   >>> RP(0, 1).gradient(other=RP(1, 0))
   ContinuedFraction(-1, 1)

The second rational point is optional, but if one is provided it must be a :py:class:`~continuedfractions.rational_points.RationalPoint` instance, otherwise a :py:class:`ValueError` is raised. This is also the case for vertical lines where the gradient is infinite:

.. code:: python

   >>> RP(1, 1).gradient(1, 0)
   ...
   ValueError: If a second rational point is provided, it must be a `RationalPoint` instance, and non-vertical with respect to this point.

.. _rational-points.collinearity:

Collinearity
~~~~~~~~~~~~

Collinearity of a rational point with other points - whether they all fall on a single line in the plane - can be determined with the :py:meth:`~continuedfractions.rational_points.RationalPoint.collinear_with` method. This accepts a variable number of :py:class:`~continuedfractions.rational_points.RationalPoint` instances, given in any order, with which to test collinearity with the original rational point. Some examples are given below:

.. code:: python

   >>> RP(1, 1).collinear_with(RP(2, 2), RP(F(-1, 2), F(-1, 2)), RP(1000, 1000))
   True
   >>> RP(1, 1).collinear_with(RP(2, 2), RP(F(-1, 2), F(-1, 2)), RP(1000, -1000))
   False

The trivial case of a single other rational point is also accepted despite the fact any two points are trivially collinear. Note that :py:meth:`~continuedfractions.rational_points.RationalPoint.collinear_with` is variadic, i.e. accepts a variable number of arguments. If checking for collinearity with an iterable of points the unpacking operator ``*`` should be used.

The :py:meth:`~continuedfractions.rational_points.RationalPoint.collinear_with_origin` method is a variant which checks for the collinearity of the given point with other rational points and also the origin :math:`(0, 0)`:

.. code:: python

   >>> RP(1, 1).collinear_with_origin(RP(2, 2), RP(F(-1, 2), F(-1, 2)), RP(1000, 1000)))
   True
   >>> RP(1, 2).collinear_with_origin(RP(2, 4), RP(F(-1, 2), -1), RP(1000, -1000))
   False

The basic collinearity test, which uses the simple gradient method, relies on the transitivity of collinearity on triples of plane points, so that if a point :math:`P` is collinear with points :math:`Q, R, S` then it is collinear with the pairs :math:`Q, R` and :math:`R, S`: if the either of the latter conditions isn't met then :math:`P, Q, R, S` cannot be collinear.

.. _rational-points.angles:

Angles
~~~~~~

Angles of position vectors of rational points, both in radians (default) and degrees, either with respect to the :math:`x`-axis, or to other rational points, can be taken with the :py:meth:`~continuedfractions.rational_points.RationalPoint.angle` method. Below are examples of the first kind:

.. code:: python

   # Radian angle between the position vector of a given rational point and the positive `x`-axis
   >>> RP(1, 0).angle()
   Decimal('0')
   >>> RP(0, 1).angle()
   Decimal('1.5707963267948965579989817342720925807952880859375')
   >>> RP(-1, 0).angle()
   Decimal('3.141592653589793115997963468544185161590576171875')

where the implementation is based on :py:func:`math.atan2`, which respects angle signs in all four quadrants of the plane in computing :math:`\text{arctan}\left(\frac{y}{x}\right)` for a plane point :math:`P = (x, y)` and returns a value in the interval :math:`(-\pi, \pi]`.

Below are examples of the second kind (angles between position vectors of two rational points):

.. code:: python

   # Radian angles between the position vectors of two rational points
   >>> RP(1, 1).angle(other=RP(0, 1)).angle()
   Decimal('0.78539816339744827899949086713604629039764404296875')
   >>> RP(1, 1).angle(other=RP(-1, 1)).angle()
   Decimal('1.5707963267948965579989817342720925807952880859375')

where the implementation is based on :py:func:`math.acos` and uses the standard formula :math:`\text{cos }\alpha = \frac{P \cdot P'}{\|P\\|\|P'\|}` for the angle :math:`\alpha` between the position vectors of two plane points :math:`P, P'`.

By default :py:meth:`~continuedfractions.rational_points.RationalPoint.angle` returns radian angles. For degrees the ``as_degrees=True`` option can be used:

.. code:: python

   >>> RP(1, 0).angle(as_degrees=True)
   Decimal('0')
   >>> RP(0, 1).angle(as_degrees=True)
   Decimal('90')
   >>> RP(-1, 0).angle(as_degrees=True)
   Decimal('180')
   >>> RP(1, 1).angle(other=RP(-1, 1), as_degrees=True)
   Decimal('90')

.. _rational-points.scaling:

Scaling
~~~~~~~

Scaling by rational values (via scalar left-multiplication), :math:`\left(\lambda, \left(\frac{a}{c}, \frac{b}{d}\right) \right) \longmapsto \left(\lambda\frac{a}{c}, \lambda\frac{b}{d}\right)`, is available via :py:meth:`~continuedfractions.rational_points.RationalTuple.scale` method (in the superclass :py:class:`~continuedfractions.rational_points.RationalTuple`):

.. code:: python

   >>> RP(F(1, 2), F(3, 4)).scale(2)
   RationalPoint(1, 3/2)
   >>> RP(F(5, 4), F(-6, 11)).scale(F(-1, 2))
   RationalPoint(-5/8, 3/11)
   >>> RP(F(1, 2), F(3, 4)).scale(0)
   RationalPoint(0, 0)

.. _rational-points.products:

Products
~~~~~~~~
Certain scalar-valued products, as ordinarily defined, can be taken for pairs of rational points :math:`P = \left(\frac{a}{c}, \frac{b}{d}\right)`, :math:`P' = \left(\frac{a'}{c'}, \frac{b'}{d'}\right) \in \mathbb{Q}^2`, including :py:meth:`~continuedfractions.rational_points.RationalPoint.dot`, which implements the dot product :math:`P \cdot P' = \frac{aa'}{cc'} + \frac{bb'}{dd'}`:

.. code:: python

   >>> RP(1, 1).dot(RP(-1, 1))
   ContinuedFraction(0, 1)
   >>> RP(1, 1).dot(RP(1, 1))
   ContinuedFraction(2, 1)
   >>> RP(1, 1).dot(RP(F(3, 5), F(4, 5)))
   ContinuedFraction(7, 5)

and :py:meth:`~continuedfractions.rational_points.RationalPoint.det` which implements the determinant :math:`\text{Det}(P, P') = \begin{vmatrix}\frac{a}{c} & \frac{a'}{c'}\\ \frac{b}{d} & \frac{b'}{d'}\end{vmatrix} = \frac{ab'}{cd'} - \frac{a'b}{c'd} = \frac{ab'c'd - a'bcd'}{cc'dd'}`:

.. code:: python

   >>> RP(1, 1).det(RP(-1, 1))
   ContinuedFraction(2, 1)
   >>> RP(1, 0).det(RP(0, 1))
   ContinuedFraction(1, 1)
   >>> RP(1, 0).det(RP(1, 0))
   ContinuedFraction(0, 1)

.. _rational-points.other-transformations:

Other Transformations
~~~~~~~~~~~~~~~~~~~~~

A few simple transformations are available, including :py:meth:`~continuedfractions.rational_points.RationalPoint.orthogonal`, which sends a point :math:`P = \left(\frac{a}{c}, \frac{b}{d}\right) \in \mathbb{Q}^2` to a point :math:`P^{\perp} = \left(-\frac{b}{d}, \frac{a}{c}\right)` whose vector is perpendicular to that of :math:`P`:

.. code:: python

   >>> RP(F(1, 2), F(3, 4)).orthogonal()
   RationalPoint(-3/4, 1/2)
   >>> RP(1, -2).orthogonal()
   RationalPoint(2, 1)

This is the linear transformation that rotates the vector of :math:`P` through :math:`90` degrees counter-clockwise, and is described by the matrix :math:`\begin{bmatrix}0 & -1 \\1 & 0 \end{bmatrix}`: it has the property that :math:`P \cdot P^{\perp} = P^{\perp} \cdot P = 0`:

.. code:: python

   >>> RP(1, 1).angle(as_degrees=True)
   Decimal('45')
   >>> RP(1, 1).orthogonal().angle(as_degrees=True)
   Decimal('135')

Basis permutation is available via :py:meth:`~continuedfractions.rational_points.RationalPoint.permute`:

.. code:: python

   >>> RP(F(1, 2), F(3, 4)).permute()
   RationalPoint(3/4, 1/2)

This swaps the coordinates and is a linear transformation described by the matrix :math:`\begin{bmatrix}0 & 1 \\1 & 0 \end{bmatrix}`.

Translation in coordinates is available via :py:meth:`~continuedfractions.rational_points.RationalPoint.translate`:

.. code:: python

   >>> RP(F(-1, 2), F(3, 4)).translate(x_by=F(-1, 4), y_by=F(1, 2))
   RationalPoint(-3/4, 7/4)
   >>> RP(1, 2).translate()
   RationalPoint(1, 2)

This uses two optional arguments (``x_by`` and ``y_by``) both set to ``0`` defaults for the translation in :math:`x`- and/or :math:`y`-coordinates.

Points may be reflected in either axis (:math:`x`- or :math:`y`-) with :py:meth:`~continuedfractions.rational_points.RationalPoint.reflect`:

.. code:: python

   >>> RP(1, 1).reflect(axis='x')
   RationalPoint(1, -1)
   >>> RP(1, 1).reflect(axis='y')
   RationalPoint(-1, 1)

These are linear transformations described by the matrices :math:`\begin{bmatrix}1 & 0\\0 & -1\end{bmatrix}`, and :math:`\begin{bmatrix}-1 & 0\\0 & 1\end{bmatrix}` respectively.

Other transformations may be added in the future.

.. _rational-points.metrics:

Metric Properties and Operations
--------------------------------

Viewing :math:`\mathbb{Q}^2` as a vector subspace of :math:`\mathbb{R}^2`, with its natural Euclidean topology, a number of metric properties and operations are provided for :py:class:`~continuedfractions.rational_points.RationalPoint` objects including (i) Euclidean norm (:math:`\ell_2`) and norm squared, (ii) Euclidean distance and distance squared, and (iii) rectilinear (or :math:`\ell_1`) norm and distance. These are described below in more detail.

.. _rational-points.euclidean-metrics:

Euclidean Norm and Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Euclidean, i.e. straight-line, norm properties for a rational point :math:`P = \left(\frac{a}{c},\frac{b}{d}\right)` include :py:attr:`~continuedfractions.rational_points.RationalPoint.norm_squared`, which implements :math:`\|P\|_{2}^2 = \left(\frac{a}{c}\right)^2 + \left(\frac{b}{d}\right)^2 = \frac{a^2}{c^2} + \frac{b^2}{d^2}`, the rational-valued square of the norm proper, and returns a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` value, while :py:attr:`~continuedfractions.rational_points.RationalPoint.norm`, returns the actual norm :math:`\|P\|_2 = \sqrt{\frac{a^2}{c^2} + \frac{b^2}{d^2}}` as a :py:class:`~decimal.Decimal` value.

Some examples are given below of these.

.. code:: python

   >>> RP(1, 1).norm_squared
   ContinuedFraction(2, 1)
   >>> RP(1, 1).norm
   >>> Decimal('1.414213562373095048801688724')
   >>> RP(F(3, 5), F(4, 5)).norm_squared
   ContinuedFraction(1, 1)
   >>> RP(F(3, 5), F(4, 5)).norm
   Decimal('1')

The ``RP(1, 1)`` examples involve the rational point :math:`(1, 1)` whose Euclidean norm is :math:`\sqrt{2}`, while the ``RP(F(3, 5), F(4, 5))`` examples involve the unit circle rational point :math:`\left(\frac{3}{5},\frac{4}{5}\right)` of norm :math:`1`. An alternative way to calculate Euclidean norm for :py:class:`~continuedfractions.rational_points.RationalPoint` objects is to call on the :py:func:`abs` built-in:

.. code:: python

   >>> abs(RP(0, 0))
   Decimal('0')
   >>> abs(RP(1, 1))
   Decimal('1.414213562373095048801688724')
   >>> abs(RP(F(3, 5), F(4, 5)))
   Decimal('1')

The rational points of unit norm lie on the unit circle :math:`C_1: x^2 + y^2 = 1`, and this can be checked simply by checking the norm squared:

.. code:: python

   >>> assert RP(1, 0).norm_squared == 1
   True
   >>> assert RP(0, 1).norm_squared == 1
   True
   >>> assert RP(F(3, 5), F(4, 5)).norm_squared == 1
   True
   >>> assert RP(1, 1).norm_squared == 1
   ...
   AssertionError:

The Euclidean distance operations for two rational points :math:`P = \left(\frac{a}{c},\frac{b}{d}\right)` and :math:`P' = \left(\frac{a'}{c'},\frac{b'}{d'}\right)` include :py:meth:`~continuedfractions.rational_points.RationalPoint.distance_squared`, which implements :math:`\|P - P'\|_{2}^2 = \left(\frac{a}{c} - \frac{a'}{c'}\right)^2 + \left(\frac{b}{d} - \frac{b'}{d'}\right)^2 = \frac{(ac' - a'c)^2}{(cc')^2} + \frac{(bd' - b'd)^2}{(dd')^2}`, the rational-valued square of the distance proper, and returns a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` value, while :py:meth:`~continuedfractions.rational_points.RationalPoint.distance`, returns the actual distance :math:`\|P - P'\|_2 = \sqrt{\left(\frac{a}{c} - \frac{a'}{c'}\right)^2 + \left(\frac{b}{d} - \frac{b'}{d'}\right)^2} = \sqrt{\frac{(ac' - a'c)^2}{(cc')^2} + \frac{(bd' - b'd)^2}{(dd')^2}}` as a :py:class:`~decimal.Decimal` value. 

Some examples of these are also given below.

.. code:: python

   >>> RP(1, 1).distance_squared(RP(0, 0))
   ContinuedFraction(2, 1)
   >>> RP(1, 1).distance(RP(0, 0))
   Decimal('1.414213562373095048801688724')
   >>> RP(1, 1).distance_squared(RP(F(3, 5), F(4, 5)))
   ContinuedFraction(1, 5)
   >>> RP(1, 1).distance(RP(F(3, 5), F(4, 5)))
   Decimal('0.4472135954999579392818347337')

Note that ``RP(1, 1).distance(RP(0, 0))`` is the :py:class:`~decimal.Decimal` value of :math:`\sqrt{2} = \|(1, 1) - (0, 0)\|_2`, while ``RP(1, 1).distance(RP(F(3, 5), F(4, 5)))`` is the :py:class:`~decimal.Decimal` value of :math:`\frac{1}{\sqrt{5}} = \|\left(1, 1\right) - \left(\frac{3}{5},\frac{4}{5}\right)\|_2`.

It is also possible to compute the perpendicular (or orthogonal) distance :math:`d^{\perp}\left(P, P'\right)` between a (non-zero) rational point :math:`P`, or more precisely, the line passing through the origin :math:`(0, 0)` and :math:`P`, denoted by :math:`\ell_{OP}`, and another rational point :math:`P'`, using the :py:meth:`~continuedfractions.rational_points.RationalPoint.perpendicular_distance` method:

.. code:: python

   >>> RP(1, 0).perpendicular_distance(RP(0, 1))
   Decimal('1')
   >>> RP(0, 1).perpendicular_distance(RP(1, 0))
   Decimal('1')
   >>> RP(1, 0).perpendicular_distance(RP(1, 0))
   Decimal('0')
   >>> RP(F(1, 2), F(1, 2)).perpendicular_distance(RP(0, 1))
   Decimal('0.7071067811865475244008443621')

The method returns a :py:class:`~decimal.Decimal` value for the perpendicular distance between the point :math:`P` represented by the object on which the method is called, and another rational point :math:`P'`, which is the point represented by the argument to the method. This is computed using a formula for the length of the straight-line segment connecting :math:`P'` with line :math:`\ell_{OP}`, which is perpendicular to the latter, given by :math:`d^{\perp}\left(P, P'\right) = \frac{|\text{det}(P, P')|}{\|P\|_2}`, where :math:`\text{det}(P, P')` is the determinant :math:`|x'y - xy'|` and :math:`P = (x, y), P' = (x', y')`. Note that :math:`d^{\perp}\left(P, P'\right)` is not necessarily equal to :math:`d^{\perp}\left(P', P\right)`, is undefined if :math:`P = (0, 0)`, and equal to :math:`0` if :math:`P` and :math:`P'` coincide or, more generally, if they are collinear with the origin.

.. _rational-points.rectilinear-metrics:

Rectilinear Norm and Distance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The rectilinear (or :math:`\ell_1`) norm, also called the taxicab norm, :math:`\|P\|_1` of a rational point :math:`P = \left(\frac{a}{c}, \frac{b}{d}\right)` is defined as the sum of the coordinate lengths, :math:`\lvert\frac{a}{b}\rvert + \lvert\frac{b}{d}\rvert`, and represents the shortest path from the origin :math:`(0, 0)` to the point :math:`P` with steps which are straight-line segments parallel to one of the coordinate axes. This is implemented by the :py:attr:`~continuedfractions.rational_points.RationalPoint.rectilinear_norm` property. It is thus always a rational number, and is returned as a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` value.

The rectilinear distance, also called the taxicab distance, :math:`\|P - P'\|_1` of two rational points :math:`P = \left(\frac{a}{c}, \frac{b}{d}\right)` and :math:`P' = \left(\frac{a'}{c'}, \frac{b'}{d'}\right)` is defined as the sum of the absolute values of the differences in coordinate lengths, :math:`\lvert \frac{ac' - a'c}{cc'} \rvert + \lvert \frac{bd' - b'd}{dd'} \rvert`, and represents the shortest path from the point :math:`P` to the point :math:`P'` with steps which are straight-line segments parallel to the coordinate axes. This is implemented by the :py:meth:`~continuedfractions.rational_points.RationalPoint.rectilinear_distance` method. It is also always a rational number, and is returned as a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` value.

Some examples are given below of both of these.

.. code:: python

   >>> RP(1, 1).rectilinear_norm
   ContinuedFraction(2, 1)
   >>> RP(F(1, 2), F(3, 5)).rectilinear_norm
   ContinuedFraction(11, 10)
   >>> RP(1, 1).rectilinear_distance(RP(F(1, 2), F(3, 5)))
   ContinuedFraction(9, 10)

.. _rational-points.heights:

Height Functions
----------------

The :py:class:`~continuedfractions.rational_points.RationalPoint` provides some basic methods relating to the notion of heights of points in the setting of projective space :math:`\mathbb{P}^2(\mathbb{Q})`, a subset of which can be identified with rational points in the plane. These methods and the basic background theory are described in more detail below.

.. _rational-points.homogeneous-coordinates:

Homogeneous Coordinates
~~~~~~~~~~~~~~~~~~~~~~~

The :py:attr:`~continuedfractions.rational_points.RationalPoint.homogeneous_coordinates` property provides a way to get a sequence of integer-valued homogeneous coordinates for rational points in projective space :math:`\mathbb{P}^2(\mathbb{Q}) = \frac{\mathbb{Q}^3 \setminus \{(0, 0, 0)\}}{\sim}`, where :math:`\sim` is the (non-zero) scalar multiple equivalence relation on non-zero rational number triples, e.g. :math:`\left(3, 4, 6\right)` is a scalar multiple :math:`6 \cdot \left(\frac{1}{2},\frac{2}{3},1\right)` of :math:`\left(\frac{1}{2},\frac{2}{3},1\right)`, while :math:`(3, 4, 5)` isn't: instead :math:`(3, 4, 5)` is a scalar multiple :math:`5 \cdot \left(\frac{3}{5}, \frac{4}{5}, 1\right)` of :math:`\left(\frac{3}{5}, \frac{4}{5}, 1\right)`.

Some examples are given below:

.. code:: python

   >>> RP(0, 0).homogeneous_coordinates
   HomogeneousCoordinates(0, 0, 1)
   >>> RP(1, 1).homogeneous_coordinates
   HomogeneousCoordinates(1, 1, 1)
   >>> RP(-1, 1).homogeneous_coordinates
   HomogeneousCoordinates(-1, 1, 1)
   >>> RP(F(3, 5), F(4, 5)).homogeneous_coordinates
   HomogeneousCoordinates(3, 4, 5)
   >>> RP(F(5, 13), F(12, 13)).homogeneous_coordinates
   HomogeneousCoordinates(5, 12, 13)
   >>> RP(F(6, 10), F(8, 10)).homogeneous_coordinates
   HomogeneousCoordinates(3, 4, 5)
   >>> RP(F(1, 2), F(2, 3)).homogeneous_coordinates
   HomogeneousCoordinates(3, 4, 6)

The examples involving ``RP(F(3, 5), F(4, 5))`` and ``RP(F(5, 13), F(12, 13))`` yield the primitive Pythagorean triples :math:`(3, 4, 5)` and :math:`(5, 12, 13)` respectively because the underlying rational points :math:`\left(\frac{3}{5},\frac{4}{5}\right)` and :math:`\left(\frac{5}{13},\frac{12}{13}\right)` fall on the unit circle :math:`x^2 + y^2 = 1` and have numerators which are coprime. The example with ``RP(F(6, 10), F(8, 10))`` yields the non-primitive Pythagorean triple :math:`(6, 8, 10)` which happens to be a scalar multiple :math:`2\cdot(3, 4, 5)` of :math:`(3, 4, 5)`, but both are homogeneous coordinates for the same rational point :math:`\left(\frac{3}{5},\frac{4}{5}\right)`.

The return value of :py:attr:`~continuedfractions.rational_points.RationalPoint.homogeneous_coordinates` is a :py:class:`~continuedfractions.rational_points.HomogeneousCoordinates` object, which is a simple :py:class:`tuple`-based wrapper for homogenous 3D rational coordinates: the individual components can be accessed from the object using descriptive labels, the coordinates can be scaled and re-scaled any number of times, and the original rational point can be recovered from the coordinates using the :py:meth:`~continuedfractions.rational_points.HomogeneousCoordinates.to_rational_point`, as the examples below demonstrate:

.. code:: python

   >>> P = RP(F(3, 5), F(4, 5)); P
   RationalPoint(3/5, 4/5)
   >>> P.homogeneous_coordinates
   HomogeneousCoordinates(3, 4, 5)
   >>> P.homogeneous_coordinates.x, P.homogeneous_coordinates.y, P.homogeneous_coordinates.z
   (3, 4, 5)
   >>> P.homogeneous_coordinates.scale(2)
   HomogeneousCoordinates(6, 8, 10)
   >>> P.homogeneous_coordinates.scale(2).scale(F(1, 2))
   HomogeneousCoordinates(3, 4, 5)
   >>> hcoords = P.homogeneous_coordinates.scale(2)
   >>> hcoords
   HomogeneousCoordinates(6, 8, 10)
   >>> hcoords.to_rational_point()
   RationalPoint(3/5, 4/5)

For more background on homogeneous coordinates users can refer to textbooks on algebraic geometry. With respect to rational points in the plane, the basic idea is that they can be identified with certain "points" of :math:`\mathbb{P}^2(\mathbb{Q})` which happen to be equivalence classes of type :math:`\left[\frac{a}{c}: \frac{b}{d}: 1\right]` (for :math:`\frac{a}{c}, \frac{b}{d} \in \mathbb{Q}`) under :math:`\sim` (the scalar multiple equivalence relation described above): the mapping :math:`\left(\frac{a}{c}, \frac{b}{d}\right) \longmapsto \left[\frac{a}{c}: \frac{b}{d}: 1\right]` is a bijection from :math:`\mathbb{Q}^2` into :math:`\mathbb{P}^2(\mathbb{Q})`, and for a given rational point :math:`P = \left(\frac{a}{c}, \frac{b}{d}\right)` the elements of its image :math:`\left[\frac{a}{c}: \frac{b}{d}: 1\right]`, under this mapping, are non-zero scalar multiples of each other and are called homogeneous coordinates for :math:`P` in :math:`\mathbb{P}^2(\mathbb{Q})`. In particular, :math:`\left(\lambda\frac{a}{c}, \lambda\frac{b}{d}, \lambda \right)` is a scalar multiple of :math:`\left( \frac{a}{c}, \frac{b}{d}, 1 \right)`, where :math:`\lambda = \text{lcm}(c, d) > 0`, and can be taken as a representative sequence of homogeneous coordinates for :math:`P`.

:py:attr:`~continuedfractions.rational_points.RationalPoint.homogeneous_coordinates` simply implements the mapping :math:`\left(\frac{a}{c},\frac{b}{d}\right) \longmapsto \left(\lambda \frac{a}{c}, \lambda \frac{b}{d}, \lambda\right)`, where :math:`\left(\lambda \frac{a}{c}, \lambda \frac{b}{d}, \lambda\right)` are integers, as :math:`\left(\lambda \frac{a}{c}, \lambda \frac{b}{d}, \lambda\right) = \left( a\frac{\lambda}{c}, b\frac{\lambda}{d}, \lambda \right)`, and :math:`\text{gcd}\left(a\frac{\lambda}{c}, b\frac{\lambda}{d}, \lambda\right) = \text{gcd}\left(|a|\frac{|d|}{\text{gcd}(c, d)}, |b|\frac{|c|}{\text{gcd}(c, d)}, \frac{|c||d|}{\text{gcd}(c, d)} \right) = 1` (from the relation :math:`\text{lcm}(c, d) = \frac{|c||d|}{\text{gcd}(c, d)}`).

.. _rational-points.heights:

Heights
~~~~~~~

The :py:attr:`~continuedfractions.rational_points.RationalPoint.height` property returns the height :math:`H` of a rational point :math:`P = \left(\frac{a}{c},\frac{b}{d}\right)` as given by:

.. math::

   H(P) = H\left(\frac{a}{c},\frac{b}{d}\right) = \text{max}\left(|a|\lvert \frac{\lambda}{c} \rvert, |b|\lvert \frac{\lambda}{d} \rvert, \lambda \right)

where :math:`\lambda = \text{lcm}(c, d)` and :math:`\left(a\frac{\lambda}{c}, b\frac{\lambda}{d},\lambda \right)` is a unique representative point  of :math:`P` in :math:`\mathbb{P}^2(\mathbb{Q})` (and also a sequence of homogeneous coordinates for :math:`P`), as described above, with the property that :math:`a\frac{\lambda}{c}, b\frac{\lambda}{d},\lambda \in \mathbb{Z} \setminus \{0\}` and :math:`\text{gcd}\left(a\frac{\lambda}{c}, b\frac{\lambda}{d},\lambda\right) = 1`.

Some examples are given below:

.. code:: python

   >>> RP(0, 0).height
   1
   >>> RP(2, F(1, 2)).height
   4
   >>> RP(F(3, 5), F(4, 5)).height
   5
   >>> RP(F(-3, 5), F(4, 5)).height
   5
   >>> RP(F(6, 10), F(8, 10)).height
   5
   >>> RP(F(5, 13), F(12, 13)).height
   13

Derived from this is the :py:attr:`~continuedfractions.rational_points.RationalPoint.log_height` property which yields the (natural, i.e. base :math:`e`) logarithm of the height :math:`H` of a rational point :math:`P` as defined above, that is, :math:`\text{log}\left(H\left(P\right)\right) = \text{log}\left(H\left(\frac{a}{c},\frac{b}{d}\right)\right)`, where :math:`H` is as defined above.

Some examples are given below:

.. code:: python

   >>> RP(0, 0).log_height
   Decimal('0')
   >>> RP(2, F(1, 2)).log_height
   Decimal('1.3862943611198905724535279659903608262538909912109375')
   >>> RP(F(3, 5), F(4, 5)).log_height
   Decimal('1.6094379124341002817999424223671667277812957763671875')
   >>> RP(F(-3, 5), F(4, 5)).log_height
   Decimal('1.6094379124341002817999424223671667277812957763671875')
   >>> RP(F(6, 10), F(8, 10)).log_height
   Decimal('1.6094379124341002817999424223671667277812957763671875')
   >>> RP(F(5, 13), F(12, 13)).log_height
   Decimal('2.564949357461536738611584951286204159259796142578125')

.. _rational-points.integral-lattice-points:

Integral Lattice Points
-----------------------

Integral lattice points, which form an Abelian subgroup of the rational points, aren't currently supported directly by any specific features, but the :py:meth:`~continuedfractions.rational_points.RationalPoint.is_integral_lattice_point` method does provide a way to filter for these:

.. code:: python

   >>> RP(0, 0).is_integral_lattice_point()
   True
   >>> RP(F(1, 2), F(3, 4)).is_integral_lattice_point()
   False

which may be useful when working with a large collection of :py:class:`~continuedfractions.rational_points.RationalPoint` instances.

Support for representing and operating on rational and integral lattices and lattice points may be added in the future. Contributions would be welcome.

.. _rational-points.rational-points-on-curves:

Rational Points on Curves
-------------------------

Rational points on curves forms a large subject that isn't supported directly in any way in the library, which is fairly small and generic in scope. Support may be added in the future for rational points on some well known plane curves, such as the unit circle, unit hyperbola, and possibly some simple elliptic curves also, in the form of class features that allow the group properties of such points to be explored.

.. _rational-points.references:

References
----------

[1] Clader, E., Ross, D. (2025 May). Beginning in Algebraic Geometry. Springer. https://link.springer.com/content/pdf/10.1007/978-3-031-88819-9.pdf

[2] Courant, R., Robbins, H., & Stewart, I. (1996). What is mathematics?: An elementary approach to ideas and methods (2nd ed.). Oxford University Press

[3] Srinivasan, P. (2022). Height Functions in Diophantine Geometry (Lecture 1). https://swc-math.github.io/aws/2023/PAWSSrinivasan/2022PAWSSrinivasanNotes1.pdf 
