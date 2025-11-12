from __future__ import annotations


__all__ = [
    'Dim2RationalCoordinates',
    'Dim3RationalCoordinates',
    'HomogeneousCoordinates',
    'RationalPoint',
    'RationalTuple',
]

# -- IMPORTS --

# -- Standard libraries --
import decimal
import math
import numbers
import typing

from decimal import Decimal
from itertools import pairwise
from typing import Any

# -- 3rd party libraries --

# -- Internal libraries --
from continuedfractions.continuedfraction import Fraction, ContinuedFraction


class RationalTuple(tuple):
    """A rational-valued tuple consisting of one or more :py:class:`numbers.Rational` values.

    The class serves as a generic base for other custom rational-valued tuple
    types defined in this library:

    * :py:class:`~continuedfractions.rational_points.Dim2RationalCoordinates`
    * :py:class:`~continuedfractions.rational_points.Dim3RationalCoordinates`
    * :py:class:`~continuedfractions.rational_points.HomogeneousCoordinates`
    * :py:class:`~continuedfractions.rational_points.RationalPoint`

    It does not contain any mathematical structure. That is left to the other
    custom types listed above.

    Examples
    --------
    >>> from fractions import Fraction as F
    >>> from continuedfractions.continuedfraction import ContinuedFraction as CF
    >>> RationalTuple(F(1, 2), CF(3, 4))
    RationalTuple(1/2, 3/4)
    """
    def __new__(cls, *args: numbers.Rational) -> RationalTuple:
        """Constructor.
        """
        if args is None or any(not isinstance(arg, numbers.Rational) for arg in args):
            raise ValueError(
                'One or more rational-valued arguments are required.'
            )

        return super().__new__(cls, args)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({", ".join(map(str, self))})'

    def scale(self, scalar: numbers.Rational) -> RationalTuple:
        """:py:class:`numbers.Rational` : A new scaled instance of the rational tuple by a rational scalar.
        
        Parameters
        ----------
        scalar : numbers.Rational
            The (rational) scalar with which to scale the rational tuple.

        Returns
        -------
        RationalTuple
            The scaled rational tuple.

        Examples
        --------
        >>> RationalTuple(1, Fraction(-2, 3), ContinuedFraction(4, 5)).scale(15)
        RationalTuple(15, -10, 12)
        >>> RationalTuple(1, Fraction(-2, 3), ContinuedFraction(4, 5)).scale(Fraction(1, 2))
        RationalTuple(1/2, -1/3, 2/5)
        >>> RationalTuple(1, Fraction(-2, 3), ContinuedFraction(4, 5)).scale(ContinuedFraction(-5, 6))
        RationalTuple(-5/6, 5/9, -2/3)
        """
        if not isinstance(scalar, numbers.Rational):
            raise ValueError('A rational scalar is required for scaling.')      # pragma: no cover

        return self.__class__(*(scalar * x for x in self))


class Dim2RationalCoordinates(RationalTuple):
    """A simple :py:class:`tuple` subtype for a sequence of two rational coordinates representing a point in :math:`\\mathbb{Q}^2`.

    Examples
    --------
    >>> from fractions import Fraction as F
    >>> from continuedfractions.continuedfraction import ContinuedFraction as CF
    >>> c = Dim2RationalCoordinates(F(1, 2), F(3, 4))
    >>> c
    Dim2RationalCoordinates(1/2, 3/4)
    >>> c.x
    Fraction(1, 2)
    >>> c.y
    Fraction(3, 4)
    """
    def __new__(cls, x: numbers.Rational, y: numbers.Rational) -> Dim2RationalCoordinates:
        """Constructor.
        """
        return super().__new__(cls, x, y)

    @property
    def x(self) -> numbers.Rational:
        """:py:class:`numbers.Rational` : The ``x``-coordinate.

        Returns
        -------
        numbers.Rational
            The :math:`x`-coordinate.

        Examples
        --------
        >>> Dim2RationalCoordinates(1, Fraction(3, 4)).x
        1
        >>> Dim2RationalCoordinates(Fraction(1, 2), Fraction(3, 4)).x
        Fraction(1, 2)
        >>> Dim2RationalCoordinates(ContinuedFraction(1, 2), Fraction(3, 4)).x
        ContinuedFraction(1, 2)
        """
        return self[0]

    @property
    def y(self) -> numbers.Rational:
        """:py:class:`numbers.Rational` : The ``y``-coordinate.

        Returns
        -------
        numbers.Rational
            The :math:`y`-coordinate.

        Examples
        --------
        >>> Dim2RationalCoordinates(Fraction(1, 2), 3).y
        3
        >>> Dim2RationalCoordinates(Fraction(1, 2), Fraction(3, 4)).y
        Fraction(3, 4)
        >>> Dim2RationalCoordinates(Fraction(1, 2), ContinuedFraction(3, 4)).y
        ContinuedFraction(3, 4)
        """
        return self[1]


class Dim3RationalCoordinates(RationalTuple):
    """A simple :py:class:`tuple` subtype for a sequence of three rational coordinates representing a point in :math:`\\mathbb{Q}^3`.

    Examples
    --------
    >>> from fractions import Fraction as F
    >>> from continuedfractions.continuedfraction import ContinuedFraction as CF
    >>> c = Dim3RationalCoordinates(1, F(-2, 3), CF(4, 5))
    >>> c
    Dim3RationalCoordinates(1, -2/3, 4/5)
    >>> c.x
    1
    >>> c.y
    Fraction(-2, 3)
    >>> c.z
    ContinuedFraction(4, 5)
    """
    def __new__(cls, x: numbers.Rational, y: numbers.Rational, z: numbers.Rational) -> Dim3RationalCoordinates:
        """Constructor.
        """
        return super().__new__(cls, x, y, z)

    @property
    def x(self) -> numbers.Rational:
        """:py:class:`numbers.Rational` : The ``x``-coordinate.

        Returns
        -------
        numbers.Rational
            The :math:`x`-coordinate.

        Examples
        --------
        >>> Dim3RationalCoordinates(1, Fraction(2, 3), ContinuedFraction(3, 4)).x
        1
        >>> Dim3RationalCoordinates(Fraction(1, 2), 3, ContinuedFraction(4, 5)).x
        Fraction(1, 2)
        >>> Dim3RationalCoordinates(ContinuedFraction(1, 2), Fraction(3, 4), 5).x
        ContinuedFraction(1, 2)
        """
        return self[0]

    @property
    def y(self) -> numbers.Rational:
        """:py:class:`numbers.Rational` : The ``y``-coordinate.

        Returns
        -------
        numbers.Rational
            The :math:`y`-coordinate.

        Examples
        --------
        >>> Dim3RationalCoordinates(Fraction(1, 2), 3, ContinuedFraction(4, 5)).y
        3
        >>> Dim3RationalCoordinates(1, Fraction(2, 3), ContinuedFraction(4, 5)).y
        Fraction(2, 3)
        >>> Dim3RationalCoordinates(1, ContinuedFraction(2, 3), Fraction(4, 5)).y
        ContinuedFraction(2, 3)
        """
        return self[1]

    @property
    def z(self) -> numbers.Rational:
        """:py:class:`numbers.Rational` : The ``z``-coordinate.

        Returns
        -------
        numbers.Rational
            The :math:`z`-coordinate.

        Examples
        --------
        >>> Dim3RationalCoordinates(Fraction(1, 2), ContinuedFraction(3, 4), 5).z
        5
        >>> Dim3RationalCoordinates(1, ContinuedFraction(2, 3), Fraction(4, 5)).z
        Fraction(4, 5)
        >>> Dim3RationalCoordinates(1, Fraction(2, 3), ContinuedFraction(4, 5)).z
        ContinuedFraction(4, 5)
        """
        return self[2]


