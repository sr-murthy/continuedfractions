__all__ = [
    'continued_fraction_real',
    'continued_fraction_rational',
    'fraction_from_elements',
    'convergent',
    'mediant',
]


# -- IMPORTS --

# -- Standard libraries --
from collections import deque
from decimal import Decimal
from itertools import accumulate
from fractions import Fraction
from typing import Generator

# -- 3rd party libraries --

# -- Internal libraries --


def continued_fraction_rational(r: Fraction, /) -> Generator[int, None, None]:
    """
    Generates the (integer) elements (also called coefficient or terms) of a
    unique, finite, "simple" continued fraction representation of the
    rational fraction ``x/y`` with numerator ``x`` and non-zero denominator
    ``y``, given as a `fractions.Fraction` object.

    The number of elements generated minus 1 is called the order of the
    continued fraction, and as the function applies only to rational fractions
    the order will always be finite.

    Negative rational fractions can be represented, but in accordance with
    convention and to ensure uniqueness only the numerator can be negative,
    while the denominator cannot - in case of inputs such as ``x/-y``, where
    ``x`` and ``y`` are positive integers, the negative sign is "transferred" from
    the denominator ``y`` to the numerator ``x``.

    For a definition of "continued fraction", "element", "order",
    "finite continued fraction", "simple continued fraction", please consult:

        https://en.wikipedia.org/wiki/Continued_fraction
        https://mathcenter.oxford.emory.edu/site/math125/continuedFractions/

    Parameters
    ----------
    r : `fractions.Fraction`
        The rational number to represented as a continued fraction.

    Yields
    ------
    int
        Elements of a unique, finite "simple" continued fraction representation
        of the given rational fraction ``x/y`` (where ``y`` is non-zero).

    Examples
    --------
    A few examples are given below of how this function can be used.

    >>> for e in continued_fraction_rational(Fraction(649, 200)):
    ...     print(e)
    ... 
    3
    4
    12
    4

    >>> list(continued_fraction_rational(Fraction(415, 93)))
    [4, 2, 6, 7]

    >>> list(continued_fraction_rational(Fraction(-649, 200)))
    [-4, 1, 3, 12, 4]

    >>> list(continued_fraction_rational(Fraction(123235, 334505)))
    [0, 2, 1, 2, 1, 1, 250, 1, 13]

    Notes
    -----
    It is known that every rational number has exactly two finite continued
    fraction representations, one of which has an additional element of ``1``
    as its last element. Any such continued fraction can be translated into a
    shorter continued fraction whose last element is 1 + its second last
    element.

    The continued fraction representation generated by this function is the
    shorter version, and is thus unique.

    A continued fraction is called "simple" if all of its fractional terms
    have the numerator ``1``, and it is the simple version that is generated by
    the function.
    """
    num, denom = r.as_integer_ratio()

    quo, rem = divmod(num, denom)
    yield quo

    while rem > 0:
        num, denom = denom, rem
        quo, rem = divmod(num, denom)
        yield quo


