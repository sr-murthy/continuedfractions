__all__ = [
    'continued_fraction_rational',
    'continued_fraction',
    'ContinuedFraction',
]


# -- IMPORTS --

# -- Standard libraries --
import re

from decimal import Decimal
from fractions import Fraction
from typing import Any, Generator

# -- 3rd party libraries --

# -- Internal libraries --


def continued_fraction_rational(x: int, y: int) -> Generator[int, None, None]:
    """
    Generates the (integer) elements of the continued fraction representation
    of a non-negative rational number ``x/y``, with numerator ``x >= 0`` and
    denominator ``y >= 0``.

    If ``y``, the denominator, is zero a ``ValueError`` is raised.
    """
    num, denum = x, y

    if denum == 0:
        raise ValueError("The denominator must be a positive integer")
 
    if num < 0 and denum < 0:
        num, denum = -num, -denum

    if num < 0 or denum < 0:
        raise ValueError("The rational number must be non-negative")

    quo, rem = divmod(num, denum)
    yield quo

    while rem > 0:
        num, denum = denum, rem
        quo, rem = divmod(num, denum)
        yield quo


def continued_fraction(x: int | float | str) -> Generator[int, None, None]:
    """
    Generates the (integer) elements of the continued fraction representation
    of ``x``, which is either an integer, float or a string representation of
    an integer or a float.
    """
    num, denum = Decimal(str(x)).as_integer_ratio()

    for elem in continued_fraction_rational(num, denum):
        yield elem


class ContinuedFraction(Fraction):

    @classmethod
    def validate(cls, *args: int | float | str | Fraction | Decimal, **kwargs: Any) -> None:
        """
        This method exists only to exclude negative numbers as inputs.

        As ``ContinuedFraction`` is a ``Fraction`` subclass inputs which don't
        satisfy the constraints of the superclass will trigger validation
        errors at the superclass level.
        """
        if set(map(type, args)).issubset([int, float, Fraction, Decimal]) and min(args) < 0:
            raise ValueError("Negative numbers, including negative numeric "
                             "strings, are invalid")

        str_args = list(filter(lambda arg: isinstance(arg, str), args))

        if str_args and any(re.match(r'^\-.*', arg.strip()) for arg in str_args): 
            raise ValueError("Negative numbers, including negative numeric "
                             "strings, are invalid")

    def __new__(cls, *args:  int | float | str | Fraction | Decimal, **kwargs: Any) -> Fraction:
        try:
            cls.validate(*args, **kwargs)
        except ValueError:
            raise

        return super().__new__(cls, *args, **kwargs)

    def __init__(self, *args:  int | float | str | Fraction | Decimal, **kwargs: Any):
        super().__init__()

        if len(args) == 1 and type(args[0]) in [int, float]:
            self._elements = tuple(continued_fraction(args[0]))
            return

        if len(args) == 1 and type(args[0]) == str and re.match(r'^\d/\d$', args[0].strip().replace(' ',  '')):
            self._elements = tuple(continued_fraction_rational(*self.as_integer_ratio()))
            return

        if len(args) == 1 and type(args[0]) == str and '/' not in args[0]:
            self._elements = tuple(continued_fraction(args[0]))
            return

        if len(args) == 1 and type(args[0]) in [Fraction, Decimal]:
            self._elements = tuple(continued_fraction_rational(*args[0].as_integer_ratio()))
            return

        if len(args) == 2 and set(map(type, args)) == set([int]):
            self._elements = tuple(continued_fraction_rational(args[0], args[1]))
            return

        if len(args) == 2 and set(map(type, args)).issubset([int, Fraction]):
            self._elements = tuple(continued_fraction_rational(*self.as_integer_ratio()))
            return

        raise ValueError(f"Invalid inputs - please check and try again")

    def __add__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__add__(other))

    def __radd__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__radd__(other))

    def __sub__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__sub__(other))

    def __rsub__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rsub__(other))

    def __mul__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__mul__(other))

    def __rmul__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rmul__(other))

    def __truediv__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__truediv__(other))

    def __rtruediv__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rtruediv__(other))

    def __floordiv__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__floordiv__(other))

    def __rfloordiv__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rfloordiv__(other))

    def __divmod__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__divmod__(other))

    def __rdivmod__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rdivmod__(other))

    def __pow__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__pow__(other))

    def __rpow__(self, other: ContinuedFraction) -> ContinuedFraction:
        return self.__class__(super().__rpow__(other))

    def __pos__(self) -> ContinuedFraction:
        return self.__class__(super().__pos__())

    def __abs__(self) -> ContinuedFraction:
        return self.__class__(super().__abs__())

    @property
    def elements(self) -> tuple[int]:
        return self._elements

    @property
    def order(self) -> int:
        return len(self._elements[1:])
