from __future__ import annotations


__all__ = [
    'ContinuedFraction',
]


# -- IMPORTS --

# -- Standard libraries --
import decimal
import functools
import statistics
import sys

from decimal import Decimal
from fractions import Fraction
from pathlib import Path
from typing import Any, Generator

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.lib import (
    continued_fraction_rational,
    convergent,
    convergents,
    fraction_from_elements,
    left_mediant,
    mediant,
    remainder,
    remainders,
    right_mediant,
)


class ContinuedFraction(Fraction):
    """An object-oriented representation of a (finite) simple continued fraction.

    An implementation of simple continued fractions as Python objects and
    instances of the standard library :py:class:`fractions.Fraction` class, with
    various properties for the continued fraction, including its elements
    (or coefficients), the order, convergents, and remainders.

    The term "simple continued fraction" denotes a specific type of continued
    fraction where the fractional terms only have numerators of :math:`1`.

    Examples
    --------
    Construct the continued fraction for the rational `649/200`.

    >>> cf = ContinuedFraction(649, 200)
    >>> cf
    ContinuedFraction(649, 200)
    >>> cf.as_float()
    3.245

    Inspect the elements, order, convergents, and remainders.

    >>> cf.elements
    (3, 4, 12, 4)
    >>> cf.order
    3
    >>> cf.convergent(0), cf.convergent(1), cf.convergent(2), cf.convergent(3)
    (ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))
    >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
    (ContinuedFraction(649, 200), ContinuedFraction(200, 49), ContinuedFraction(49, 4), ContinuedFraction(4, 1))

    Check some properties of the convergents and remainders.

    >>> assert cf.remainder(1) == 1 / (cf - cf.convergent(0))

    Construct continued fractions from element sequences.

    >>> cf_inverse = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
    >>> cf_inverse
    ContinuedFraction(200, 649)
    >>> assert cf_inverse == 1/cf
    >>> assert cf * cf_inverse == 1
    >>> cf_negative_inverse = ContinuedFraction.from_elements(-1, 1, 2, 4, 12, 4)
    >>> cf_negative_inverse
    ContinuedFraction(-200, 649)
    >>> assert cf_negative_inverse == -1/cf
    >>> assert cf * cf_negative_inverse == -1
    """

    # Slots - ATM only ``_elements`` to store the continued fraction elements sequence
    __slots__ = ['_elements',]

    # Declare all instances to have an ``_elements`` attribute, which must be
    # a ``tuple`` of ``int``s.
    _elements: tuple[int]

    def __new__(cls, *args: Any, **kwargs: Any) -> ContinuedFraction:
        """Creates, initialises and returns instances of this class.

        Arguments can be any which are valid for creating objects of the
        :py:class:`fractions.Fraction` superclass.

        For clarification, valid arguments can be one of the following:

        * a single instance of :py:class:`numbers.Rational`, including
          :py:class:`int`, :py:class:`fractions.Fraction` or
          :py:class:`ContinuedFraction`, named or unnamed
        * a pair of  :py:class:`numbers.Rational` instances, including
          :py:class:`int`, :py:class:`fractions.Fraction` and
          :py:class:`ContinuedFraction`, named or unnamed
        * a single :py:class:`float` or :py:class:`decimal.Decimal` value
          that is not a special value such as :py:data:`math.nan`,
          ``float('inf')``, or ``Decimal('infinity')``
        * a single numeric valid string (:py:class:`str`) - validity is
          determined in the superclass by the
          :py:data:`fractions._RATIONAL_FORMAT` test

        Returns
        -------
        ContinuedFraction
            A :py:class:`ContinuedFraction` instance.

        Examples
        --------
        Several example are given below of constructing the simple continued
        fraction for the number :math:`\\frac{-649}{200}` in different ways.

        >>> ContinuedFraction(-649, 200)
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction('-3.245')
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(Decimal('-3.245'))
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction('-649/200')
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(Fraction(-649, 200))
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(ContinuedFraction(649, -200))
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(Fraction(-649), 200)
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(649, Fraction(-200))
        ContinuedFraction(-649, 200)
        >>> ContinuedFraction(Fraction(-649), ContinuedFraction(200))
        ContinuedFraction(-649, 200)

        In each of the examples above, the minus sign can be removed from
        the arguments to the :py:class:`numbers.Rational` instance and
        instead attached to the outer class, e.g.:

        >>> -ContinuedFraction(649, 200)
        ContinuedFraction(-649, 200)
        >>> -ContinuedFraction('3.245')
        ContinuedFraction(-649, 200)
        >>> -ContinuedFraction('649/200')
        ContinuedFraction(-649, 200)

        Invalid arguments will raise errors in the
        :py:class:`fractions.Fraction` superclass.
        """
        # Get the ``fractions.Fraction`` instance from the superclass constructor
        self = super().__new__(cls, *args, **kwargs)

        # Call ``lib.continued_fraction_rational`` with the fraction to get
        # get the elements, and assign back to the instance
        self._elements = tuple(continued_fraction_rational(self))

        return self

    @classmethod
    def from_elements(cls, *elements: int) -> ContinuedFraction:
        """Returns a :py:class:`ContinuedFraction` instance from a sequence of (integer) elements of a (finite) simple continued fraction.

        Invalid elements will trigger a :py:class:`ValueError`.

        Parameters
        ----------
        *elements : int
            An ordered sequence of integer elements of a (finite) simple
            continued fraction.

        Returns
        -------
        ContinuedFraction
            A new and fully initialised instance of :py:class:`ContinuedFraction` with
            the given element sequence.

        Raises
        ------
        ValueError
            If any elements are not integers, or any elements after the 1st
            are not positive.

        Examples
        --------
        Constructing a continued fraction for the rational :math:`\\frac{649}{200}` using
        the element sequence :math:`3, 4, 12, 4`.

        >>> c1 = ContinuedFraction.from_elements(3, 4, 12, 4)
        >>> c1
        ContinuedFraction(649, 200)

        Constructing the continued fraction of the (multiplicative) inverse :math:`\\frac{200}{649}`
        using the element sequence :math:`0, 3, 4, 12, 4`.

        >>> c2 = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
        >>> c2
        ContinuedFraction(200, 649)

        Validation for elements containing non-integers or negative integers.

        >>> ContinuedFraction.from_elements('0', 1)
        Traceback (most recent call last):
        ...
        ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
        >>> ContinuedFraction.from_elements(0, 1, 2.5)
        Traceback (most recent call last):
        ...
        ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
        >>> ContinuedFraction.from_elements(1, 0)
        Traceback (most recent call last):
        ...
        ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive
        >>> ContinuedFraction.from_elements(1, -1)
        Traceback (most recent call last):
        ...
        ValueError: Continued fraction elements must be integers, and all elements after the 1st must be positive

        """
        # Create a new ``ContinuedFraction`` instance from the given elements
        # and initialise with elements only - no need to initialise via
        # ``__init__``
        if any(not isinstance(elem, int) or (elem <= 0 and i > 0) for i, elem in enumerate(elements)):
            raise ValueError(
                "Continued fraction elements must be integers, and all "
                "elements after the 1st must be positive"
            )

        # A step to ensure uniqueness of the simple form of the continued
        # fraction - if the last element is ``1`` it can be "removed" by
        # adding it to the second last element, thereby shortening the
        # sequence by one element. The resulting simple continued
        # fraction becomes unique for the number that is represented.
        if len(elements) > 1 and elements[-1] == 1:
            elements = elements[:-2] + (elements[-2] + 1,)

        # Call the superclass constructor with the ``fractions.Fraction``
        # instance returned by ``lib.fraction_from_elements`` - this will
        # be the highest-order convergent of the simple continued
        # fraction represented by the given sequence of elements
        self = super().__new__(cls, fraction_from_elements(*elements))

        # Assign the given elements back to the instance - note that we
        # have avoided going through the division algorithm in
        # ``lib.continued_fraction_rational``
        self._elements = elements
    
        return self

    def extend(self, *new_elements: int) -> None:
        """Performs an in-place extension of the tail of the current sequence of elements.

        Raises a :py:class:`ValueError` if there are no new elements, or are
        not positive integers.

        .. note::

           As this method performs an in-place modification of the existing/
           current instance the object ID remains the same.

        Parameters
        ----------
        elements
            An (ordered) sequence of new (integer) elements by which the tail
            of the existing sequence of elements is extended.

        Raises
        ------
        ValueError
            If no new elements provided, or the new elements provided are not
            positive integers.

        Examples
        --------
        >>> cf = ContinuedFraction('3.245')
        >>> cf
        ContinuedFraction(649, 200)
        >>> cf.elements
        (3, 4, 12, 4)
        >>> cf.order
        3
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(3, 1)), (1, ContinuedFraction(13, 4)), (2, ContinuedFraction(159, 49)), (3, ContinuedFraction(649, 200)))
        >>> tuple(cf.remainders)
        ((3, ContinuedFraction(4, 1)), (2, ContinuedFraction(49, 4)), (1, ContinuedFraction(200, 49)), (0, ContinuedFraction(649, 200)))
        >>> cf.extend(5, 2)
        >>> cf
        ContinuedFraction(7457, 2298)
        >>> cf.elements
        (3, 4, 12, 4, 5, 2)
        >>> cf.order
        5
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(3, 1)), (1, ContinuedFraction(13, 4)), (2, ContinuedFraction(159, 49)), (3, ContinuedFraction(649, 200)), (4, ContinuedFraction(3404, 1049)), (5, ContinuedFraction(7457, 2298)))
        >>> tuple(cf.remainders)
        ((5, ContinuedFraction(2, 1)), (4, ContinuedFraction(11, 2)), (3, ContinuedFraction(46, 11)), (2, ContinuedFraction(563, 46)), (1, ContinuedFraction(2298, 563)), (0, ContinuedFraction(7457, 2298)))
        >>> cf = ContinuedFraction(649, 200)
        >>> cf.extend(0, 1)
        Traceback (most recent call last):
        ...
        ValueError: The elements/coefficients to be added to the tail must be positive integers.
        >>> cf.extend(1, -1)
        Traceback (most recent call last):
        ...
        ValueError: The elements/coefficients to be added to the tail must be positive integers.
        """
        if not new_elements or any(not isinstance(x, int) or x < 1 for x in new_elements):
            raise ValueError(
                "The elements/coefficients to be added to the tail must be "
                "positive integers."
            )

        elements = self._elements + new_elements
        fraction = convergent(len(elements) - 1, *elements)
        self._numerator, self._denominator = fraction.as_integer_ratio()
        self._elements = elements

    def truncate(self, *tail_elements: int) -> None:
        """Performs an in-place truncation of the tail of the existing sequence of elements.

        Raises a :py:class:`ValueError` if the tail elements provided are not
        positive integers, or do not form a segment of the existing tail. This
        includes the case where the length of the tail elements provided exceed
        the length of the existing tail, i.e. the order of the continued
        fraction represented by the instance.

        .. note::

           The tail elements provided must be positive integers which form a
           subsequence of the tail of the original sequence ending with the
           last element, e.g. with respect to the complete sequence of elements
           ``(3, 4, 12, 4)`` a value of ``12, 4`` for ``*tail_elements`` would
           be valid, but ``4, 12`` would be invalid as it does not represent
           a segment of the tail, and ``3, 4, 12, 4`` would also be invalid
           as it includes the head ``3``.

        .. note::

           As this method performs an in-place modification of the existing/
           current instance the object ID remains the same.

        Parameters
        ----------
        tail_elements
            An (ordered) sequence of (integer) elements to truncate from the
            tail of the existing sequence of elements.

        Raises
        ------
        ValueError
            If no tail elements are provided, or the tail elements provided do
            not represent a valid segment of the existing tail.

        Examples
        --------
        >>> cf = ContinuedFraction('3.245')
        >>> cf
        ContinuedFraction(649, 200)
        >>> cf.elements
        (3, 4, 12, 4)
        >>> cf.order
        3
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(3, 1)), (1, ContinuedFraction(13, 4)), (2, ContinuedFraction(159, 49)), (3, ContinuedFraction(649, 200)))
        >>> tuple(cf.remainders)
        ((3, ContinuedFraction(4, 1)), (2, ContinuedFraction(49, 4)), (1, ContinuedFraction(200, 49)), (0, ContinuedFraction(649, 200)))
        >>> cf.truncate(12, 4)
        >>> cf
        ContinuedFraction(13, 4)
        >>> cf.elements
        (3, 4)
        >>> cf.order
        1
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(3, 1)), (1, ContinuedFraction(13, 4)))
        >>> tuple(cf.remainders)
        ((1, ContinuedFraction(4, 1)), (0, ContinuedFraction(13, 4)))
        >>> cf = ContinuedFraction(649, 200)
        >>> cf.truncate(4, 12)
        Traceback (most recent call last):
        ...
        ValueError: The elements/coefficients to be truncated from the tail must form a valid segment of the existing tail.
        >>> cf.truncate(3, 4, 12, 4)
        Traceback (most recent call last):
        ...
        ValueError: The elements/coefficients to be truncated from the tail must form a valid segment of the existing tail.
        """
        order = self.order
        truncation_length = len(tail_elements)

        if not tail_elements or truncation_length > order or self._elements[order + 1 - truncation_length:] != tail_elements:
            raise ValueError(
                "The elements/coefficients to be truncated from the tail must "
                "form a valid segment of the existing tail."
            )

        elements = self._elements[:order + 1 - truncation_length]

        # A step to ensure uniqueness of the simple form of the continued
        # fraction - if the last element is ``1`` it can be "removed" by
        # adding it to the second last element, thereby shortening the
        # sequence by one element. The resulting simple continued
        # fraction becomes unique for the number that is represented.
        if len(elements) > 1 and elements[-1] == 1:
            elements = elements[:-2] + (elements[-2] + 1,)

        fraction = convergent(len(elements) - 1, *elements)
        self._numerator, self._denominator = fraction.as_integer_ratio()
        self._elements = elements

    def __eq__(self, other, /) -> bool:
        """Custom equality check.

        Compares the sequence of elements/coefficients of ``self`` with
        that of ``other`` if ``other`` is also a
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
        instance, otherwise calls the superclass :py:class:`~fractions.Fraction`
        equality check.

        Returns
        -------
        bool
            The boolean result of the equality check.
        """
        if isinstance(other, self.__class__):
            return self._elements == other._elements

        return super().__eq__(other)

    def __hash__(self) -> int:
        """Custom hash.

        Custom hash which hashes the sequence of elements/coefficients - as
        this is always defined as a finite, non-empty tuple the hash is
        always defined.

        Returns
        -------
        int
            The hash of the
            :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
            instance.
        """
        return hash(self._elements)

    def __add__(self, other, /):
        return self.__class__(super().__add__(other))

    def __radd__(self, other, /):
        return self.__class__(super().__radd__(other))

    def __sub__(self, other, /):
        return self.__class__(super().__sub__(other))

    def __rsub__(self, other, /):
        return self.__class__(super().__rsub__(other))

    def __mul__(self, other, /):
        return self.__class__(super().__mul__(other))

    def __rmul__(self, other, /):
        return self.__class__(super().__rmul__(other))

    def __truediv__(self, other, /):
        return self.__class__(super().__truediv__(other))

    def __rtruediv__(self, other, /):
        return self.__class__(super().__rtruediv__(other))

    def __floordiv__(self, other, /):
        return self.__class__(super().__floordiv__(other))

    def __rfloordiv__(self, other, /):
        return self.__class__(super().__rfloordiv__(other))

    def __divmod__(self, other, /):
        quo, rem = super().__divmod__(other)

        return self.__class__(quo), self.__class__(rem)

    def __rdivmod__(self, other, /):
        quo, rem = super().__rdivmod__(other)
        
        return self.__class__(quo), self.__class__(rem)

    def __pow__(self, other, /) -> ContinuedFraction:
        return self.__class__(super().__pow__(other))

    def __rpow__(self, other, /):
        return self.__class__(Fraction(other).__rpow__(self))

    def __pos__(self) -> ContinuedFraction:
        return self.__class__(super().__pos__())

    def __neg__(self) -> ContinuedFraction:
        """
        Division-free negation for a finite simple continued fraction, as
        described `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/creating-continued-fractions.html#negative-continued-fractions>`_.

        The basic algorithm can be described as follows: if
        :math:`[a_0; a_1,\\ldots, a_n]` is the simple continued fraction of a
        **positive** rational number :math:`\\frac{a}{b}` of finite order
        :math:`n` then  :math:`-\\frac{a}{b}` has the simple continued
        fraction:

        .. math::

           \\begin{cases}
           [-a_0;]                                      \\hskip{3em} & n = 0 \\\\
           [-(a_0 + 1); 2]                              \\hskip{3em} & n = 1 \\text{ and } a_1 = 2 \\\\
           [-(a_0 + 1); a_2 + 1, a_3,\\ldots, a_n]      \\hskip{3em} & n \\geq 2 \\text{ and } a_1 = 1 \\\\
           [-(a_0 + 1); 1, a_1 - 1, a_2, \\ldots,a_n]   \\hskip{3em} & n \\geq 2 \\text{ and } a_1 \\geq 2
           \\end{cases}

        In applying this algorithm there is an assumption that the last element
        :math:`a_n > 1`, as any simple continued fraction of type
        :math:`[a_0; a_1,\\ldots, a_{n} = 1]` can be reduced to the simple
        continued fraction :math:`[a_0; a_1,\\ldots, a_{n - 1} + 1]`.
        """
        cls_ = self.__class__
        elms = self._elements

        if len(elms) == 1:
            # Case (1) of the algorithm
            neg_elms = (-elms[0],)
        elif len(elms) == 2 and elms[1] == 2:
            # Case (2) of the algorithm
            neg_elms = (-(elms[0] + 1), 2)
        elif len(elms) > 1 and elms[1] == 1:
            # Case (3) of the algorithm
            neg_elms = (-(elms[0] + 1), elms[2] + 1, *elms[3:])
        else:
            # Case (4) of the algorithm
            neg_elms = (-(elms[0] + 1), 1, elms[1] - 1, *elms[2:])

        neg_self = cls_.__new__(cls_, *convergent(len(neg_elms) - 1, *neg_elms).as_integer_ratio())
        neg_self._elements = neg_elms

        return neg_self

    def __abs__(self) -> ContinuedFraction:
        return self.__class__(super().__abs__())

    def as_float(self) -> float:
        """Returns the :py:class:`float` value of the continued fraction.

        Returns
        -------
        float
            The :py:class:`float` value of the continued fraction.

        Examples
        --------
        Note that the default :py:mod:`decimal` context precision of :math:`28`
        is used in these examples.

        >>> import math
        >>> math.pi
        3.141592653589793

        Now construct a :py:class:`ContinuedFraction` instance from it, and check the 
        :py:class:`float` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_float()
        3.141592653589793
        """
        return self.numerator / self.denominator

    def as_decimal(self) -> Decimal:
        """Returns the :py:class:`decimal.Decimal` value of the continued fraction.

        Returns
        -------
        decimal.Decimal
            The :py:class:`decimal.Decimal` representation of the continued fraction.

        Examples
        --------
        Note that the default :py:mod:`decimal` context precision of :math:`28`
        is used in these examples.

        >>> import math
        >>> math.pi
        3.141592653589793

        Now construct a :py:class:`ContinuedFraction` instance from it, and check the 
        :py:class:`float` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_decimal()
        Decimal('3.141592653589793115997963469')
        """
        return Decimal(self.numerator) / Decimal(self.denominator)

    @property
    def elements(self) -> tuple[int]:
        """:py:class:`tuple`: The (ordered) sequence of elements of the continued fraction.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.elements
        (0, 8, 9, 1, 21, 1, 1, 5)
        """
        return self._elements

    @property
    def order(self) -> int:
        """:py:class:`int`: The order of the continued fraction, which is the number of its elements minus :math:`1`.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> len(cf.elements)
        8
        >>> cf.order
        7
        """
        return len(self._elements[1:])

    @property
    def khinchin_mean(self) -> Decimal | None:
        """:py:class:`decimal.Decimal` or :py:data:`None`: The Khinchin mean of the continued fraction, which is defined as the geometric mean of all its elements after the 1st.

        We define the Khinchin mean :math:`K_n` of a (simple) continued
        fraction :math:`[a_0; a_1, a_2, \\ldots, a_n]` as:

        .. math::

           K_n := \\sqrt[n]{a_1a_2 \\cdots a_n} = \\left( a_1a_2 \\cdots a_n \\right)^{\\frac{1}{n}}, \\hskip{3em} n \\geq 1

        This property is intended to make it easier to study the limit of
        :math:`K_n` as :math:`n \\to \\infty`.  See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/exploring-continued-fractions.html#khinchin-means-khinchin-s-constant>`_
        for more details.

        In the special case of integers or fractions representing integers,
        whose continued fraction representations consist of only a single
        element, a null value is returned.

        Examples
        --------
        Note that the default :py:mod:`decimal` context precision of :math:`28`
        is used in these examples.

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

        """
        match self.order:
            case 0:
                return None
            case 1:
                return Decimal(self.elements[-1])
            case _:
                return Decimal(statistics.geometric_mean(self.elements[1:]))

    @functools.cache
    def convergent(self, k: int, /) -> ContinuedFraction:
        """Returns the :math:`k`-th (simple) convergent of the continued fraction.

        Given a (simple) continued fraction  :math:`[a_0;a_1,a_2,\\ldots]` the
        :math:`k`-th convergent is defined as:

        .. math::

           C_k = a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2 \\ddots \\cfrac{1}{a_{k-1} + \\cfrac{1}{a_k}}}}

        The result is a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance.
        
        If  the continued fraction is of order :math:`n` then it has exactly
        :math:`n + 1` convergents :math:`C_0,C_1,C_2,\\ldots,C_n` where
        the :math:`k`-th convergent :math:`C_k = \\frac{p_k}{q_k}` is given by
        the recurrence relation:

        .. math::
           
           \\begin{align}
           p_k &= a_kp_{k - 1} + p_{k - 2} \\\\
           q_k &= a_kq_{k - 1} + q_{k - 2},        \\hskip{3em}    k \\geq 3
           \\end{align}

        where :math:`p_0 = a_0`, :math:`q_0 = 1`, :math:`p_1 = p_1p_0 + 1`,
        and :math:`q_1 = p_1`.

        Parameters
        ----------
        k : int
            The index of the convergent, as described above.

        Returns
        -------
        ContinuedFraction
            A new :py:class:`ContinuedFraction` instance representing the :math:`k`-th
            (simple) convergent of the original continued fraction, as
            described above.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.convergent(0)
        ContinuedFraction(0, 1)
        >>> cf.convergent(2)
        ContinuedFraction(9, 73)
        >>> cf.convergent(6)
        ContinuedFraction(448, 3629)
        >>> cf.convergent(7)
        ContinuedFraction(2469, 20000)
        """
        return self.__class__(convergent(k, *self._elements))

    @property
    def convergents(self) -> Generator[tuple[int, ContinuedFraction], None, None]:
        """Generates an enumerated sequence of all convergents of the continued fraction.

        The convergents are generated as tuples of :py:class:`int` and
        :py:class:`~continuedfraction.continuedfraction.ContinuedFraction`
        instances, where the integers represent the indices of the convergents.

        If :math:`n` is the order of the continued fraction then :math:`n + 1`
        convergents :math:`C_0, C_1, \\ldots, C_n` are generated in that order.

        Yields
        ------
        tuple
            A tuple of convergent index (:py:class:`int`) and convergents
            (:py:class:`~continuedfractions.continuedfraction.ContinuedFraction`)
            of the continued fraction.

        Examples
        --------
        >>> cf = ContinuedFraction('3.245')
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(3, 1)), (1, ContinuedFraction(13, 4)), (2, ContinuedFraction(159, 49)), (3, ContinuedFraction(649, 200)))
        """
        yield from enumerate(map(self.__class__, convergents(*self._elements)))

    @property
    def even_convergents(self) -> Generator[tuple[int, ContinuedFraction], None, None]:
        """Generates an enumerated sequence of all even-order convergents of the continued fraction.

        The convergents are generated as tuples of :py:class:`int` and
        :py:class:`~continuedfraction.continuedfraction.ContinuedFraction`
        instances, where the integers represent the indices of the convergents.

        If :math:`n` is the order of the continued fraction then only the even-
        indexed convergents :math:`C_0, C_2, C_4, \\ldots` are generated.

        Yields
        ------
        tuple
            A tuple of convergent index (:py:class:`int`) and convergents
            (:py:class:`~continuedfractions.continuedfraction.ContinuedFraction`)
            of the continued fraction.

        Examples
        --------
        >>> tuple(ContinuedFraction('3.245').even_convergents)
        ((0, ContinuedFraction(3, 1)), (2, ContinuedFraction(159, 49)))
        """
        yield from filter(lambda t: t[0] % 2 == 0, self.convergents)

    @property
    def odd_convergents(self) -> Generator[tuple[int, ContinuedFraction], None, None]:
        """Generates an enumerated sequence of all odd-order convergents of the continued fraction.

        The convergents are generated as tuples of :py:class:`int` and
        :py:class:`~continuedfraction.continuedfraction.ContinuedFraction`
        instances, where the integers represent the indices of the convergents.

        If :math:`n` is the order of the continued fraction then only the odd-
        indexed convergents :math:`C_1, C_3, C_5, \\ldots` are generated.

        Yields
        ------
        tuple
            A tuple of convergent index (:py:class:`int`) and convergents
            (:py:class:`~continuedfractions.continuedfraction.ContinuedFraction`)
            of the continued fraction.

        Examples
        --------
        >>> tuple(ContinuedFraction('3.245').odd_convergents)
        ((1, ContinuedFraction(13, 4)), (3, ContinuedFraction(649, 200)))
        """
        yield from filter(lambda t: t[0] % 2 == 1, self.convergents)

    @functools.cache
    def semiconvergent(self, k: int, m: int, /) -> ContinuedFraction:
        """Returns the :math:`m`-th semiconvergent of two consecutive convergents :math:`p_{k - 1}` and :math:`p_k` of the continued fraction.

        The integer :math:`k` must be positive and determine two consecutive
        convergents :math:`p_{k - 1}` and :math:`p_k` of a (finite, simple)
        continued fraction.

        The integer :math:`m` can be any positive integer.

        Parameters
        ----------
        k : int
            The integer :math:`k` determining two consecutive convergents
            :math:`p_{k - 1}` and :math:`p_k` of a (finite, simple) continued
            fraction
            :math:`[a_0; a_1, \\ldots, a_{k}, a_{k + 1}, \\ldots, a_n]`.

        m : int
            The index of the semiconvergent of the convergents
            :math:`p_{k - 1}` and :math:`p_k`.

        Returns
        -------
        ContinuedFraction
            The :math:`m`-th semiconvergent of the convergents
            :math:`p_{k - 1}` and :math:`p_k`.

        Raises
        ------
        ValueError
            If :math:`k` or :math:`m` are not positive integers, or :math:`k`
            is an integer that does **not** satisfy :math:`1 \\leq k \\leq n`
            where :math:`n` is the order of the (finite, simple) continued
            fraction of which :math:`p_{k - 1}` and :math:`p_k` are
            convergents.

        Examples
        --------
        >>> cf = ContinuedFraction(-415, 93)
        >>> cf.elements
        (-5, 1, 1, 6, 7)
        >>> tuple(cf.convergents)
        ((0, ContinuedFraction(-5, 1)), (1, ContinuedFraction(-4, 1)), (2, ContinuedFraction(-9, 2)), (3, ContinuedFraction(-58, 13)), (4, ContinuedFraction(-415, 93)))
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
        """
        if not isinstance(k, int) or k not in range(1, self.order + 1) or not isinstance(m, int) or m < 1:
            raise ValueError(
                "`k` and `m` must be positive integers and `k` must be an "
                "integer in the range `1..n` where `n` is the order of the "
                "continued fraction"
            )

        return self.convergent(k - 1).right_mediant(self.convergent(k), k=m)

    @functools.cache
    def remainder(self, k: int, /) -> ContinuedFraction:
        """Returns the :math:`k`-th remainder of the continued fraction.

        Given a (simple) continued fraction  :math:`[a_0;a_1,a_2,\\ldots]` the
        :math:`k`-th remainder :math:`R_k` is the (simple) continued fraction
        :math:`[a_k; a_{k + 1}, a_{k + 2}, \\ldots]`:

        .. math::

           R_k = a_k + \\cfrac{1}{a_{k + 1} + \\cfrac{1}{a_{k + 2} \\ddots }}

        where :math:`R_0` is just the original continued fraction, i.e.
        :math:`R_0 = [a_0; a_1, a_2, \\ldots]`.

        The result is a :py:class:`~continuedfractions.continuedfraction.ContinuedFraction` instance.

        The remainders satisfy the recurrence relation:

        .. math::

           R_{k - 1} = a_{k - 1} + \\frac{1}{R_k}, \\hskip{3em} k \\geq 1

        If the original continued fraction is finite then its remainders are all
        finite and rational.

        As this class implements finite simple continued fractions, this method
        always produces rational numbers.

        The integer :math:`k` must be non-negative and cannot exceed the order
        of the continued fraction, i.e. the number of its tail elements, and 
        the tail elements must define a valid finite simple continued fraction.

        Parameters
        ----------
        k : int
            The index of the remainder, as described above.

        Returns
        -------
        ContinuedFraction
            A new :py:class:`ContinuedFraction` instance representing the :math:`k`-th
            remainder of the original continued fraction, as described above.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.remainder(0)
        ContinuedFraction(2469, 20000)
        >>> cf.remainder(2)
        ContinuedFraction(2469, 248)
        >>> cf.remainder(6)
        ContinuedFraction(6, 5)
        >>> cf.remainder(7)
        ContinuedFraction(5, 1)
        """
        return self.__class__(remainder(k, *self._elements))

    @property
    def remainders(self) -> Generator[tuple[int, ContinuedFraction], None, None]:
        """Generates an enumerated sequence of all remainders of the continued fraction in descending order of index.

        If :math:`n` is the order of the continued fraction then there are
        :math:`n + 1` remainders :math:`R_0, R_1, \\ldots, R_n`, and the method
        generates these in reverse order :math:`R_0, R_1, \\ldots, R_n`.

        See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/exploring-continued-fractions.html#remainders>`_
        for more details on remainders.

        The remainders are generated as tuples of :py:class:`int`
        and :py:class:`~continuedfraction.continuedfraction.ContinuedFraction`
        instances, where the integers represent the indexes of the remainders.

        Yields
        ------
        tuple
            A tuple of remainder indices (:py:class:`int`) and remainders
            (:py:class:`~continuedfractions.continuedfraction.ContinuedFraction`)
            of the continued fraction.

        Examples
        --------
        >>> tuple(ContinuedFraction('3.245').remainders)
        ((3, ContinuedFraction(4, 1)), (2, ContinuedFraction(49, 4)), (1, ContinuedFraction(200, 49)), (0, ContinuedFraction(649, 200)))
        >>> tuple(ContinuedFraction(-415, 93).remainders)
        ((4, ContinuedFraction(7, 1)), (3, ContinuedFraction(43, 7)), (2, ContinuedFraction(50, 43)), (1, ContinuedFraction(93, 50)), (0, ContinuedFraction(-415, 93)))
        """
        yield from zip(reversed(range(self.order + 1)), map(self.__class__, remainders(*self._elements)))

    @functools.cache
    def left_mediant(self, other: Fraction, /, *, k: int = 1) -> ContinuedFraction:
        """Returns the :math:`k`-th left-mediant of the continued fraction with another rational number.
        
        For a positive integer :math:`k`, the :math:`k`-th left-mediant of two
        rational numbers :math:`r = \\frac{a}{b}` and :math:`s = \\frac{c}{d}`,
        where :math:`b, d, b + d \\neq 0`, is defined as:
        
        .. math::

           \\frac{ka + c}{kb + d}, \\hskip{3em}    k \\geq 1

        while the :math:`k`-th right mediant is defined as:
        
        .. math::

           \\frac{a + kc}{b + kd}, \\hskip{3em}    k \\geq 1

        If we assume that :math:`r < s` and :math:`bd > 0` then these mediants
        have the property that:
       
        .. math::

           \\frac{a}{b} < \\frac{ka + c}{kb + d} \\leq \\frac{a + kc}{b + kd} < \\frac{c}{d},   \\hskip{3em} k \\geq 1

        where equality holds for :math:`k = 1`. If we let :math:`k \\to \\infty`
        then the mediants converge to opposite limits:

        .. math::

          \\begin{align}
          \\lim_{k \\to \\infty} \\frac{ka + c}{kb + d} &= \\frac{a}{b} \\\\
          \\lim_{k \\to \\infty} \\frac{a + kc}{b + kd} &= \\frac{c}{d}
          \\end{align}

        For more information consult the
        `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/mediants.html>`_.

        The method is cached (with :py:func:`functools.cache`), which makes calls
        after the initial call much faster.

        Parameters
        ----------
        other : fractions.Fraction, ContinuedFraction
            The second fraction to use to calculate the :math:`k`-th mediant with
            the first.
        
        k : int, default=1
            The order of the mediant, as defined above.        

        Returns
        -------
        ContinuedFraction
            The :math:`k`-th left-mediant of the original fraction and the second
            fraction, as a :py:class:`ContinuedFraction` instance.

        Examples
        --------
        >>> c1 = ContinuedFraction('1/2')
        >>> c2 = ContinuedFraction(3, 5)
        >>> c1, c2
        (ContinuedFraction(1, 2), ContinuedFraction(3, 5))
        >>> c1.left_mediant(c2)
        ContinuedFraction(4, 7)
        >>> c1.left_mediant(c2, k=2)
        ContinuedFraction(5, 9)
        >>> c1.left_mediant(c2, k=3)
        ContinuedFraction(6, 11)
        >>> c1.left_mediant(c2, k=100)
        ContinuedFraction(103, 205)
        >>> assert c1.left_mediant(c2, k=2) < c1.right_mediant(c2, k=2)
        >>> assert c1.left_mediant(c2, k=3) < c1.right_mediant(c2, k=3)
        >>> assert c1.left_mediant(c2, k=100) < c1.right_mediant(c2, k=100)
        """
        return self.__class__(left_mediant(self, other, k=k))

    @functools.cache
    def right_mediant(self, other: Fraction, /, *, k: int = 1) -> ContinuedFraction:
        """Returns the :math:`k`-th right-mediant of the continued fraction with another rational number.
        
        For a positive integer :math:`k`, the :math:`k`-th right-mediant of two
        rational numbers :math:`r = \\frac{a}{b}` and :math:`s = \\frac{c}{d}`,
        where :math:`b, d, b + d \\neq 0`, is defined as:
        
        .. math::

           \\frac{a + kc}{b + kd}, \\hskip{3em}    k \\geq 1

        while the :math:`k`-th left-mediant is defined as:
        
        .. math::

           \\frac{ka + c}{kb + d}, \\hskip{3em}    k \\geq 1

        If we assume that :math:`r < s` and :math:`bd > 0` then these mediants
        have the property that:
       
        .. math::

           \\frac{a}{b} < \\frac{ka + c}{kb + d} \\leq \\frac{a + kc}{b + kd} < \\frac{c}{d},   \\hskip{3em} k \\geq 1

        where equality holds for :math:`k = 1`. If we let :math:`k \\to \\infty`
        then the mediants converge to opposite limits:

        .. math::

          \\begin{align}
          \\lim_{k \\to \\infty} \\frac{ka + c}{kb + d} &= \\frac{a}{b} \\\\
          \\lim_{k \\to \\infty} \\frac{a + kc}{b + kd} &= \\frac{c}{d}
          \\end{align}

        For more information consult the
        `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/mediants.html>`_.

        Parameters
        ----------
        other : fractions.Fraction, ContinuedFraction
            The second fraction to use to calculate the :math:`k`-th mediant with
            the first.
        
        k : int, default=1
            The order of the mediant, as defined above.        

        Returns
        -------
        ContinuedFraction
            The :math:`k`-th right-mediant of the original fraction and the second
            fraction, as a :py:class:`ContinuedFraction` instance.

        Examples
        --------
        >>> c1 = ContinuedFraction('1/2')
        >>> c2 = ContinuedFraction(3, 5)
        >>> c1, c2
        (ContinuedFraction(1, 2), ContinuedFraction(3, 5))
        >>> c1.right_mediant(c2)
        ContinuedFraction(4, 7)
        >>> c1.right_mediant(c2, k=2)
        ContinuedFraction(7, 12)
        >>> c1.right_mediant(c2, k=3)
        ContinuedFraction(10, 17)
        >>> c1.right_mediant(c2, k=100)
        ContinuedFraction(301, 502)
        >>> assert c1.left_mediant(c2, k=2) < c1.right_mediant(c2, k=2)
        >>> assert c1.left_mediant(c2, k=3) < c1.right_mediant(c2, k=3)
        >>> assert c1.left_mediant(c2, k=100) < c1.right_mediant(c2, k=100)
        """
        return self.__class__(right_mediant(self, other, k=k))

    @functools.cache
    def mediant(self, other: Fraction, /) -> ContinuedFraction:
        """Returns the simple mediant of the continued fraction with another continued fraction.
        
        The simple mediant of two rational numbers :math:`r = \\frac{a}{b}`
        and :math:`s = \\frac{c}{d}`, where :math:`b, d, b + d \\neq 0`, is
        defined as:
        
        .. math::

           \\frac{a + c}{b + d}

        The resulting value :math:`\\frac{a + c}{b + d}` is the same as the
        1st order left- or right-mediant of :math:`r = \\frac{a}{b}`
        and :math:`s = \\frac{c}{d}`. So this method would produce the same
        result as the :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.left_mediant`
        or :py:meth:`~continuedfractions.continuedfraction.ContinuedFraction.right_mediant`
        methods where the order :math:`k` is set to :math:`1`.

        For more information consult the
        `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/mediants.html>`_.

        Parameters
        ----------
        other : fractions.Fraction, ContinuedFraction
            The other continued fraction.
        
        Returns
        -------
        ContinuedFraction
            The simple mediant of the original fraction and the other continued
            fraction.

        Examples
        --------
        >>> ContinuedFraction(1, 2).mediant(ContinuedFraction(3, 5))
        ContinuedFraction(4, 7)
        >>> assert ContinuedFraction(1, 2).mediant(ContinuedFraction(3, 5)) == ContinuedFraction(1, 2).left_mediant(ContinuedFraction(3, 5), k=1)
        >>> assert ContinuedFraction(1, 2).mediant(ContinuedFraction(3, 5)) == ContinuedFraction(1, 2).right_mediant(ContinuedFraction(3, 5), k=1)
        """
        return self.__class__(mediant(self, other))


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/continuedfraction.py
    #
    # NOTE: the doctest examples using where `float` or ``decimal.Decimal``
            # values assume a context precision of 28 digits
    decimal.getcontext().prec = 28
    import doctest
    doctest.testmod()