class HomogeneousCoordinates(Dim3RationalCoordinates):
    """A class to represent homogeneous coordinates for rational points in projective space :math:`\\mathbb{P}^2(\\mathbb{Q})`.

    Examples
    --------
    >>> from fractions import Fraction as F
    >>> h = HomogeneousCoordinates(3, 4, 5)
    >>> h = h.scale(F(1, 5))
    >>> h
    HomogeneousCoordinates(3/5, 4/5, 1)
    >>> h.to_rational_point()
    RationalPoint(3/5, 4/5)
    """

    def to_rational_point(self) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Returns a new rational point from this sequence of homogeneous coordinates.

        Returns
        -------
        RationalPoint
            A new rational point from this sequence of homogeneous coordinates.

        Examples
        --------
        >>> HomogeneousCoordinates(3, 4, 5).to_rational_point()
        RationalPoint(3/5, 4/5)
        """
        return RationalPoint(Fraction(self.x, self.z), Fraction(self.y, self.z))


class RationalPoint(Dim2RationalCoordinates):
    """A simple class for representing and operating on rational points as points in the :math:`xy`-plane.

    These are points in :math:`\\mathbb{R}^2` whose coordinates are rational
    i.e. elements of :math:`\\mathbb{Q}`, and thus are points of
    :math:`\\mathbb{Q}^2`.

    The points form an abelian group under component-wise addition, and form a
    closed set under scalar left-multiplication by rational numbers. The scalar
    left-multiplication is distributive over sums of rational points.

    This implemention of rational points is based essentially on a custom
    implementation
    :py:class:`~continuedfractions.rational_points.RationalTuple` of
    :py:class:`tuple`, with exactly two rational-valued members: in Python
    this means the arguments must be instances of
    :py:class:`~numbers.Rational`, which includes values of type:

    * :py:class:`int`
    * :py:class:`~fractions.Fraction`
    * :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`

    Internally, the rational coordinates of the point are stored as
    :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
    objects.

    Examples
    --------
    >>> RationalPoint(Fraction(3, 5), Fraction(4, 5))
    RationalPoint(3/5, 4/5)
    >>> RationalPoint(3, ContinuedFraction(4, 5))
    RationalPoint(3, 4/5)
    >>> RationalPoint(Fraction(3, 5), ContinuedFraction(4))
    RationalPoint(3/5, 4)
    >>> RationalPoint(-3, 4)
    RationalPoint(-3, 4)
    >>> RationalPoint(2, .5)
    Traceback (most recent call last):
    ...
    ValueError: A `RationalPoint` object must be specified as a pair of rational numbers `r` and `s`, each of type either integer (`int`), or fraction (`Fraction` or `ContinuedFraction`).
    """
    def __new__(cls, x: int | Fraction | ContinuedFraction, y: int | Fraction | ContinuedFraction) -> RationalPoint:
        """Constructor.
        """
        if not isinstance(x, (int, Fraction, ContinuedFraction)) or not isinstance(y, (int, Fraction, ContinuedFraction)):
            raise ValueError(
                'A `RationalPoint` object must be specified as a pair of '
                'rational numbers `r` and `s`, each of type either integer '
                '(`int`), or fraction (`Fraction` or `ContinuedFraction`).'
            )

        return super().__new__(cls, ContinuedFraction(x), ContinuedFraction(y))

    @classmethod
    def zero(cls) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : The zero rational point.

        Returns
        -------
        RationalPoint
            The zero rational point.

        Examples
        --------
        >>> RationalPoint.zero()
        RationalPoint(0, 0)
        """
        return cls(0, 0)

    @classmethod
    def sum(cls, *rational_points: RationalPoint) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : The sum of a variable number of rational points.

        This is designed as a helper method for rational point summation
        because the built-in :py:func:`sum` function only works for
        :py:class:`~continuedfractions.rational_points.RationalPoint`
        instances if the ``start`` value is set to ``RP(0, 0)``, which many
        users may not be aware of.

        Parameters
        ----------
        rational_points : typing.Iterable
            A variable number of
            :py:class:`~continuedfractions.rational_points.RationalPoint`
            instances to add.

        Returns
        -------
        RationalPoint
            The sum of the rational points.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP.sum(RP(-1, 1), RP(1, -1))
        RationalPoint(0, 0)
        >>> RP.sum(RP(1, 1), RP(2, 1), RP(3, 1))
        RationalPoint(6, 3)
        >>> RP.sum(RP(0, 0), RP(1, F(-1, 2)), RP(F(3, 5), F(4, 5)), RP(F(5, 12), 6))
        RationalPoint(121/60, 63/10)
        """
        return sum(rational_points, start=cls.zero())

    @property
    def coordinates(self) -> Dim2RationalCoordinates:
        """
        :py:class:`~continuedfractions.rational_points.Dim2RationalCoordinates` : The pair of (rational) coordinates of the rational point.

        Returns
        -------
        tuple
            The pair of coordinates of the rational point as a tuple of
            :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
            instances.

        Examples
        --------
        >>> P = RationalPoint(Fraction(1, 2), Fraction(-3, 4))
        >>> P.coordinates
        Dim2RationalCoordinates(1/2, -3/4)
        """
        return Dim2RationalCoordinates(*self)

    def gradient(self, /, *, other: RationalPoint = None) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : Computes the gradient (slope) of the line passing through this rational point and either the origin :math:`(0, 0)` (default) or another point`.
        
        If no second rational point is provided the gradient of this rational
        point is computed with respect to the origin :math:`(0, 0)`: if this
        rational point has a zero :math:`x`-coordinate, i.e. falls on the
        :math:`y`-axis, then a :py:class:`None` value will be returned, to
        indicate that the result is undefined.

        If another rational point :math:`P' = (x', y')` (as represented by
        ``other``) is provided then the gradient is computed as:

        .. math::

           \\frac{y' - y}{x' - x}, \\hskip{3em} x' \\neq x

        where :math:`P = (x, y)` is this rational point (as represented by
        ``self``).

        If no non-zero second rational point is provided the gradient is
        computed with respect to the origin:

        .. math::

           \\frac{y}{x}, \\hskip{3em} x \\neq 0

        As the gradient of a vertical line is infinite (or undefined) the
        method raises a :py:class:`ValueError`, which occurs whenver the
        second rational point is vertical with respect to this point, i.e.
        the two points have the same :math:`x`-coordinate.

        Parameters
        ----------
        other : RationalPoint, default=None
            An optional second rational point with respect to which the
            gradient is computed.

        Returns
        -------
        ContinuedFraction
            The gradient (slope) of the line connecting this rational point and
            either the origin :math:`(0, 0)` (default) or another point.

        Raises
        ------
        ValueError
            If ``other`` is not a rational point or the point it represents is
            vertical with respect to this rational point.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 1).gradient()
        ContinuedFraction(1, 1)
        >>> RP(1, 1).gradient(other=RP(2, 1))
        ContinuedFraction(0, 1)
        >>> RP(0, 1).gradient(other=RP(1, 0))
        ContinuedFraction(-1, 1)
        >>> RP(0, 1).gradient()
        >>> RP(1, 1).gradient(other=RP(1, 2))
        Traceback (most recent call last):
        ...
        ValueError: If a second rational point is provided, it must be a `RationalPoint` instance, and non-vertical with respect to this point.
        """
        if other is None:
            return ContinuedFraction(self.y, self.x) if self.x != 0 else None

        if not isinstance(other, RationalPoint) or other.x == self.x:
            raise ValueError(
                'If a second rational point is provided, it must be a '
                '`RationalPoint` instance, and non-vertical with respect '
                'to this point.'
            )

        return ContinuedFraction(other.y - self.y, other.x - self.x)

    def collinear_with(self, *rational_points: RationalPoint) -> bool:
        """:py:class:`bool` : Tests whether this rational point is collinear with one or more rational points.

        The collinearity test for three points :math:`P_1 = (x_1, y_1)`,
        :math:`P_2 = (x_2, y_2)`, and :math:`P_3 = (x_3, y_3)` uses the
        gradient method:

        .. math::

           \\frac{y_2 - y_1}{x_2 - x_1} = \\frac{y_3 - y_2}{x_3 - x_2}, \\hskip{3em} x_2 \\neq x_1; x_3 \\neq x_2

        which can be rearranged as the equation:

        .. math::

           (y_3 - y_2)(x_2 - x_1) - (y_2 - y_1)(x_3 - x_2) = 0

        Note that the other rational points do not need to be given in any
        particular order.

        Parameters
        ----------
        rational_points : RationalPoint
            One or more rational points to test for collinearity with this
            point.

        Returns
        -------
        bool
            Whether this point is collinear with the given rational points.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 1).collinear_with(RP(2, 2), RP(F(-1, 2), F(-1, 2)))
        True
        >>> RP(1, 1).collinear_with(RP(2, 2), RP(F(-1, 2), F(-1, 2)), RP(-3, -3))
        True
        >>> RP(1, 1).collinear_with(RP(-2, -2), RP(F(1, 2), F(1, 2)), RP(1, 2))
        False
        >>> RP(1, 1).collinear_with(RP(F(-1, 2), F(-1, 2)))
        True
        >>> RP(1, 1).collinear_with(RP(2, 1))
        True
        """
        if any(not isinstance(P, self.__class__) for P in rational_points):
            raise ValueError(
                'One or more non-`RationalPoint` instances detected. Please '
                'check the inputs and try again.'
            )

        if len(rational_points) == 1:
            return True

        def collinear(P1: RationalPoint, P2: RationalPoint, P3: RationalPoint, /) -> bool:
            """Inner function to test collinearity for exactly three rational points, including this one (``self``).
            """
            if (P1 == P2) or (P1 == P3) or (P2 == P3):
                return True

            x1, y1, x2, y2, x3, y3 = (*P1, *P2, *P3)

            return (y3 - y2) * (x2 - x1) - (y2 - y1) * (x3 - x2) == 0

        for Q, R in pairwise(rational_points):
            if not collinear(self, Q, R):
                return False

        return True

    def collinear_with_origin(self, *rational_points: RationalPoint) -> bool:
        """:py:class:`bool` : Tests whether this rational point is collinear with one or more rational points and the origin :math:`(0, 0)`.

        This is to allow easier checking of collinearity of points falling on a
        line passing through the origin.

        Note that the other rational points do not need to be given in any
        particular order.

        Parameters
        ----------
        rational_points : RationalPoint
            One or more rational points to test for collinearity with this
            point and the origin :math:`(0, 0)`

        Returns
        -------
        bool
            Whether this point is collinear with the given rational points
            and the origin :math:`(0, 0)`.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 1).collinear_with_origin(RP(2, 2), RP(F(-1, 2), F(-1, 2)))
        True
        >>> RP(1, 1).collinear_with_origin(RP(2, 2), RP(F(-1, 2), F(1, 2)))
        False
        >>> RP(1, 0).collinear_with_origin(RP(-1, 0), RP(F(1, 2), F(1, 2)))
        False
        >>> RP(1, 0).collinear_with_origin(RP(-1, 0), RP(F(1, 2), 0))
        True
        """
        if any(not isinstance(P, self.__class__) for P in rational_points):
            raise ValueError(
                'One or more non-`RationalPoint` instances detected. Please '
                'check the inputs and try again.'
            )

        return self.collinear_with(self.zero(), *rational_points)

    def angle(self, /, *, other: RationalPoint = None, as_degrees: bool = False) -> Decimal:
        """:py:class:`~decimal.Decimal`: The radian (or degree) angle between this rational point, as a position vector in :math:`\\mathbb{Q}^2`, and either another rational point or the positive :math:`x`-axis.
        
        If another rational point :math:`P'` (as represented by ``other``) is
        provided, the computed angle is that between the position vector of
        this rational point :math:`P = (x, y)` (as represented by ``self``) and
        the other, as given by:

        .. math::

           \\alpha = \\text{arccos}\\left( \\frac{P \\cdot P'}{\\|P\\|\\|P'\\|} \\right)

        If no other rational point is provided the computed angle is that
        between the position vector of this rational point and the
        positive :math:`x`-axis, as given by:

        .. math::

           \\alpha = \\text{atan2}\\left(\\frac{y}{x}\\right)

        where :math:`\\text{atan2}` refers to the :math:`\\text{arctan}`
        extension that uses both :math:`x`- and :math:`y`-coordinates of a plane point
        :math:`P = (x, y)`, as implemented by :py:func:`math.atan2`. For reference
        any standard book on trigonometry or plane geometry should contain a
        definition.

        The optional ``as_degrees`` boolean can be used to return the angle in
        degrees.

        Parameters
        ----------
        as_degrees : bool, default=False
            Whether to return the angle in degrees.

        Returns
        -------
        decimal.Decimal
           The angle between this rational point, as a
           position vector in :math:`\\mathbb{Q}^2`, and either another
           rational point, if provided, or the positive
           :math:`x`-axis.

        Examples
        --------
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 0).angle()
        Decimal('0')
        >>> RP(1, 0).angle(as_degrees=True)
        Decimal('0')
        >>> RP(1, 1).angle()
        Decimal('0.78539816339744827899949086713604629039764404296875')
        >>> RP(1, 1).angle(as_degrees=True)
        Decimal('45')
        >>> RP(1, 1).angle(other=RP(0, 1))
        Decimal('0.78539816339744827899949086713604629039764404296875')
        >>> RP(1, 1).angle(other=RP(0, 1), as_degrees=True)
        Decimal('45')
        """
        if other and other == self:
            angle = Decimal('0')
        elif other and other != self: 
            angle = Decimal(math.acos(self.dot(other).as_decimal() / (self.norm * other.norm)))
        else:
            angle = Decimal(math.atan2(self.y, self.x))

        if not as_degrees:
            return angle

        return Decimal(math.degrees(angle))

    def orthogonal(self) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Returns a rational point whose position vector is orthogonal to that of the original point.

        This is described by the linear transformation:

        .. math::

           \\begin{bmatrix}0 & -1 \\\\1 & 0 \\end{bmatrix} \\begin{bmatrix}\\frac{a}{c} \\\\\\frac{b}{d}\\end{bmatrix} = \\begin{bmatrix} -\\frac{b}{d} \\\\ \\frac{a}{c} \\end{bmatrix}

        for points
        :math:`P = \\left(\\frac{a}{c}, \\frac{b}{d}\\right) \\in \\mathbb{Q}^2`,
        and has the property that :math:`P \\cdot P^{\\perp} = P^{\\perp} \\cdot P = 0` where
        :math:`\\perp` is the orthogonality relation..

        Returns
        -------
        RationalPoint
            The "orthogonal" of the rational point as defined above.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(F(1, 2), F(3, 4)).orthogonal()
        RationalPoint(-3/4, 1/2)
        >>> RP(1, -2).orthogonal()
        RationalPoint(2, 1)
        >>> RP(1, -2).orthogonal().dot(RP(1, -2))
        ContinuedFraction(0, 1)
        """
        return self.__class__(-self.y, self.x)

    def permute(self) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Returns a new rational point by swapping the original coordinates.

        This is described by the linear transformation:

        .. math::

           \\begin{bmatrix}0 & 1 \\\\1 & 0 \\end{bmatrix} \\begin{bmatrix}\\frac{a}{c} \\\\\\frac{b}{d}\\end{bmatrix} = \\begin{bmatrix} \\frac{b}{d} \\\\ \\frac{a}{c} \\end{bmatrix}

        for points
        :math:`P = \\left(\\frac{a}{c}, \\frac{b}{d}\\right) \\in \\mathbb{Q}^2`.

        Returns
        -------
        RationalPoint
            The permuted rational point with the original coordinates
            swapped.

        Examples
        --------
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 2).permute()
        RationalPoint(2, 1)
        """
        return self.__class__(self.y, self.x)

    def translate(self, /, *, x_by: int | Fraction | ContinuedFraction = 0, y_by: int | Fraction | ContinuedFraction = 0) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Returns a new rational point obtained by translating the original in the :math:`x`- and/or :math:`y`-coordinates by rational scalars.

        An affine transformation which implements the mapping:

        .. math::

           \\left(\\left(\\frac{a}{c},\\frac{b}{d}\\right), \\lambda, \\mu\\right) \\longmapsto \\left(\\frac{a}{c} + \\lambda, \\frac{b}{d} + \\mu\\right)

        for rational points :math:`\\left(\\frac{a}{c}, \\frac{b}{d}\\right) \\in \\mathbb{Q}^2`
        and rational scalars :math:`\\lambda, \\mu \\in \\mathbb{Q}`.

        This will not be a linear transformation as the origin :math:`(0, 0)` of
        :math:`\\mathbb{Q}^2` wil be moved for any non-zero scalars.

        Parameters
        ----------
        x_by : int or Fraction or ContinuedFraction, default=0
            The optional parameter for translating the :math:`x`-coordinate,
            with a default value of :math:`0`. Must be a rational value.

        y_by : int or Fraction or ContinuedFraction, default=0
            The optional parameter for translating the :math:`y`-coordinate,
            with a default value of :math:`0`. Must be a rational value.

        Returns
        -------
        RationalPoint
            A new rational point translated from the original using the given
            coordinate translation parameters.

        Raises
        ------
        ValueError
            If the coordinate translation parameters are not of the expected
            type.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> P = RP(F(1, 2), F(-3, 4)); P
        RationalPoint(1/2, -3/4)
        >>> P.translate(x_by=F(-1, 4), y_by=2)
        RationalPoint(1/4, 5/4)
        >>> P.translate(x_by=-.5)
        Traceback (most recent call last):
        ...
        ValueError: The coordinate translation parameters must be of type `int`, `fractions.Fraction` or `ContinuedFraction`.
        """
        if not (isinstance(x_by, (int, Fraction, ContinuedFraction)) and isinstance(y_by, (int, Fraction, ContinuedFraction))):
            raise ValueError(
                'The coordinate translation parameters must be of type `int`, '
                '`fractions.Fraction` or `ContinuedFraction`.'
            )

        return self.__class__(self.x + x_by, self.y + y_by)

    def reflect(self, axis: typing.Literal['x', 'y']) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Returns a new rational point obtained by reflecting the original in the :math:`x`- or :math:`y`-axis.

        Implements linear transformations given by the mappings:

        .. math::

           \\left(\\frac{a}{c}, \\frac{b}{d} \\right) \\longmapsto \\left(\\frac{a}{c}, -\\frac{b}{d}\\right)

        for reflection in the :math:`x`-axis, and:

        .. math::

           \\left(\\frac{a}{c}, \\frac{b}{d} \\right) \\longmapsto \\left(-\\frac{a}{c}, \\frac{b}{d}\\right)

        for reflection in the :math:`y`-axis, with matrices
        :math:`\\begin{bmatrix}1 & 0\\\\0 & -1\\end{bmatrix}`, and
        :math:`\\begin{bmatrix}-1 & 0\\\\0 & 1\\end{bmatrix}` respectively.

        Parameters
        ----------
        axis : str
            The axis of reflection: should be a string literal which is either
            ``"x"`` or ``"y"``.

        Returns
        -------
        RationalPoint
            A new rational point reflected from the original in the given axis.

        Raises
        ------
        ValueError
            If the axis is invalid or incorrectly specified.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> P = RP(1, 1)
        >>> P.reflect(axis='x')
        RationalPoint(1, -1)
        >>> P.reflect(axis='y')
        RationalPoint(-1, 1)
        >>> P.reflect(axis="X")
        Traceback (most recent call last):
        ...
        ValueError: The axis of reflection must be a string literal which is either "x" or "y".
        """
        if not (isinstance(axis, str) and axis in ['x', 'y']):
            raise ValueError(
                'The axis of reflection must be a string literal which is '
                'either "x" or "y".'
            )

        return self.__class__(self.x, -self.y) if axis == 'x' else self.__class__(-self.x, self.y)

    def dot(self, other: RationalPoint, /) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : The dot product of two rational points as position vectors in :math:`\\mathbb{Q}^2`.

        If :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` and
        :math:`P'  = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)` are two
        rational points in the plane their dot product :math:`P \\cdot P'` is
        the rational number:

        .. math::
        
           \\begin{align}
           P \\cdot P' &= \\frac{aa'}{cc'} + \\frac{bb'}{dd'} \\\\
                       &= \\frac{aa'dd' + bb'cc'}{cc'dd'}        
           \\end{align}

        This value is returned as a 
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
        object because this is the standard representation of rational numbers
        in this package.

        Returns
        -------
        ContinuedFraction
            The standard Euclidean dot product for two rational points in the
            plane.

        Examples
        --------
        >>> P = RationalPoint(Fraction(1, 2), Fraction(3, 4))
        >>> Q = RationalPoint(Fraction(1, 3), Fraction(2, 5))
        >>> P.dot(Q)
        ContinuedFraction(7, 15)
        >>> P.dot(2)
        Traceback (most recent call last):
        ...
        ValueError: The dot product is only defined between `RationalPoint` instances.
        >>> P.dot(RationalPoint(0, 0))
        ContinuedFraction(0, 1)
        >>> P.dot(RationalPoint(1, 1))
        ContinuedFraction(5, 4)
        """
        if not isinstance(other, self.__class__):
            raise ValueError(
                'The dot product is only defined between `RationalPoint` '
                'instances.'
            )

        if self.coordinates == (0, 0) or other.coordinates == (0, 0):
            return ContinuedFraction(0)

        return (self.x * other.x) + (self.y * other.y)

    def det(self, other: RationalPoint, /) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : The determinant of the :math:`2 \\times 2` matrix formed by the position vectors in :math:`\\mathbb{Q}^2` of this rational point and another.

        Computes the (rational) determinant:

        .. math::

           \\begin{vmatrix}\\frac{a}{c} & \\frac{a'}{c'}\\\\\\frac{b}{d} & \\frac{b'}{d'}\\end{vmatrix} = \\frac{ab'}{cd'} - \\frac{a'b}{c'd} = \\frac{ab'c'd - a'bcd'}{cc'dd'}

        of the matrix formed by the position vectors of two plane rational
        points :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` and
        :math:`P'  = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)`, where
        :math:`P` is represented by ``self`` and :math:`P'` by ``other``.

        Geometrically, the quantity represents the signed area of the
        plane parallelogram formed by the position vectors of :math:`P` and
        :math:`P'` and the vector sum :math:`P + P'`, where the sign is
        positive or negative depending on whether
        :math:`\\frac{bc}{ad} < \\frac{b'c'}{a'd'}` or 
        :math:`\\frac{bc}{ad} > \\frac{b'c'}{a'd'}` respectively, where
        :math:`\\frac{bc}{ad}` and :math:`\\frac{b'c'}{a'd'}` are the
        gradients of the lines passing through the origin :math:`(0, 0)`
        and :math:`P` and :math:`P'` respectively. The quantity is zero
        when these lines are collinear, i.e. when :math:`P` and :math:`P'`
        fall on a single line passing through :math:`(0, 0)`.
        
        Returns
        -------
        ContinuedFraction
            The determinant of the :math:`2 \\times 2` matrix formed by the
            position vector of this rational point and another, as described
            above.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> P, Q, R = RP(F(3, 5), F(4, 5)), RP(1, 1), RP(F(5, 4), 2); P, Q, R
        (RationalPoint(3/5, 4/5), RationalPoint(1, 1), RationalPoint(5/4, 2))
        >>> P.det(Q)
        ContinuedFraction(-1, 5)
        >>> P.det(R)
        ContinuedFraction(1, 5)
        >>> Q.det(R)
        ContinuedFraction(3, 4)
        >>> P.det(P)
        ContinuedFraction(0, 1)
        """
        if not isinstance(other, self.__class__):
            raise ValueError(
                'The determinant is only defined between `RationalPoint` '
                'instances.'
            )

        if self.coordinates == (0, 0) or other.coordinates == (0, 0):
            return ContinuedFraction(0)

        return (self.x * other.y) - (self.y * other.x)    

    @property
    def norm_squared(self) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : The square of the Euclidean (:math:`\\ell_2`) norm of a rational point in the plane.

        The Euclidean (:math:`\\ell_2`) norm squared :math:`\\|P\\|_{2}^2` of a
        rational point :math:`P = \\left(\\frac{a}{c}, \\frac{b}{d} \\right)`
        in the plane, which is the dot product :math:`P \\cdot P` of
        :math:`P` with itself:

        .. math::

           \\begin{align}
           \\|P\\|_{2}^2 = P \\cdot P &= \\frac{a^2}{c^2} + \\frac{b^2}{d^2} \\\\
                                    &= \\frac{a^2d^2 + b^2c^2}{c^2d^2}
           \\end{align}

        and is also a rational number.

        Returns
        -------
        ContinuedFraction
            The Euclidean norm squared of the rational point.

        Examples
        --------
        >>> RationalPoint(1, 1).norm_squared
        ContinuedFraction(2, 1)
        >>> RationalPoint(Fraction(1, 2), Fraction(3, 5)).norm_squared
        ContinuedFraction(61, 100)
        >>> RationalPoint(0, 0).norm_squared
        ContinuedFraction(0, 1)
        """
        return self.dot(self)

    @property
    def norm(self) -> Decimal:
        """:py:class:`~decimal.Decimal` : The Euclidean norm of a rational point in the plane.

        The Euclidean norm :math:`\\|P\\|_2` of a rational point
        :math:`P = \\left(\\frac{a}{c}, \\frac{b}{d} \\right)`, as given by:

        .. math::

           \\begin{align}
           \\|P\\|_2 = \\sqrt{P \\cdot P} &= \\sqrt{\\frac{a^2}{c^2} + \\frac{b^2}{d^2}} \\\\
                                          &= \\sqrt{\\frac{a^2d^2 + b^2c^2}{c^2d^2}}
           \\end{align}

        Returns
        -------
        decimal.Decimal
            The Euclidean norm of the rational point.

        Examples
        --------
        >>> RationalPoint(1, 1).norm
        Decimal('1.414213562373095048801688724')
        >>> RationalPoint(Fraction(1, 2), Fraction(3, 5)).norm
        Decimal('0.7810249675906654394129722736')
        >>> RationalPoint(0, 0).norm
        Decimal('0')
        >>> RationalPoint(Fraction(3, 5), Fraction(4, 5)).norm
        Decimal('1')
        """
        return self.norm_squared.as_decimal().sqrt()

    def distance_squared(self, other: RationalPoint, /) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : The square of the Euclidean distance between this point and another rational point in the plane.

        If :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` and
        :math:`P'  = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)` are
        two rational points in the plane the square of their Euclidean distance
        :math:`\\|P - P'\\|_{2}^2` is the non-negative rational number:

        .. math::

           \\begin{align}
           \\|P - P'\\|^2 &= \\left( \\frac{a}{c} - \\frac{a'}{c'} \\right)^2 + \\left( \\frac{b}{d} - \\frac{b'}{d'} \\right)^2 \\\\
                          &= \\left( \\frac{ac' - a'c}{cc'} \\right)^2 + \\left( \\frac{bd' - b'd}{dd'} \\right)^2 \\\\
                          &= \\frac{\\left(ac' - a'c\\right)^2d^2d'^2 + \\left(bd' - b'd\\right)^2c^2c'^2}{c^2c'^2d^2d'^2}
           \\end{align}

        where :math:`\\|P - P'\\|_{2}^2 = 0` if and only if :math:`P = P'`.

        The Euclidean distance :math:`\\|P - P'\\|_2` is simply the square root of
        this quantity, but will in general not be a rational number **unless**
        :math:`\\left( \\frac{ac' - a'c}{cc'} \\right)^2 + \\left( \\frac{bd' - b'd}{dd'} \\right)^2`
        is a square of a rational number.

        Returns
        -------
        ContinuedFraction
            The square of the Euclidean distance between this point and another
            rational point in the plane.

        Examples
        --------
        >>> P = RationalPoint(Fraction(3, 5), Fraction(4, 5))
        >>> P
        RationalPoint(3/5, 4/5)
        >>> P.distance_squared(RationalPoint(0, 0))
        ContinuedFraction(1, 1)
        >>> P.distance_squared(RationalPoint(1, 1))
        ContinuedFraction(1, 5)
        >>> RationalPoint(0, 0).distance_squared(RationalPoint(1, 1))
        ContinuedFraction(2, 1)
        """
        if not isinstance(other, RationalPoint):
            raise ValueError(
                'The square of the Euclidean distance is defined only between '
                'two `RationalPoint` instances.'
            )

        if other == self:
            return ContinuedFraction(0, 1)

        if other == RationalPoint(0, 0):
            return self.norm_squared

        if self == RationalPoint(0, 0):
            return other.norm_squared

        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2)

    def distance(self, other: RationalPoint, /) -> Decimal:
        """:py:class:`~decimal.Decimal` : The Euclidean distance between this point and another rational point.

        For rational points :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` and
        :math:`P'  = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)` this is the
        square root :math:`\\sqrt{\\|P - P'\\|_{2}^2}` of the distance squared
        :math:`\\|P - P'\\|_{2}^2` as defined above.

        And of course :math:`\\|P - P'\\|_{2} = 0` if and only if :math:`P = P'`.

        Returns
        -------
        decimal.Decimal
            The Euclidean distance between this point and another rational
            point in the plane.

        Examples
        --------
        >>> P = RationalPoint(Fraction(3, 5), Fraction(4, 5))
        >>> P
        RationalPoint(3/5, 4/5)
        >>> P.distance(RationalPoint(0, 0))
        Decimal('1')
        >>> P.distance_squared(RationalPoint(1, 1))
        ContinuedFraction(1, 5)
        >>> RationalPoint(0, 0).distance(RationalPoint(1, 1))
        Decimal('1.414213562373095048801688724')
        """
        if not isinstance(other, RationalPoint):
            raise ValueError(
                'The Euclidean distance is defined only between two '
                '`RationalPoint` instances.'
            )

        return self.distance_squared(other).as_decimal().sqrt()

    def perpendicular_distance(self, other: RationalPoint, /) -> Decimal:
        """:py:class:`~decimal.Decimal` : The perpendicular distance between this rational point and another.

        Given a non-zero rational point
        :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)`, the line
        :math:`\\ell_{OP}` passing through the origin :math:`(0, 0)` and
        :math:`P`, and another rational point
        :math:`P' = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)`, the
        perpendicular distance :math:`d^{\\perp}\\left(P, P'\\right)'` between
        :math:`P` and :math:`P'` is defined here as the length
        :math:`d^{\\perp}\\left(P, P'\\right)` of the line
        segment connecting :math:`P'` and :math:`\\ell_{OP}`, perpendicular to
        the latter, as given by:

        .. math::

           d^{\\perp}\\left(P, P'\\right) = \\frac{\\lvert\\text{det}(P, P')\\rvert}{\\|P\\|_2}

        where :math:`\\text{det}(P, P')` is the determinant
        of :math:`P` and :math:`P'` as described in
        :py:meth:`~continuedfractions.rational_points.RationalPoint.det`.

        Returns
        -------
        decimal.Decimal
            The perpendicular distance between this rational point and another
            as defined above.

        Examples
        --------
        >>> from continuedfractions.rational_points import RationalPoint as RP
        >>> RP(1, 0).perpendicular_distance(RP(0, 1))
        Decimal('1')
        >>> RP(0, 1).perpendicular_distance(RP(1, 0))
        Decimal('1')
        >>> RP(1, 0).perpendicular_distance(RP(1, 0))
        Decimal('0')
        >>> RP(1, 0).perpendicular_distance(RP(-1, 0))
        Decimal('0')
        >>> RP(0, 0).perpendicular_distance(RP(1, 0))
        Traceback (most recent call last):
        ...
        ValueError: The perpendicular distance is defined only between two `RationalPoint` instances, the first of which must be non-zero, i.e. different from `RationalPoint(0, 0)`.
        >>> RP(1, 0).perpendicular_distance(1)
        Traceback (most recent call last):
        ...
        ValueError: The perpendicular distance is defined only between two `RationalPoint` instances, the first of which must be non-zero, i.e. different from `RationalPoint(0, 0)`.
        """
        if not isinstance(other, RationalPoint) or self == self.zero():
            raise ValueError(
                'The perpendicular distance is defined only between two '
                '`RationalPoint` instances, the first of which must be '
                'non-zero, i.e. different from `RationalPoint(0, 0)`.'
            )

        # If the two points are collinear with the origin ``(0, 0)`` return 0.
        a, b = self.angle(as_degrees=True), other.angle(as_degrees=True)
        if a == b or abs(a) + abs(b) == Decimal('180'):
            return Decimal('0')

        # Otherwise compute the value and return
        return abs(self.det(other)).as_decimal() / self.norm

    def is_integral_lattice_point(self) -> bool:
        """:py:class:`bool` : Whether the rational point is an integral lattice point, i.e. has integer coordinates.

        Returns
        -------
        bool
            Whether the coordinates correspond to integers. Coordinates in
            fractional form :math:`\\frac{a}{1}` where the numerator :math:`a`
            is an integer are treated as integers.

        Examples
        --------
        >>> RationalPoint(1, 2).is_integral_lattice_point()
        True
        >>> RationalPoint(Fraction(1, 2), 2).is_integral_lattice_point()
        False
        """
        return all(coord.denominator == 1 for coord in self.coordinates)

    @property
    def rectilinear_norm(self) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction`: The rectilinear (:math:`\\ell_1` or taxicab) norm of the rational point.

        The rectilinear (:math:`\\ell_1` or taxicab) norm :math:`\\|r\\|_1` of
        a rational point :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` is given by:

        .. math::

           \\|P\\|_1 = \\lvert\\frac{a}{c}\\rvert + \\lvert\\frac{b}{d}\\rvert

        The rectilinear norm of a rational point is a non-negative rational
        number, hence the property produces 
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
        objects, as this is the standard representation of rationals in this
        package.

        To get the decimal value use the
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction.as_decimal`
        method.

        Returns
        -------
        ContinuedFraction
            The rectilinear norm of the rational point, which is always a
            non-negative rational number.

        Examples
        --------
        >>> RationalPoint(Fraction(-1, 2), Fraction(3, 4)).rectilinear_norm
        ContinuedFraction(5, 4)
        >>> RationalPoint(Fraction(1, 2), Fraction(-3, 4)).rectilinear_norm
        ContinuedFraction(5, 4)
        >>> RationalPoint(Fraction(1, 2), Fraction(3, 4)).rectilinear_norm
        ContinuedFraction(5, 4)
        """
        return sum(map(abs, self.coordinates))

    def rectilinear_distance(self, other: RationalPoint, /) -> ContinuedFraction:
        """:py:class:`~continuedfractions.continuedfraction.ContinuedFraction` : The rectilinear (:math:`\\ell_1` or taxicab) distance between this rational point and another.

        If :math:`P = \\left( \\frac{a}{c}, \\frac{b}{d} \\right)` and
        :math:`P'  = \\left( \\frac{a'}{c'}, \\frac{b'}{d'} \\right)` are
        two rational points in the plane their rectilinear distance
        :math:`\\|P - P'\\|_1` is the non-negative rational number:

        .. math::

           \\begin{align}
           \\|P - P'\\|_1 &= \\lvert \\frac{a}{c} - \\frac{a'}{c'} \\rvert + \\lvert \\frac{b}{d} - \\frac{b'}{d'} \\rvert \\\\
                          &= \\lvert \\frac{ac' - a'c}{cc'} \\rvert + \\lvert \\frac{bd' - b'd}{dd'} \\rvert
           \\end{align}

        where :math:`\\|P - P'\\| = 0` if and only if :math:`P = P'`.

        Returns
        -------
        decimal.Decimal
            The rectilinear distance between this point and another rational
            point in the plane.

        Examples
        --------
        >>> RationalPoint(Fraction(3, 5), Fraction(4, 5)).rectilinear_distance(RationalPoint(1, 1))
        ContinuedFraction(3, 5)
        >>> RationalPoint(0, 0).rectilinear_distance(RationalPoint(1, 1))
        ContinuedFraction(2, 1)
        """
        if not isinstance(other, RationalPoint):
            raise ValueError(
                'The Euclidean distance is defined only between two '
                '`RationalPoint` instances.'
            )

        return abs(self.x - other.x) + abs(self.y - other.y)

    @property
    def homogeneous_coordinates(self) -> HomogeneousCoordinates:
        """:py:class:`~continuedfractions.rational_points.HomogeneousCoordinates` : A unique sequence of integer-valued homogeneous coordinates in :math:`\\mathbb{P}^2` for this rational point.

        For a rational point :math:`P = \\left(\\frac{a}{c},\\frac{b}{d}\\right)`
        the triple
        :math:`\\left(\\lambda \\frac{a}{c}, \\lambda \\frac{b}{d}, \\lambda\\right) = \\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right)`,
        where :math:`\\lambda = \\text{lcm}(c, d) > 0`, represents a unique representative sequence of homogeneous coordinates for :math:`P` in :math:`\\mathbb{P}^2` such
        that
        :math:`\\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right)`
        are all integers (not all zero) and :math:`\\text{gcd}\\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right) = 1`.

        Returns
        -------
        HomogeneousCoordinates
            A tuple of "minimal" integer-valued homogeneous coordinates in
            for this rational point in projective space :math:`\\mathbb{P}^2`.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> RationalPoint(0, 0).homogeneous_coordinates
        HomogeneousCoordinates(0, 0, 1)
        >>> RationalPoint(F(1, 2), F(3, 4)).homogeneous_coordinates
        HomogeneousCoordinates(2, 3, 4)
        >>> RationalPoint(F(1, 2), F(2, 3)).homogeneous_coordinates
        HomogeneousCoordinates(3, 4, 6)
        >>> RationalPoint(-1, 1).homogeneous_coordinates
        HomogeneousCoordinates(-1, 1, 1)
        >>> RationalPoint(1, 1).homogeneous_coordinates
        HomogeneousCoordinates(1, 1, 1)
        """
        lcm = math.lcm(self.x.denominator, self.y.denominator)

        return HomogeneousCoordinates((lcm * self.x).numerator, (lcm * self.y).numerator, lcm)

    @property
    def height(self) -> int:
        """:py:class:`int` : The height of the rational point in the projective space :math:`\\mathbb{P}^2`.

        The height :math:`H\\left(\\frac{a}{c},\\frac{b}{d}\\right)` of a
        rational point :math:`P = \\left(\\frac{a}{c},\\frac{b}{d}\\right)`
        as given by:

        .. math::

           \\text{max}\\left(|a|\\lvert \\frac{\\lambda}{c} \\rvert, |b|\\lvert \\frac{\\lambda}{d} \\rvert, \\lambda \\right)

        where :math:`\\lambda = \\text{lcm}(c, d) > 0`, and :math:`\\left(\\lambda \\frac{a}{c}, \\lambda \\frac{b}{d}, \\lambda\\right) = \\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right)`
        is a unique sequence of integer-valued homogeneous coordinates
        :math:`\\left(\\lambda \\frac{a}{c}, \\lambda \\frac{b}{d}, \\lambda\\right) = \\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right)`
        of :math:`P` in :math:`\\mathbb{P}^2`.

        Returns
        -------
        int
            The height of this rational point as defined above.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> RationalPoint(0, 0).height
        1
        >>> RationalPoint(1, 1).height
        1
        >>> RationalPoint(-1, 1).height
        1
        >>> RationalPoint(F(3, 5), F(4, 5)).height
        5
        >>> RationalPoint(F(1, 2), F(3, 5)).height
        10
        """
        return max(map(abs, self.homogeneous_coordinates))
        
    @property
    def log_height(self) -> Decimal:
        """:py:class:`~decimal.Decimal` : The natural logarithm of the height of the rational point as defined above.

        The (natural) logarithm of the height of a rational point
        :math:`P = \\left(\\frac{a}{c},\\frac{b}{d}\\right)` as given by:

        .. math::

           \\text{log}\\left(H\\left(\\frac{a}{c}, \\frac{b}{d}\\right)\\right) = \\text{log}\\left(\\text{max}\\left(|a|\\lvert \\frac{\\lambda}{c} \\rvert, |b|\\lvert \\frac{\\lambda}{d} \\rvert, \\lambda \\right)\\right)

        where :math:`\\lambda = \\text{lcm}(c, d) > 0` and :math:`\\left(\\lambda \\frac{a}{c}, \\lambda \\frac{b}{d}, \\lambda\\right) = \\left(a \\frac{\\lambda}{c}, b \\frac{\\lambda}{d}, \\lambda\\right)`
        is a unique sequence of integer-valued homogeneous coordinates for
        :math:`P` in :math:`\\mathbb{P}^2`, as defined above.

        Returns
        -------
        decimal.Decimal
            The (natural) logarithm of the height of this rational point in
            :math:`\\mathbb{P}^2` as defined above.

        Examples
        --------
        >>> from fractions import Fraction as F
        >>> RationalPoint(0, 0).log_height
        Decimal('0')
        >>> RationalPoint(1, 1).log_height
        Decimal('0')
        >>> RationalPoint(-1, 1).log_height
        Decimal('0')
        >>> RationalPoint(F(3, 5), F(4, 5)).log_height
        Decimal('1.6094379124341002817999424223671667277812957763671875')
        >>> RationalPoint(F(1, 2), F(3, 5)).log_height
        Decimal('2.30258509299404590109361379290930926799774169921875')
        """
        return Decimal(math.log(self.height, math.e))

    def __add__(self, other: RationalPoint) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Component-wise addition for two rational points.

        Implements component-wise addition of two rational points:

        .. math::

           \\left(\\frac{a}{c}, \\frac{b}{d}\\right) + \\left(\\frac{a'}{c'}, \\frac{b'}{d'}\\right) = \\left(\\frac{ac' + a'c}{cc'}, \\frac{bd' + b'd}{dd'}\\right)

        The second operand as represented by ``other`` must be an instance of
        :py:class:`~continuedfractions.rational_points.RationalPoint`.
        """
        if not isinstance(other, RationalPoint):
            raise TypeError(
                'Addition is defined only between two `RationalPoint` '
                'instances.'
            )

        return self.__class__(self.x + other.x, self.y + other.y)

    def __sub__(self, other: RationalPoint) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Component-wise subtraction for two rational points.

        Implements component-wise subtraction of two rational points:

        .. math::

           \\left(\\frac{a}{c}, \\frac{b}{d}\\right) - \\left(\\frac{a'}{c'}, \\frac{b'}{d'}\\right) = \\left(\\frac{ac' - a'c}{cc'}, \\frac{bd' - b'd}{dd'}\\right)

        The second operand as represented by ``other`` must be an instance of
        :py:class:`~continuedfractions.rational_points.RationalPoint`.
        """
        if not isinstance(other, RationalPoint):                            # pragma: no cover
            raise TypeError(                                                    
                'Subtraction is defined only between two `RationalPoint` '
                'instances.'
            )

        return self.__class__(self.x - other.x, self.y - other.y)

    def __neg__(self) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Component-wise negation for a rational point.

        Implements component-wise negation for a rational point:

        .. math::

           -\\left(\\frac{a}{c}, \\frac{b}{d}\\right) = \\left(-\\frac{a}{c}, -\\frac{b}{d}\\right)
        """
        return self.__class__(-self.x, -self.y)

    def __mul__(self, other: Any) -> None:
        """Does not support component-wise right-multiplication by a scalar to respect notational convention.
        """
        raise NotImplementedError(
            'Only rational scalar left-multiplication is supported. This '
            'means the left-most operand must be an instance of '
            '`numbers.Rational`, i.e. an `int`, `fractions.Fraction` or '
            '`ContinuedFraction`.'
        )

    def __rmul__(self, other: int | Fraction | ContinuedFraction) -> RationalPoint:
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Component-wise scalar left-multiplication of a rational number by an integer or rational number.

        Implements component-wise left-multiplication of a rational point with
        a rational scalar :math:`\\lambda`:

        .. math::

           \\lambda \\left(\\frac{a}{c}, \\frac{b}{d}\\right) = \\left(\\lambda \\frac{a}{c}, \\lambda \\frac{b}{d}\\right), \\hspace{1em} \\lambda \\in \\mathbb{Q}

        The implementation is in terms of ``__rmul__``, because conventionally
        scalar multiples of a vectors in vector spaces (or subspaces) such as
        :math:`\\mathbb{R}^n` are written in left-multiplication style.
        
        The second operand must be a rational number scalar as given by an
        instance of :py:class:`int`, :py:class:`~fractions.Fraction`, or
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`.
        """
        if not isinstance(other, (int, Fraction, ContinuedFraction)):
            raise TypeError(                                                        # pragma: no cover
                'Only rational scalar left-multiplication is supported. This '
                'means the left-most operand must be an instance of '
                '`numbers.Rational`, i.e. an `int`, `fractions.Fraction` or '
                '`ContinuedFraction`.'
            )

        if other == 0:
            return self.__class__(0, 0)

        return self.__class__(self.x * other, self.y * other)

    def __truediv__(self, other: int | Fraction | ContinuedFraction):
        """:py:class:`~continuedfractions.rational_points.RationalPoint` : Component-wise division by a non-zero rational scalar.

        Implements component-wise division of a rational point by a non-zero
        rational scalar :math:`\\lambda`:

        .. math::

           \\left(\\frac{a}{c}, \\frac{b}{d}\\right) \\div \\lambda = \\frac{1}{\\lambda}\\cdot \\left(\\frac{a}{c}, \\frac{b}{d} \\right) = \\left(\\frac{a}{\\lambda c}, \\frac{b}{\\lambda d} \\right), \\hspace{1em} \\lambda \\in \\mathbb{Q}\\setminus \\{0\\}

        by scaling the point by :math:`\\frac{1}{\\lambda}`.
        """
        if not isinstance(other, (int, Fraction, ContinuedFraction)):
            raise TypeError(                                                        # pragma: no cover
                'The scalar must be a rational, specifically, an instance of '
                '`int`, `fractions.Fraction` or `ContinuedFraction`.'
            )

        if other == 0:
            raise ZeroDivisionError('Division by zero.')

        return Fraction(1, other) * self

    def __abs__(self) -> Decimal:
        """:py:class:`~decimal.Decimal` : The absolute value of the rational point as the standard Euclidean norm.

        For points in :math:`\\mathbb{R}^n` the notion of absolute value and
        Euclidean norm coincide.

        Returns
        -------
        decimal.Decimal
            The absolute value of the rational point as the standard Euclidean norm.

        Examples
        --------
        >>> abs(RationalPoint(0, 0))
        Decimal('0')
        >>> abs(RationalPoint(Fraction(3, 5), Fraction(4, 5)))
        Decimal('1')
        >>> abs(RationalPoint(1, 1))
        Decimal('1.414213562373095048801688724')
        """
        return self.norm


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     PYTHONPATH="src" python3 -m doctest -v src/continuedfractions/rational_points.py
    #
    # NOTE: the doctest examples using ``decimal.Decimal`` values are based on
    #       a context precision of 28 digits.
    decimal.getcontext().prec = 28
    import doctest
    doctest.testmod()
