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

    # To support pattern matching of instances in :py:func:`match` statements
    __match_args__ = ('numerator', 'denominator')

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
        """Validates inputs for object creation.

        Checks whether the arguments are one of the following types:

        * a single :py:class:`int`, or a :py:class:`float` different from :py:data:`math.nan` 
        * a single numeric string (:py:class:`str`)
        * a single :py:class:`fractions.Fraction` or :py:class:`ContinuedFraction` or
          :py:class:`decimal.Decimal` object
        * a pairwise combination of an :py:class:`int`, :py:class:`fractions.Fraction` or
          :py:class:`ContinuedFraction` object, representing the numerator
          and non-zero denominator of a rational number

        Parameters
        ----------
        *args : int, float, str, fractions.Fraction, ContinuedFraction, decimal.Decimal
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
        """Creates objects of this class.

        Creates instances of this class, which represent finite, simple
        continued fractions.

        Arguments must be one of the following types:

        * a single :py:class:`int`, or a :py:class:`float` different from :py:data:`math.nan` 
        * a single numeric string (:py:class:`str`)
        * a single :py:class:`fractions.Fraction` or :py:class:`ContinuedFraction` or
          :py:class:`decimal.Decimal` object
        * a pairwise combination of an :py:class:`int`, :py:class:`fractions.Fraction` or
          :py:class:`ContinuedFraction` object, representing the numerator
          and non-zero denominator of a rational number

        Parameters
        ----------
        *args : int, float, str, fractions.Fraction, ContinuedFraction, decimal.Decimal
            Arguments of the type described above.

        **kwargs
            Any valid keyword arguments for the superclass
            :py:class:`fractions.Fraction`.

        Returns
        -------
        ContinuedFraction
            A new instance of :py:class:`ContinuedFraction`, but not yet initialised
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
        """Returns a :py:class:`ContinuedFraction` object from a sequence of (integer) elements of a continued fraction.

        There is a validation check: all elements must be integers, and all
        elements after the 1st should be positive; otherwise a :py:class:`ValueError`
        is raised.

        Parameters
        ----------
        *elements : int
            An ordered sequence of integer elements of a (finite) continued
            fraction.

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
        """Initialises new :py:class:`ContinuedFraction` instances.

        Parameters
        ----------
        *args : int, float, str, fractions.Fraction, ContinuedFraction, decimal.Decimal
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
        Construct the continued fraction for the rational :math:`\\frac{415}{93}`.

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

        match args:
            # -- case of a single ``ContinuedFraction`` --
            case (ContinuedFraction(),):
                self._elements: Final[tuple[int]] = args[0].elements
            # -- case of a single ``int`` --
            case (int(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(args[0])))
            # -- case of a single ``float`` --
            case (float(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_real(args[0]))
            # -- case of a single (signed or unsigned) numeric string matching --
            # -- ``fractions._RATIONAL_FORMAT`` --
            case (str(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_real(args[0]))            
            # -- case of a single ``fractions.Fraction`` or ``decimal.Decimal``
            case (Fraction(),) | (Decimal(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(*args[0].as_integer_ratio())))
            # -- case of a pair of ``int``s
            case (int(), int(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(args[0], args[1])))
            # -- case of a pairwise combination of ``int``,                --
            # -- ``fractions.Fraction`` or ``ContinuedFraction`` instances --
            case (int() | Fraction() | ContinuedFraction(), int() | Fraction() | ContinuedFraction(),):
                self._elements: Final[tuple[int]] = tuple(continued_fraction_rational(Fraction(*self.as_integer_ratio())))
            # -- any other case - these cases would have been excluded by --
            # ``validate`` but just to be sure                            --
            case _:     # pragma: no cover
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
        """Returns the :py:class:`float` value of the continued fraction.

        The method is cached (with :py:func:`functools.cache`), which makes calls
        after the initial call much faster.

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

        Now construct a :py:class:`ContinuedFraction` object from it, and check the 
        :py:class:`float` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_float()
        3.141592653589793
        """
        return self.numerator / self.denominator

    @functools.cache
    def as_decimal(self) -> Decimal:
        """Returns the :py:class:`decimal.Decimal` value of the continued fraction.

        The method is cached (with :py:func:`functools.cache`), which makes calls
        after the initial call much faster.

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

        Now construct a :py:class:`ContinuedFraction` object from it, and check the 
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
        """tuple[int]: The sequence of elements of the continued fraction.

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
        """int: The order of the continued fraction, which is the number of its elements minus :math:`1`.

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
    @functools.lru_cache
    def khinchin_mean(self) -> Decimal | None:
        """decimal.Decimal: The Khinchin mean of the continued fraction, which is defined as the geometric mean of all its elements after the 1st.

        The Khinchin mean is the geometric mean :math:`\\sqrt[n]{a_1a_2 \\cdots a_n}`
        of all elements of the (finite, simple) continued fraction :math:`[a_0;a_1,\\ldots,a_n]`
        starting from the 1st.

        As in practice all :py:class:`ContinuedFraction` objects will have a finite
        sequence of elements the Khinchin mean as defined above will always
        have a computable value.

        In the special case of integers or fractions representing integers,
        whose continued fraction representations consist of only a single
        element, a null value is returned.

        The property is cached (with :py:func:`functools.lru_cache`), which makes
        calls after the initial call much faster.

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
        if self.order == 1:
            return Decimal(self.elements[-1])

        try:
            return Decimal(statistics.geometric_mean(self.elements[1:]))
        except statistics.StatisticsError:
            return

    @functools.cache
    def convergent(self, k: int, /) -> ContinuedFraction:
        """Returns the :math:`k`-th (simple) convergent of the continued fraction.

        Given a simple continued fraction  :math:`[a_0;a_1,a_2,\\ldots]` the
        :math:`k`-th convergent is defined as:

        .. math::

           C_k = a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2 \\ddots \\cfrac{1}{a_{k-1} + \\cfrac{1}{a_k}}}}

        The result is a :py:class:`fractions.Fraction` object.
        
        The integer :math:`k` is called the order of the convergent, and if 
        :math:`[a_0;a_1,a_2,\\ldots]` is finite of order :math:`n` then it has
        exactly :math:`n + 1` convergents :math:`C_0,C_1,C_2,\\ldots,C_n` where
        the :math:`k`-th convergent :math:`C_k = \\frac{p_k}{q_k}` is given by
        the recurrence relation:

        .. math::
           
           \\begin{align}
           p_k &= a_kp_{k - 1} + p_{k - 2} \\\\
           q_k &= a_kq_{k - 1} + q_{k - 2},        \\hskip{3em}    k \\geq 3
           \\end{align}

        where :math:`p_0 = a_0`, :math:`q_0 = 1`, :math:`p_1 = p_1p_0 + 1`,
        and :math:`q_1 = p_1`.

        The property is cached (with :py:func:`functools.cache`), which makes
        calls after the initial call much faster.

        Parameters
        ----------
        k : int
            The order of the convergent, as described above.

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
    @functools.lru_cache
    def convergents(self) -> MappingProxyType[int, ContinuedFraction]:
        """types.MappingProxyType[int, ContinuedFraction]: An immutable dict of all :math:`k`-order convergents of the continued fraction, keyed by order.

        Each convergent is indexed by its order and is also a
        :py:class:`ContinuedFraction` object.

        The property is cached (with :py:func:`functools.lru_cache`), which makes
        calls after the initial call much faster.

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

    @property
    @functools.lru_cache
    def even_order_convergents(self) -> MappingProxyType[int, ContinuedFraction]:
        """types.MappingProxyType[int, ContinuedFraction]: An immutable dict of all even-order convergents of the continued fraction, keyed/indexed by  order.

        Each convergent is indexed by its order and is also a
        :py:class:`ContinuedFraction` object.

        The property is cached (with :py:func:`functools.lru_cache`), which makes
        calls after the initial call much faster.

        Examples
        --------
        >>> ContinuedFraction('3.245').even_order_convergents
        mappingproxy({0: ContinuedFraction(3, 1), 2: ContinuedFraction(159, 49)})
        """
        return MappingProxyType({
            k: self.convergents[k]
            for k in range(0, self.order + 1, 2)
        })

    @property
    @functools.lru_cache
    def odd_order_convergents(self) -> MappingProxyType[int, ContinuedFraction]:
        """types.MappingProxyType[int, ContinuedFraction]: An immutable dict of all odd-order convergents of the continued fraction, keyed by order.

        Each convergent is indexed by its order and is also a
        :py:class:`ContinuedFraction` object.

        The property is cached (with :py:func:`functools.lru_cache`), which makes
        calls after the initial call much faster.

        Examples
        --------
        >>> ContinuedFraction('3.245').odd_order_convergents
        mappingproxy({1: ContinuedFraction(13, 4), 3: ContinuedFraction(649, 200)})
        """
        return MappingProxyType({
            k: self.convergents[k]
            for k in range(1, self.order + 1, 2)
        })

    @functools.cache
    def remainder(self, k: int, /) -> ContinuedFraction:
        """Returns the :math:`k`-th remainder of the continued fraction.

        The :math:`k`-th remainder :math:`R_k` of a (simple) continued fraction
        :math:`[a_0; a_1,\\ldots]` as the continued fraction :math:`[a_k;a_{k + 1},\\ldots]`,
        obtained from the original by "removing" the elements of the :math:`(k - 1)`-st
        convergent :math:`C_{k - 1} = (a_0,a_1,\\ldots,a_{k - 1})`.

        .. math::

            R_k = a_k + \\cfrac{1}{a_{k + 1} + \\cfrac{1}{a_{k + 2} \\ddots }}

        The method is cached (with :py:func:`functools.cache`), which makes calls
        after the initial call much faster.

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
        return self.__class__.from_elements(*self._elements[k:])

    @property
    @functools.lru_cache
    def remainders(self) -> MappingProxyType[int, ContinuedFraction]:
        """types.MappingProxyType[int, ContinuedFraction]: An immutable dict of all :math:`k`-th remainders of the continued fraction, keyed by order.

        Each remainder is indexed by its order and is also a
        :py:class:`ContinuedFraction` object.

        The property is cached (with :py:func:`functools.lru_cache`), which makes
        calls after the initial call much faster.

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
            fraction, as a :py:class:`ContinuedFraction` object.

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
        return self.__class__(mediant(self, other, dir="left", k=k))

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
            The :math:`k`-th right-mediant of the original fraction and the second
            fraction, as a :py:class:`ContinuedFraction` object.

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
        return self.__class__(mediant(self, other, dir="right", k=k))


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/continuedfraction.py
    #
    import doctest
    doctest.testmod()
