__all__ = [
    'ContinuedFraction',
]


# -- IMPORTS --

# -- Standard libraries --
import math
import sys

from decimal import Decimal
from fractions import Fraction, _RATIONAL_FORMAT
from functools import partial
from pathlib import Path
from types import MappingProxyType
from typing import Any

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.lib import (
    continued_fraction_rational,
    continued_fraction_real,
    fraction_from_elements,
    kth_convergent,
)


class ContinuedFraction(Fraction):
    """
    A simple implementation of continued fractions as Python objects and
    instances of the standard library ``fractions.Fraction`` class, with
    various properties for the continued fraction, including its elements
    (or coefficients), the order, convergents, segments, and remainders.

    Attributes
    ----------
    elements : tuple[int]
        The ordered sequence of elements of the continued fraction.

    order : int
        The order of the continued fraction, defined as the number of
        elements - 1.

    convergents : types.MappingProxyType[int, Fraction]
        An immutable map of all the `k`-order convergents of the continued
        fraction, keyed by `k`.

    Methods
    -------
    as_float()
        The `float` value of the fraction, as given by standard division of
        the numerator by the denominator.

    segment(k: int)
        The `k`th segment of the continued fraction, defined as the continued
        fraction given by its `k`-order convergent, whose elements consist of
        the first `k + 1` two elements of the original continued fraction.

    remainder(k: int)
        The `k`th remainder of the continued fraction, defined as the continued
        fraction given by the difference between the original continued
        fraction and its `(k - 1)`-order convergent (equivalently, the
        `(k - 1)` order segment, as defined above).

    mediant(other: Fraction)
        The continued fraction of the rational number formed by taking the
        pairwise sum of the numerators and denominators of the original
        continued fraction and a second fraction (`other`). The resulting
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

    Inspect the elements, order, convergents, segments and remainders

    >>> cf.elements
    (3, 4, 12, 4)
    >>> cf.order
    3
    >>> cf.convergents
    mappingproxy({0: Fraction(3, 1), 1: Fraction(13, 4), 2: Fraction(159, 49), 3: Fraction(649, 200)})
    >>> cf.segment(1)
    ContinuedFraction(13, 4)
    >>> cf.remainder(1)
    ContinuedFraction(200, 49)

    Check some properties of the segments and remainders

    >>> assert cf.remainder(1) == 1 / (cf - cf.convergents[0])

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

    # Class attribute to store an error message for input errors
    __valid_inputs_msg__ = (
        "Only single integers, non-nan floats, numeric strings, \n"
        "`fractions.Fraction`, or `decimal.Decimal` objects; or two \n"
        "integers or two `fractions.Fraction` objects or a pairwise \n"
        "combination of these, representing the numerator and non-zero \n"
        "denominator, respectively, of a rational fraction, are valid."
    )

    @classmethod
    def validate(cls, *args: int | float | str | Fraction | Decimal, **kwargs: Any) -> None:
        """
        Checks whether the arguments are one of the following types:

        * a single integer or a non-nan float
        * a single numeric string
        * a single `fractions.Fraction` or `decimal.Decimal` object
        * two integers or `fractions.Fraction` objects, or a combination of an
          integer and a `fractions.Fraction` object, representing the numerator
          and non-zero denominator of a rational fraction

        Parameters
        ----------
        *args: int or float or str or fractions.Fraction or decimal.Decimal
            Arguments of the type described above.

        Raises
        ------
        ValueError
            If validation fails.

        Notes
        -----
        To avoid recursion errors validation excludes `ContinuedFraction`
        instances, and for the same reason convergents of a
        `ContinuedFraction` instance are given as `fractions.Fraction`
        instances.

        Examples
        --------
        >>> ContinuedFraction.validate(100)
        >>> ContinuedFraction.validate(3, -2)

        >>> ContinuedFraction.validate(1, -2.0)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `decimal.Decimal` objects; or two 
        integers or two `fractions.Fraction` objects or a pairwise 
        combination of these, representing the numerator and non-zero 
        denominator, respectively, of a rational fraction, are valid.

        >>> ContinuedFraction.validate(-.123456789)
        >>> ContinuedFraction.validate('-.123456789')
        >>> ContinuedFraction.validate('-649/200')
        >>> ContinuedFraction.validate(-3/2)

        >>> ContinuedFraction.validate(-3, 0)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `decimal.Decimal` objects; or two 
        integers or two `fractions.Fraction` objects or a pairwise 
        combination of these, representing the numerator and non-zero 
        denominator, respectively, of a rational fraction, are valid.

        >>> ContinuedFraction.validate(Fraction(-415, 93))
        >>> ContinuedFraction.validate(Decimal('12345.6789'))
        >>> ContinuedFraction.validate(Decimal(12345.6789))

        >>> ContinuedFraction.validate(Fraction(3, 2), 2.5)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `decimal.Decimal` objects; or two 
        integers or two `fractions.Fraction` objects or a pairwise 
        combination of these, representing the numerator and non-zero 
        denominator, respectively, of a rational fraction, are valid.
        """
        if len(args) not in [1, 2]:
            raise ValueError(cls.__valid_inputs_msg__)

        if (
            len(args) == 1 and
            not set(map(type, args)).issubset(
                [int, float, str, Fraction, Decimal]
            )
        ):
            raise ValueError(cls.__valid_inputs_msg__)

        if any(isinstance(arg, float) and math.isnan(arg) for arg in args):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args) == 1 and isinstance(args[0], str) and not _RATIONAL_FORMAT.match(args[0]):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args) == 2 and not set(map(type, args)).issubset([int, Fraction]):
            raise ValueError(cls.__valid_inputs_msg__)

        if len(args) == 2 and args[1] == 0:
            raise ValueError(cls.__valid_inputs_msg__)

    def __new__(cls, *args:  int | float | str | Fraction | Decimal, **kwargs: Any) -> Fraction:
        """
        Creates instances of this class, which represent finite, simple
        continued fractions.

        Arguments must be one of the following types:

        * a single integer or a non-nan float
        * a single numeric string
        * a single `fractions.Fraction` or `decimal.Decimal` object
        * two integers or `fractions.Fraction` objects, or a combination of an
          integer and a `fractions.Fraction` object, representing the numerator
          and non-zero denominator of a rational fraction

        Parameters
        ----------
        *args: int or float or str or fractions.Fraction or decimal.Decimal
            Arguments of the type described above.

        **kwargs
            Any valid keyword arguments for the superclass
            `fractions.Fraction`.

        Returns
        -------
        ContinuedFraction
            A new instance of `ContinuedFraction`, but not yet initialised with
            the class-specific attributes and properties.

        Examples
        --------
        >>> ContinuedFraction(100, 2)
        ContinuedFraction(50, 1)

        >>> ContinuedFraction(1, -2.0)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `decimal.Decimal` objects; or two 
        integers or two `fractions.Fraction` objects or a pairwise 
        combination of these, representing the numerator and non-zero 
        denominator, respectively, of a rational fraction, are valid.

        >>> ContinuedFraction('-.123456789')
        ContinuedFraction(-123456789, 1000000000)

        >>> ContinuedFraction(.3, -2)
        Traceback (most recent call last):
        ...
        ValueError: Only single integers, non-nan floats, numeric strings, 
        `fractions.Fraction`, or `decimal.Decimal` objects; or two 
        integers or two `fractions.Fraction` objects or a pairwise 
        combination of these, representing the numerator and non-zero 
        denominator, respectively, of a rational fraction, are valid.

        >>> ContinuedFraction(Fraction(-415, 93))
        ContinuedFraction(-415, 93)
        """
        try:
            cls.validate(*args, **kwargs)
        except ValueError:
            raise

        return super().__new__(cls, *args, **kwargs)

    @classmethod
    def from_elements(cls, *elements: int) -> Fraction:
        """
        Returns a `ContinuedFraction` instance from a sequence of (integer)
        elements of a continued fraction.

        Parameters
        ----------
        *elements: int
            An ordered sequence of elements of a (finite) continued fraction.

        Returns
        -------
        ContinuedFraction
            A new and fully initialised instance of `ContinuedFraction` with
            the given element sequence.

        Examples
        --------
        Constructing a continued fraction for the rational `649/200` using the
        element sequence `(3, 4, 12, 4)`.

        >>> c1 = ContinuedFraction.from_elements(3, 4, 12, 4)
        >>> c1
        ContinuedFraction(649, 200)

        Constructing the continued fraction of the inverse rational `200/649`
        using the element sequence `(0, 3, 4, 12, 4)`.

        >>> c2 = ContinuedFraction.from_elements(0, 3, 4, 12, 4)
        >>> c2
        ContinuedFraction(200, 649)
        """
        return cls(fraction_from_elements(*elements))

    def __init__(self, *args:  int | float | str | Fraction | Decimal, **kwargs: Any) -> None:
        """
        Initialises new `ContinuedFraction` instances with attributes and
        properties for their elements, order, convergents, segments and
        remainders.

        Parameters
        ----------
        *args : int or float or str or fractions.Fraction or decimal.Decimal
            Arguments of the type described above.

        **kwargs
            Any valid keyword arguments for the superclass fractions.Fraction

        Raises
        ------
        ValueError
            If there are arguments that have somehow passed the validation
            check, but do not fall into one of the types described above.

        Examples
        --------
        Construct the continued fraction for the rational `415/93`.

        >>> cf = ContinuedFraction(415, 93)
        >>> cf
        ContinuedFraction(415, 93)

        Inspect the elements, order, convergents, segments and remainders

        >>> cf.elements
        (4, 2, 6, 7)
        >>> cf.order
        3
        >>> cf.convergents
        mappingproxy({0: Fraction(4, 1), 1: Fraction(9, 2), 2: Fraction(58, 13), 3: Fraction(415, 93)})
        >>> cf.segment(0), cf.segment(1), cf.segment(2), cf.segment(3)
        (ContinuedFraction(4, 1), ContinuedFraction(9, 2), ContinuedFraction(58, 13), ContinuedFraction(415, 93))
        >>> cf.remainder(0), cf.remainder(1), cf.remainder(2), cf.remainder(3)
        (ContinuedFraction(415, 93), ContinuedFraction(93, 43), ContinuedFraction(43, 7), ContinuedFraction(7, 1))

        Check some properties of the segments and remainders

        >>> assert cf.remainder(1) == 1 / (cf - cf.convergents[0])
        """
        super().__init__()

        if len(args) == 1 and isinstance(args[0], int):
            self._elements = tuple(continued_fraction_rational(args[0], 1))
        elif len(args) == 1 and isinstance(args[0], float):
            self._elements = tuple(continued_fraction_real(args[0]))
        elif len(args) == 1 and isinstance(args[0], str) and _RATIONAL_FORMAT.match(args[0]) and '/' in args[0]:
            self._elements = tuple(continued_fraction_rational(*self.as_integer_ratio()))
        elif len(args) == 1 and isinstance(args[0], str) and _RATIONAL_FORMAT.match(args[0]) and '/' not in args[0]:
            self._elements = tuple(continued_fraction_real(args[0]))
        elif len(args) == 1 and (isinstance(args[0], Fraction) or isinstance(args[0], Decimal)):
            self._elements = tuple(continued_fraction_rational(*args[0].as_integer_ratio()))
        elif len(args) == 2 and set(map(type, args)) == set([int]):
            self._elements = tuple(continued_fraction_rational(args[0], args[1]))
        elif len(args) == 2 and set(map(type, args)).issubset([int, Fraction]):
            self._elements = tuple(continued_fraction_rational(*self.as_integer_ratio()))
        else:      # pragma: no cover
            raise ValueError(self.__class__.__valid_inputs_msg__)

        _kth_convergent = partial(kth_convergent, *self._elements)
        self._convergents = MappingProxyType(
            {
                k: _kth_convergent(k=k)
                for k in range(len(self._elements))
            }
        )

    def __add__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__add__(other))

    def __radd__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__radd__(other))

    def __sub__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__sub__(other))

    def __rsub__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__rsub__(other))

    def __mul__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__mul__(other))

    def __rmul__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__rmul__(other))

    def __truediv__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__truediv__(other))

    def __rtruediv__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__rtruediv__(other))

    def __floordiv__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__floordiv__(other))

    def __rfloordiv__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__rfloordiv__(other))

    def __divmod__(self, other: Fraction, /) -> Fraction:
        quo, rem = super().__divmod__(other)

        return self.__class__(quo), self.__class__(rem)

    def __rdivmod__(self, other: Fraction, /) -> Fraction:
        quo, rem = super().__rdivmod__(other)
        
        return self.__class__(quo), self.__class__(rem)

    def __pow__(self, other: Fraction, /) -> Fraction:
        return self.__class__(super().__pow__(other))

    def __rpow__(self, other: Fraction, /) -> Fraction:
        return self.__class__(Fraction(other).__pow__(self))

    def __pos__(self) -> Fraction:
        return self.__class__(super().__pos__())

    def __neg__(self) -> Fraction:
        return self.__class__(super().__neg__())

    def __abs__(self) -> Fraction:
        return self.__class__(super().__abs__())


    def as_float(self) -> float:
        """
        Returns the `float` value of the continued fraction, using standard
        division (`/`) of the numerator by the denominator.

        Returns
        -------
        float
            The `float` representation of the continued fraction.

        Examples
        --------
        >>> import math
        >>> math.pi
        3.141592653589793

        Now construct a `ContinuedFraction` object from it, and check the 
        `float` value.

        >>> cf = ContinuedFraction(math.pi)
        >>> cf
        ContinuedFraction(884279719003555, 281474976710656)
        >>> cf.as_float()
        3.141592653589793
        """
        return self.numerator / self.denominator

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
                  of its elements + `1`.

        Returns
        -------
        int
            The order of the continued fraction, which is the number of its
            elements + `1`.

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
    def convergents(self) -> MappingProxyType[int, Fraction]:
        """
        Property: the map of all convergents of the continued fraction, keyed
                  by the orders `0`,`1`,...,`n`, where `n` is the order of
                  the continued fraction.

        Returns
        -------
        types.MappingProxyType[int, fractions.Fraction]
            The map of all convergents of the continued fraction, keyed
            by their orders.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.convergents
        mappingproxy({0: Fraction(0, 1), 1: Fraction(1, 8), 2: Fraction(9, 73), 3: Fraction(10, 81), 4: Fraction(219, 1774), 5: Fraction(229, 1855), 6: Fraction(448, 3629), 7: Fraction(2469, 20000)})
        """
        return self._convergents

    def segment(self, k: int, /) -> Fraction:
        """
        The `k`th segment of the continued fraction, defined as the continued
        fraction given by its `k`-order convergent, whose elements consist of
        the first `k + 1` two elements of the original continued fraction.

        Parameters
        ----------
        k : int
            The index of the segment, as described above.

        Returns
        -------
        ContinuedFraction
            A new `ContinuedFraction` instance representing the `k`th segment
            of the original continued fraction, as described above.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.segment(2)
        ContinuedFraction(9, 73)
        """
        return self.__class__.from_elements(*self._elements[:k + 1])

    def remainder(self, k: int, /) -> Fraction:
        """
        The `k`th remainder of the continued fraction, defined as the continued
        fraction given by the difference between the original continued
        fraction and its `(k - 1)`-order convergent (equivalently, the
        `(k - 1)`-order segment, as defined above).

        Parameters
        ----------
        k : int
            The index of the remainder, as described above.

        Returns
        -------
        ContinuedFraction
            A new `ContinuedFraction` instance representing the `k`th remainder
            of the original continued fraction, as described above.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.remainder(2)
        ContinuedFraction(2469, 248)
        """
        return self.__class__.from_elements(*self._elements[k:])

    def mediant(self, other: Fraction) -> Fraction:
        """
        The continued fraction of the rational number formed by taking the
        pairwise sum of the numerators and denominators of the original
        continued fraction and a second fraction (`other`). The resulting
        fraction has the property that its value lies between its two
        constituents.        

        Parameters
        ----------
        other : fractions.Fraction or ContinuedFraction
            The second fraction to use to calculate the mediant with the
            first.

        Returns
        -------
        ContinuedFraction
            The mediant of the original and the second fractions, as a
            `ContinuedFraction` instance.

        Examples
        --------
        >>> cf = ContinuedFraction('.12345')
        >>> cf
        ContinuedFraction(2469, 20000)
        >>> cf.mediant(Fraction('.1235'))
        ContinuedFraction(679, 5500)
        """
        return self.__class__(
            self.numerator + other.numerator,
            self.denominator + other.denominator
        )



if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/continuedfraction.py
    #
    import doctest
    doctest.testmod()
