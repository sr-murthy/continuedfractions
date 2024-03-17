from __future__ import annotations


__all__ = [
    'ContinuedFraction',
]


# -- IMPORTS --

# -- Standard libraries --
import functools
import math
import statistics
import sys

from decimal import Decimal
from fractions import Fraction, _RATIONAL_FORMAT
from pathlib import Path
from types import MappingProxyType
from typing import Any, Final

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.lib import (
    continued_fraction_rational,
    continued_fraction_real,
    fraction_from_elements,
    convergent,
    mediant,
)


class ContinuedFraction(Fraction):
    """
    An implementation of simple continued fractions as Python objects and
    instances of the standard library ``fractions.Fraction`` class, with
    various properties for the continued fraction, including its elements
    (or coefficients), the order, convergents, and remainders.

    The term "simple continued fraction" denotes a specific type of continued
    fraction where the fractional terms only have numerators of ``1``.

    Attributes
    ----------
    elements : `tuple[int]`
        The ordered sequence of elements of the continued fraction.

    order : `int`
        The order of the continued fraction, defined as the number of
        elements - ``1``.

    khinchin_mean : `decimal.Decimal`
        The geometric mean of all elements of the continued fraction, starting
        from ``a_1``, excluding the leading element ``a_0``.

    Methods
    -------
    as_float()
        The ``float`` value of the fraction, as given by standard division of
        the numerator by the denominator.

    convergent(k: int)
        The ``k``-th (simple) convergent of the continued fraction, defined as the
        finite simple continued fraction of order ``k`` consisting of the first
        ``k + 1`` elements of the original continued fraction.

    remainder(k: int)
        The ``k``-th remainder of the continued fraction, defined as the continued
        fraction whose elements start from the ``k``-th element of the sequence
        of elements of the original continued fraction.

    mediant(other: Fraction)
        The continued fraction of the rational number formed by taking the
        pairwise sum of the numerators and denominators of the original
        continued fraction and a second fraction (``other``). The resulting
        fraction has the property that its value lies between the two
        constituents.

    Examples
    --------
    Construct the continued fraction for the rational `649/200`.

    >>> cf = ContinuedFraction(649, 200)
    >>> cf
    ContinuedFraction(649, 200)
    >>> cf.as_float()
    3.245

    Inspect the elements, order, convergents, and remainders

    >>> cf.elements
    (3, 4, 12, 4)
    >>> cf.order
    3
    >>> cf.convergent(0), cf.convergent(1), cf.convergent(2), cf.convergent(3)
    (ContinuedFraction(3, 1), ContinuedFraction(13, 4), ContinuedFraction(159, 49), ContinuedFraction(649, 200))
    >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
    (ContinuedFraction(649, 200), ContinuedFraction(200, 49), ContinuedFraction(49, 4), ContinuedFraction(4, 1))

    Check some properties of the convergents and remainders

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

    # Class attribute to store an error message for input errors
    __valid_inputs_msg__ = (
        "Only single integers, non-nan floats, numeric strings, \n"
        "`fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` \n"
        "objects; or a pairwise combination of an integer, \n"
        "`fractions.Fraction` or ``ContinuedFraction`` object, representing \n"
        "the numerator and non-zero denominator, respectively, of a rational \n"
        "fraction, are valid."
    )

    @classmethod
    def validate(cls, *args_: int | float | str | Fraction | ContinuedFraction | Decimal, **kwargs: Any) -> None:
        """
        Checks whether the arguments are one of the following types:

        * a single ``int`` or a non-``nan`` ``float``
        * a single numeric string (``str``)
        * a single ``fractions.Fraction`` or ``ContinuedFraction`` or
          ``decimal.Decimal`` object
        * a pairwise combination of an ``int``, ``fractions.Fraction`` or
          ``ContinuedFraction`` object, representing the numerator
          and non-zero denominator of a rational fraction

        Parameters
        ----------
        *args: `int`, `float` `str`, `fractions.Fraction`, `ContinuedFraction`, `decimal.Decimal`
            Arguments subject to the validation rules described above.

        Raises
        ------
        ValueError
            If validation fails.

        Examples
        --------
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
        """
        if len(args_) not in [1, 2]:
            raise ValueError(cls.__valid_inputs_msg__)

        if (
            len(args_) == 1 and
            not set(map(type, args_)).issubset(
                [int, float, str, Fraction, ContinuedFraction, Decimal]
            )
        ):
            raise ValueError(cls.__valid_inputs_msg__)

        if any(isinstance(arg, float) and math.isnan(arg) for arg in args_):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args_) == 1 and isinstance(args_[0], str) and not _RATIONAL_FORMAT.match(args_[0]):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args_) == 2 and not set(map(type, args_)).issubset([int, Fraction, ContinuedFraction]):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args_) == 2 and args_[1] == 0:
            raise ValueError(cls.__valid_inputs_msg__)

    def __new__(cls, *args:  int | float | str | Fraction | ContinuedFraction | Decimal, **kwargs: Any) -> ContinuedFraction:
        """
        Creates instances of this class, which represent finite, simple
        continued fractions.

        Arguments must be one of the following types:

        * a single ``int`` or a non-``nan`` ``float``
        * a single numeric string (``str``)
        * a single ``fractions.Fraction`` or ``ContinuedFraction`` or
          ``decimal.Decimal`` object
        * a pairwise combination of an ``int``, ``fractions.Fraction`` or
          ``ContinuedFraction`` object, representing the numerator
          and non-zero denominator of a rational fraction

        Parameters
        ----------
        *args: `int`, `float`, `str`, `fractions.Fraction`, `ContinuedFraction`, `decimal.Decimal`
            Arguments of the type described above.

        **kwargs
            Any valid keyword arguments for the superclass
            ``fractions.Fraction``.

        Returns
        -------
        ContinuedFraction
            A new instance of ``ContinuedFraction``, but not yet initialised
            with the class-specific attributes and properties.

        Examples
        --------
        >>> ContinuedFraction(100, 2)
        ContinuedFraction(50, 1)

        >>> ContinuedFraction(1, -2.0)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` 
        objects; or a pairwise combination of an integer, 
        `fractions.Fraction` or ``ContinuedFraction`` object, representing 
        the numerator and non-zero denominator, respectively, of a rational 
        fraction, are valid.

        >>> ContinuedFraction('-.123456789')
        ContinuedFraction(-123456789, 1000000000)

        >>> ContinuedFraction(.3, -2)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `ContinuedFraction`, or  `decimal.Decimal` 
        objects; or a pairwise combination of an integer, 
        `fractions.Fraction` or ``ContinuedFraction`` object, representing 
        the numerator and non-zero denominator, respectively, of a rational 
        fraction, are valid.

        >>> ContinuedFraction(Fraction(-415, 93))
        ContinuedFraction(-415, 93)
        """
        try:
            cls.validate(*args, **kwargs)
        except ValueError:
            raise

        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def from_elements(cls, *elements: int) -> ContinuedFraction:
        """
        Returns a ``ContinuedFraction`` instance from a sequence of (integer)
        elements of a continued fraction.

        There is a validation check: all elements must be integers, and all
        elements after the 1st should be positive; otherwise a ``ValueError``
        is raised.

        Parameters
        ----------
        *elements: `int`
            An ordered sequence of integer elements of a (finite) continued
            fraction.

        Returns
        -------
        ContinuedFraction
            A new and fully initialised instance of ``ContinuedFraction`` with
            the given element sequence.

        Raises
        ------
        ValueError
            If any elements are not integers, or any elements after the 1st
            are not positive.

        Examples
        --------
        Constructing a continued fraction for the rational ``649/200`` using
        the element sequence ``(3, 4, 12, 4)``.

        >>> c1 = ContinuedFraction.from_elements(3, 4, 12, 4)
        >>> c1
        ContinuedFraction(649, 200)

        Constructing the continued fraction of the inverse rational ``200/649``
        using the element sequence ``(0, 3, 4, 12, 4)``.

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
        # Create a new ``ContinuedFraction`` object from the given elements
        # and initialise with elements only - no need to initialise via
        # ``__init__``
        if any(not isinstance(elem, int) or (elem <= 0 and i > 0) for i, elem in enumerate(elements)):
            raise ValueError(
                "Continued fraction elements must be integers, and all "
                "elements after the 1st must be positive"
            )

        obj = cls(fraction_from_elements(*elements))
        obj._elements = elements
    
        return obj

    def __init__(self, *args:  int | float | str | Fraction | ContinuedFraction | Decimal, **kwargs: Any) -> None:
        """
        Initialises new ``ContinuedFraction`` instances with attributes and
        properties for their elements, order, convergents, and remainders.

        Parameters
        ----------
        *args : `int`, `float`, `str`, `fractions.Fraction`, `ContinuedFraction`, `decimal.Decimal`
            Arguments of the type described above.

        **kwargs
            Any valid keyword arguments for the superclass
            ``fractions.Fraction``

        Raises
        ------
        ValueError
            If there are arguments that have somehow passed the validation
            check, but do not fall into one of the types described above.

        Examples
        --------
        Construct the continued fraction for the rational ``415/93``.

        >>> cf = ContinuedFraction(415, 93)
        >>> cf
        ContinuedFraction(415, 93)

        Inspect the elements, order, convergents, and remainders

        >>> cf.elements
        (4, 2, 6, 7)
        >>> cf.order
        3
        >>> cf.convergent(0), cf.convergent(1), cf.convergent(2), cf.convergent(3)
        (ContinuedFraction(4, 1), ContinuedFraction(9, 2), ContinuedFraction(58, 13), ContinuedFraction(415, 93))
        >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
        (ContinuedFraction(415, 93), ContinuedFraction(93, 43), ContinuedFraction(43, 7), ContinuedFraction(7, 1))

        Check some properties of the convergents and remainders

        >>> assert cf.remainder(1) == 1 / (cf - cf.convergent(0))
        """
        super().__init__()

        if len(args) == 1 and isinstance(args[0], ContinuedFraction):
            self._elements: Final[tuple[int]] = args[0].elements
        if len(args) == 1 and isinstance(args[0], int):
            self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(args[0])))
        elif len(args) == 1 and isinstance(args[0], float):
            self._elements: Final[tuple[int]] = tuple(continued_fraction_real(args[0]))
        elif len(args) == 1 and isinstance(args[0], str) and _RATIONAL_FORMAT.match(args[0]) and '/' in args[0]:
            self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(*self.as_integer_ratio())))
        elif len(args) == 1 and isinstance(args[0], str) and _RATIONAL_FORMAT.match(args[0]) and '/' not in args[0]:
            self._elements: Final[tuple[int]] = tuple(continued_fraction_real(args[0]))
        elif len(args) == 1 and (isinstance(args[0], Fraction) or isinstance(args[0], Decimal)):
            self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(*args[0].as_integer_ratio())))
        elif len(args) == 2 and set(map(type, args)) == set([int]):
            self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(args[0], args[1])))
        elif len(args) == 2 and set(map(type, args)).issubset([int, Fraction, ContinuedFraction]):
            self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(*self.as_integer_ratio())))
        else:      # pragma: no cover
            raise ValueError(self.__class__.__valid_inputs_msg__)

    def __add__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__add__(other))

    def __radd__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__radd__(other))

    def __sub__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__sub__(other))

    def __rsub__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__rsub__(other))

    def __mul__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__mul__(other))

    def __rmul__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__rmul__(other))

    def __truediv__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__truediv__(other))

    def __rtruediv__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__rtruediv__(other))

    def __floordiv__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__floordiv__(other))

    def __rfloordiv__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__rfloordiv__(other))

    def __divmod__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        quo, rem = super().__divmod__(other)

        return self.__class__(quo), self.__class__(rem)

    def __rdivmod__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        quo, rem = super().__rdivmod__(other)
        
        return self.__class__(quo), self.__class__(rem)

    def __pow__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(super().__pow__(other))

    def __rpow__(self, other: int | float | Fraction | ContinuedFraction, /) -> ContinuedFraction:
        return self.__class__(Fraction(other).__pow__(self))

    def __pos__(self) -> ContinuedFraction:
        return self.__class__(super().__pos__())

    def __neg__(self) -> ContinuedFraction:
        return self.__class__(super().__neg__())

    def __abs__(self) -> ContinuedFraction:
        return self.__class__(super().__abs__())

    @functools.cache
    def as_float(self) -> float:
        """
        Returns the ``float`` value of the continued fraction, using standard
        division (``/``) of the numerator by the denominator.

        The method is cached (with ``functools.cache``), which makes calls
        after the initial call much faster.

        Returns
        -------
        float
            The ``float`` representation of the continued fraction.

        Examples
        --------
        >>> import math
        >>> math.pi
        3.141592653589793

        Now construct a ``ContinuedFraction`` object from it, and check the 
        ``float`` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_float()
        3.141592653589793
        """
        return self.numerator / self.denominator

    @functools.cache
    def as_decimal(self) -> Decimal:
        """
        Returns the ``float`` value of the continued fraction, using standard
        division (``/``) of the numerator by the denominator.

        The method is cached (with ``functools.cache``), which makes calls
        after the initial call much faster.

        Returns
        -------
        float
            The `float` representation of the continued fraction.

        Examples
        --------
        >>> import math
        >>> math.pi
        3.141592653589793

        Now construct a ``ContinuedFraction` object from it, and check the 
        ``float`` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_float()
        3.141592653589793
        """
        return Decimal(self.numerator) / Decimal(self.denominator)

    @property
    def elements(self) -> tuple[int]:
        """
        Property: the element sequence of the continued fraction.

        Returns
        -------
        tuple[int]
            The element sequence of the continued fraction.

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
        """
        Property: the order of the continued fraction, which is the number
                  of its elements + ``1``.

        Returns
        -------
        int
            The order of the continued fraction, which is the number of its
            elements + ``1``.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.order
        7
        """
        return len(self._elements[1:])

    @property
    @functools.lru_cache
    def khinchin_mean(self) -> Decimal | None:
        """
        Property: the Khinchin mean of the continued fraction, which we define
                  as the geometric mean of all its elements starting from
                  ``a_1``, so that is,:
                  ::

                    a_1, a_2, ...

                  The leading element ``a_0`` is excluded.

                  As in practice all ``ContinuedFraction`` objects will have a
                  finite sequence of elements the Khinchin mean as defined
                  above will always have a computable value.

                  In the special case of integers or fractions representing
                  integers, whose continued fraction representations consist of
                  only a single element, a null value is returned.

                  The property is cached (with ``functools.lru_cache``), which
                  makes calls after the initial call much faster.

        Returns
        -------
        decimal.Decimal
            The geometric mean of all elements of the continued fraction,
            excluding the leading term ``a_0``, so the geometric mean of
            the sequence ``a_1, a2, ...``.

        Examples
        --------
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
        if self.order == 1:
            return Decimal(self.elements[-1])

        try:
            return Decimal(statistics.geometric_mean(self.elements[1:]))
        except statistics.StatisticsError:
            return

    @functools.cache
    def convergent(self, k: int, /) -> ContinuedFraction:
        """
        Returns a ``ContinuedFraction`` object for the `k`-th (simple)
        convergent of the continued fraction, which is defined as the finite 
        simple continued fraction of order ``k`` formed from the first
        ``k + 1`` elements ``a_0, a_1, ... , a_k``.

        The property is cached (with ``functools.cache``), which makes
        calls after the initial call much faster.

        Parameters
        ----------
        k : `int`
            The order of the convergent, as described above.

        Returns
        -------
        ContinuedFraction
            A new ``ContinuedFraction`` instance representing the ``k``-th
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
        return self.__class__(convergent(*self._elements, k=k))

    @property
    @functools.lru_cache
    def convergents(self) -> MappingProxyType[int, ContinuedFraction]:
        """
        Property: An immutable dict of all ``k``-order convergents of the
                  continued fraction, keyed/indexed by ``k``. Each convergent
                  is also a ``ContinuedFraction`` object.

                  The property is cached (with ``functools.lru_cache``), which
                  makes calls after the initial call much faster.

        Returns
        -------
        ContinuedFraction
            An immutable dict of all ``k``-order convergents of the continued
            fraction, keyed/index by ``k``. Each convergent is also a
            ``ContinuedFraction`` object.

        Examples
        --------
        >>> cf = ContinuedFraction('3.245')
        >>> cf.convergents
        mappingproxy({0: ContinuedFraction(3, 1), 1: ContinuedFraction(13, 4), 2: ContinuedFraction(159, 49), 3: ContinuedFraction(649, 200)})
        >>> cf.convergents[0], cf.convergents[2]
        (ContinuedFraction(3, 1), ContinuedFraction(159, 49))
        """
        return MappingProxyType({
            k: self.convergent(k)
            for k in range(self.order + 1)
        })

    @functools.cache
    def remainder(self, k: int, /) -> ContinuedFraction:
        """
        The ``k``-th remainder of the continued fraction, defined as the continued
        fraction consisting of the elements starting from the ``k``-th element
        of the sequence of elements of the original continued fraction: so the
        ``k``-th remainder has the elements ``a_k, a_{k + 1}, ...``.

        The method is cached (with ``functools.cache``), which makes calls
        after the initial call much faster.

        Parameters
        ----------
        k : `int`
            The index of the remainder, as described above.

        Returns
        -------
        ContinuedFraction
            A new ``ContinuedFraction`` instance representing the ``k``-th
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
        return self.__class__.from_elements(*self._elements[k:])

    @property
    @functools.lru_cache
    def remainders(self) -> MappingProxyType[int, ContinuedFraction]:
        """
        Property: An immutable dict of all ``k``-th remainders of the
                  continued fraction, keyed/indexed by ``k``. Each remainder
                  is also a ``ContinuedFraction`` object.

                  The property is cached (with ``functools.lru_cache``), which
                  makes calls after the initial call much faster.

        Returns
        -------
        ContinuedFraction
            An immutable dict of all ``k``-th remainders of the continued
            fraction, keyed/index by ``k``. Each remainder is also a
            ``ContinuedFraction`` object.

        Examples
        --------
        >>> cf = ContinuedFraction('3.245')
        >>> cf.remainders
        mappingproxy({0: ContinuedFraction(649, 200), 1: ContinuedFraction(200, 49), 2: ContinuedFraction(49, 4), 3: ContinuedFraction(4, 1)})
        >>> cf.remainders[0], cf.remainders[2]
        (ContinuedFraction(649, 200), ContinuedFraction(49, 4))
        """
        return MappingProxyType({
            k: self.remainder(k)
            for k in range(self.order + 1)
        })

    @functools.cache
    def mediant(self, other: Fraction, /, *, dir="right", k: int = 1) -> ContinuedFraction:
        """
        Returns the ``k``-th left- or right-mediant of this
        ``ContinuedFraction`` object with another ``fractions.Fraction``
        object.
        
        The "direction" of the mediant is specified with ``dir``, and can only
        be one of ``"left"`` or  ``"right"``.

        For a positive integer ``k``, the ``k``-th left-mediant of rational numbers
        ``r = a / b`` and ``s = c / d``, where ``b`` and ``d`` are non-zero,
        can be defined as:
        ::

            (ka + c) / (kb + d)

        while the ``k``-th right mediant can be defined as:
        ::

            (a + kc) / (b + kd)

        If we assume that ``r < s`` and ``bd > 0`` then the ``k``-th left mediants have
        the property that:
        ::

            a / b < ... < (3a + c) / (3b + d) < (2a + c) / (2b + d) < (a + c) / (b + d) < c / d
            a / b < (a + c) / (b + d) < (a + 2c) / (b + 2d) < (a + 3c) / (b + 3d) < ... c / d

        That is, the left mediants form a strictly decreasing sequence, actually
        converging to ``a / b``, while the right mediants form a strictly
        increasing sequence of, actually converging to ``c / d``.

        For the left mediant use ``dir="left"``, while for the right use
        `dir='right'`. The default is ``dir="right"``. For ``k = 1`` the left
        and right mediants are the same.

        The method is cached (with ``functools.cache``), which makes calls
        after the initial call much faster.

        Parameters
        ----------
        other : `fractions.Fraction`, `ContinuedFraction`
            The second fraction to use to calculate the ``k``-th mediant with
            the first.
        
        k : `int`, default=1
            The order of the mediant, as defined above.        

        Returns
        -------
        ContinuedFraction
            The ``k``-th mediant of the original fraction and the second
            fraction, as a ``ContinuedFraction`` instance.

        Examples
        --------
        >>> c1 = ContinuedFraction('.5')
        >>> c2 = ContinuedFraction(3, 5)
        >>> c1, c2
        (ContinuedFraction(1, 2), ContinuedFraction(3, 5))
        >>> c1.mediant(c2)
        ContinuedFraction(4, 7)
        >>> c1.mediant(c2, k=2)
        ContinuedFraction(7, 12)
        >>> c1.mediant(c2, k=3)
        ContinuedFraction(10, 17)
        """
        return self.__class__(mediant(self, other, dir=dir, k=k))


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/continuedfraction.py
    #
    import doctest
    doctest.testmod()