def continued_fraction_real(x: int | float | str, /) -> Generator[int, None, None]:
    """
    Generates the (integer) elements of a "simple" continued fraction
    representation of ``x``, which can be either an integer, float or an
    equivalent string representation, except for nans and non-numeric strings.

    As floats are finite precision representations of real numbers, if ``x``
    is a float representing a real number with a fractional part containing
    an infinite periodic sequence of digits, or is an irrational number, the
    continued fraction representation of ``x``, as given by the elements
    generated by the function, will necessarily be finite, but not necessarily
    unique.

    No attempt is made to raise exceptions or errors directly - if ``x`` is not
    an ``int`` or ``float``, or is a ``nan`` or a non-numeric string, either
    the ``decimal.Decimal`` conversion or the call to
    ``continued_fraction_rational`` will trigger upstream error(s).

    Parameters
    ----------
    x : `int`, `float`, `str`
        The number to represent as a continued fraction. It can be any ``int``
        or ``float``, or an equivalent string representation of an ``int`` or
        ``float``, except for nans (``float("nan")``) and non-numeric strings.

    Yields
    ------
    int
        Elements of a unique "simple" continued fraction representation of
        the given ``int`` or ``float``.

    Examples
    --------
    A few examples are given below of how this function can be used.

    >>> list(continued_fraction_real(2/5))
    [0, 2, 2]

    >>> list(continued_fraction_real(2984.0495684))
    [2984, 20, 5, 1, 2, 1, 7, 2, 9, 6, 1, 4]

    >>> list(continued_fraction_real(1/1j))
    Traceback (most recent call last):
    ...
    decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

    >>> list(continued_fraction_real('-1/3'))
    Traceback (most recent call last):
    ...
    decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]

    >>> list(continued_fraction_real(-649/200))
    [-4, 1, 3, 12, 4]

    Notes
    -----
    It might be expected that numeric strings expressing rational fractions,
    such as ``"1/3"``, would be processed succesfully, but this is not the
    case, as the key step in the function is to use the string representation
    of ``x`` to construct a `decimal.Decimal` object, which, however, does not
    treat strings such as ``"x/y"`` where ``x`` and ``y`` are integers or
    floats, as numeric.

    See the CPython library source for more information:

    https://github.com/python/cpython/blob/main/Lib/_pydecimal.py#L557

    But actual fractions where the numerator and denominator are ``int`` or
    ``float``, e.g. ``-1/4`` or ``5.6/2``, can be processed successfully.
    """
    num, denum = Decimal(str(x)).as_integer_ratio()

    for elem in continued_fraction_rational(Fraction(num, denum)):
        yield elem


def fraction_from_elements(*elements: int) -> Fraction:
    """
    Returns a ``fractions.Fraction`` object representing the rational fraction
    constructed from an ordered sequence of the (integer) elements of a
    continued fraction.

    The element sequence must be given as positional arguments, which means
    that if they are contained in an iterable then they must be unpacked
    using the unpacking operator ``*``, as described in the examples below.

    Parameters
    ----------
    *elements : `int`
        A variable-length sequence of integer elements of a continued fraction.

    Returns
    -------
    fractions.Fraction
        A rational fraction constructed from the given sequence of elements of
        a continued fraction.

    Raises
    ------
    ValueError
        If any elements are not integers.

    Examples
    --------
    >>> fraction_from_elements(3, 4, 12, 4)
    Fraction(649, 200)

    >>> fraction_from_elements(-4, 1, 3, 12, 4)
    Fraction(-649, 200)

    >>> fraction_from_elements(4, 2, 6, 7)
    Fraction(415, 93)

    >>> fraction_from_elements(*[4, 2, 6, 7])
    Fraction(415, 93)

    >>> fraction_from_elements(4.5, 2, 6, 7)
    Traceback (most recent call last):
    ...
    ValueError: Continued fraction elements must be integers
    """
    if any(not isinstance(elem, int) for elem in elements):
        raise ValueError("Continued fraction elements must be integers")

    return Fraction(
        deque(
            accumulate(reversed(elements), func=lambda x, y: Fraction(1, x) + y)
        ).pop()
    )


def convergent(*elements: int, k: int = 1) -> Fraction:
    """
    Returns a ``fractions.Fraction`` object representing the ``k``-th
    convergent of a (finite) continued fraction given by an ordered sequence of
    its (integer) elements.
    
    The integer ``k`` is called the order of the convergent, and a continued
    fraction of order ``n`` has exactly ``n + 1`` convergents of orders ``0``,
    ``1``, ... ``n``.

    Each convergent has its own continued fraction representation, which occurs
    as a partial sum in the continued fraction representation of the number
    represented by the continued fraction given by the element sequence.

    It is assumed that ``k`` < the number of elements, otherwise a
    ``ValueError`` is raised.

    Parameters
    ----------
    *elements : int
        A variable-length sequence of integer elements of a continued fraction.

    k : int, default=1
        The order of the convergent.

    Returns
    -------
    fractions.Fraction
        A rational fraction constructed from the given sequence of elements of
        a continued fraction, representing the ``k``-order convergent of a
        (finite) continued fraction represented by the given element sequence.

    Raises
    ------
    ValueError
        If `k` < the number of elements.

    Examples
    --------
    >>> convergent(3, 4, 12, 4, k=0)
    Fraction(3, 1)

    >>> convergent(3, 4, 12, 4, k=1)
    Fraction(13, 4)

    >>> convergent(3, 4, 12, 4, k=2)
    Fraction(159, 49)

    >>> convergent(3, 4, 12, 4, k=3)
    Fraction(649, 200)

    >>> convergent(3, 4, 12, 4, k=-1)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer less than the number of elements of the continued fraction

    >>> convergent(3, 4, 12, 4, k=4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer less than the number of elements of the continued fraction
    """
    if not isinstance(k, int) or k < 0 or k >= len(elements):
        raise ValueError(
            "`k` must be a non-negative integer less than the number of "
            "elements of the continued fraction"
        )

    return fraction_from_elements(*elements[:k + 1])


def mediant(r: Fraction, s: Fraction, /, *, dir='right', k: int = 1) -> Fraction:
    """
    Returns the ``k``-th left- or right-mediant of two rational numbers, given
    as ``fractions.Fraction`` objects.

    For a positive integer ``k``, the ``k``-th left-mediant of rational numbers
    ``r = a / b`` and ``s = c / d``, where ``b`` and ``d`` are non-zero, can be
    defined as:
    ::

        (ka + c) / (kb + d)

    while the ``k``-th right mediant can be defined as:
    ::

        (a + kc) / (b + kd)

    If we assume that ``r < s`` and ``bd > 0`` then the ``k``-th left mediants
    have the property that:
    ::

        a / b < ... < (3a + c) / (3b + d) < (2a + c) / (2b + d) < (a + c) / (b + d) < c / d
        a / b < (a + c) / (b + d) < (a + 2c) / (b + 2d) < (a + 3c) / (b + 3d) < ... c / d

    That is, the left mediants form a strictly decreasing sequence, actually
    converging to ``a / b``, while the right mediants form a strictly increasing
    sequence of, actually converging to ``c / d``.

    For the left mediant use ``dir="left"``, while for the right use
    ``dir="right"``. The default is ``dir="right"``. For ``k = 1`` the left and
    right mediants are the same.

    Parameters
    ----------
    r : fractions.Fraction
        The first rational number.

    s : fractions.Fraction
        The second rational number.

    dir : str, default='right'
        The "direction" of the mediant - `'left'` or `'right'`, as defined
        above.

    k : int, default=1
        The order of the mediant, as defined above.

    Returns
    -------
    fractions.Fraction
        The `k`-th left- or right-mediant of the two given rational numbers.

    Examples
    --------
    >>> mediant(Fraction(1, 2), Fraction(3, 5))
    Fraction(4, 7)
    >>> mediant(Fraction(1, 2), Fraction(3, 5), dir='left')
    Fraction(4, 7)
    >>> mediant(Fraction(1, 2), Fraction(3, 5), k=2)
    Fraction(7, 12)
    >>> mediant(Fraction(1, 2), Fraction(3, 5), dir='left', k=2)
    Fraction(5, 9)
    >>> mediant(Fraction(1, 2), Fraction(3, 5), k=3, dir='right')
    Fraction(10, 17)
    >>> mediant(Fraction(1, 2), Fraction(3, 5), k=3, dir='left')
    Fraction(6, 11)
    """
    if not (dir in ['left', 'right'] and isinstance(k, int) and k > 0):
        raise ValueError(
            "The mediant direction must be 'left' or 'right' and the order "
            "`k` must be a positive integer"
        )

    a, b = r.as_integer_ratio()
    c, d = s.as_integer_ratio()

    if dir == 'left':
        return Fraction(k * a + c, k * b + d)

    return Fraction(a + k * c, b + k * d)


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/lib.py
    #
    import doctest
    doctest.testmod()
