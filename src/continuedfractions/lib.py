__all__ = [
    'continued_fraction_real',
    'continued_fraction_rational',
    'convergent',
    'convergents',
    'fraction_from_elements',
    'left_mediant',
    'mediant',
    'remainder',
    'remainders',
    'right_mediant',
]


# -- IMPORTS --

# -- Standard libraries --
import decimal
import functools
import re

from decimal import Decimal
from fractions import Fraction
from typing import Generator

# -- 3rd party libraries --
import numba

# -- Internal libraries --


# A private copy of ``fractions._RATIONAL_FORMAT`` to support debugging
_RATIONAL_FORMAT = re.compile(r"""
    \A\s*                                  # optional whitespace at the start,
    (?P<sign>[-+]?)                        # an optional sign, then
    (?=\d|\.\d)                            # lookahead for digit or .digit
    (?P<num>\d*|\d+(_\d+)*)                # numerator (possibly empty)
    (?:                                    # followed by
       (?:\s*/\s*(?P<denom>\d+(_\d+)*))?   # an optional denominator
    |                                      # or
       (?:\.(?P<decimal>\d*|\d+(_\d+)*))?  # an optional fractional part
       (?:E(?P<exp>[-+]?\d+(_\d+)*))?      # and optional exponent
    )
    \s*\Z                                  # and optional whitespace to finish
""", re.VERBOSE | re.IGNORECASE)


@numba.jit
def _continued_fraction_rational(x: int, y: int) -> Generator[int, None, None]:     # pragma: no cover
    """
    A private implementation of the basic continued fraction algorithm for
    rational numbers :math:`\\frac{x}{y}`.

    Parameters
    ----------
    x : int
        An integer representing the numerator of a rational number.

    y : int
        An integer representing the (non-zero) denominator of the same rational
        number.

    Yields
    ------
    int
        Elements of a unique simple continued fraction of the given rational
        number.
    """
    while y:
        q, r = divmod(x, y)
        yield q
        x, y = y, r


def continued_fraction_rational(r: Fraction, /) -> Generator[int, None, None]:
    """Public service method for the private :py:func:`_continued_fraction_rational` above.

    The resulting sequence of elements defines a continued fraction of the form:

    .. math::

       a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2 + \\ddots\\cfrac{1}{a_{n - 1} + \\cfrac{1}{a_n}}}}

    which is also written more compactly as:

    .. math::

       [a_0; a_1, a_2\\ldots, a_n]

    The order of the continued fraction is said to be :math:`n`. If the last
    element :math:`a_n = 1` the sequence can be rewritten as
    :math:`[a_0; a_1, a_2\\ldots, a_{n - 1} + 1]`, which is then unique as a
    simple continued fraction representation of the rational number.

    Negative rational numbers can also be represented in this way, provided we
    use the `Euclidean division lemma <https://en.wikipedia.org/wiki/Euclid%27s_lemma>`_.
    This is described in more detail in the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/creating-continued-fractions.html#negative-continued-fractions>`_.

    For a definition of "continued fraction", "element", "order",
    "finite continued fraction", "simple continued fraction", please consult
    the `package documentation <https://continuedfractions.readthedocs.io/en/stable>`_,
    or any online resource such as `Wikipedia <https://en.wikipedia.org/wiki/Continued_fraction>`_,
    or suitable books on number theory.

    Parameters
    ----------
    r : `fractions.Fraction`
        The rational number to represented as a simple continued fraction.

    Yields
    ------
    int
        Elements of a unique simple continued fraction of the given rational
        number.

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
    Every rational number has exactly two simple continued fractions, one of
    which has an additional element of :math:`1` as its last element,
    i.e. :math:`[a_0;a_1,a_2,\\ldots,a_{n - 1}, 1]`. But this form can be
    reduced by adding the :math:`1` to the second last element, :math:`a_{n - 1}`,
    producing the shorter form :math:`[a_0;a_1,a_2,\\ldots, a_{n - 1} + 1]`,
    where the last element is now :math:`> 1`.

    The simple continued fraction representation generated by this function is
    the shorter version, and is thus unique.
    """
    yield from _continued_fraction_rational(*r.as_integer_ratio())


def continued_fraction_real(x: int | float | str | Decimal, /) -> Generator[int, None, None]:
    """Generates a finite sequence of elements (coefficients) of a (simple) continued fraction of the given real number.

    The result is a finite sequence even though the given number :math:`x` may
    be irrational or not exactly representable as a real number. 

    The simple continued fraction representation of :math:`x` is a number of
    the form

    .. math::

       a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2 + \\ddots}}

    where :math:`a_0 = [x]` is the integer part of :math:`x`, and the
    :math:`a_1,a_2\\ldots` are the (non-negative) quotients obtained by a
    repeated application of `Euclidean division <https://en.wikipedia.org/wiki/Euclidean_division>`_
    to the fractional part :math:`x - [x]`, which is called the remainder.

    If the last element :math:`a_n = 1` the sequence can be rewritten as
    :math:`[a_0; a_1, a_2\\ldots, a_{n - 1} + 1]`.

    As Python :py:class:`float` values, like all floating point
    implementations, are `finite precision representations <https://docs.python.org/3/tutorial/floatingpoint.html>`_
    of real numbers, the resulting simple continued fraction  of :math:`x`
    generated by this function may be approximate, not exact, and also not
    necessarily unique.

    For non-rational real numbers it is best to pass :py:class:`decimal.Decimal`
    values, with the `context precision <https://docs.python.org/3.12/library/decimal.html#context-objects>`_
    set to the highest level possible.

    The results for rational numbers are guaranteed to be exact however large
    the number, subject to memory and hardware limitations of the running
    environment.

    Invalid values will generate an error in either the
    :py:class:`fractions.Fraction` or :py:class:`decimal.Decimal` classes -
    no errors are raised directly in the function itself.

    Parameters
    ----------
    x : int, float, str, decimal.Decimal
        The real number to represent as a simple continued fraction.

    Yields
    ------
    int
        Elements of a simple continued fraction of the given real number.

    Examples
    --------
    A few examples are given below of how this function can be used.

    >>> list(continued_fraction_real(5000))
    [5000]
    >>> list(continued_fraction_real(-5000.0))
    [-5000]
    >>> list(continued_fraction_real(2/5))
    [0, 2, 2, 1801439850948198]
    >>> list(continued_fraction_real('2/5'))
    [0, 2, 2]
    >>> list(continued_fraction_real('-1/3'))
    [-1, 1, 2]
    >>> list(continued_fraction_real(1/1j))
    Traceback (most recent call last):
    ...
    TypeError: conversion from complex to Decimal is not supported
    >>> list(continued_fraction_real("not a numeric string"))
    Traceback (most recent call last):
    ...
    decimal.InvalidOperation: [<class 'decimal.ConversionSyntax'>]
    >>> list(continued_fraction_real(-649/200))
    [-4, 1, 3, 12, 3, 1, 234562480591, 2, 5, 2]
    >>> list(continued_fraction_real('-649/200'))
    [-4, 1, 3, 12, 4]
    >>> list(continued_fraction_real('-649/-200'))
    Traceback (most recent call last):
    ...
    ValueError: Invalid literal for Fraction: '-649/-200'
    >>> list(continued_fraction_real(Decimal('0.3333')))
    [0, 3, 3333]
    """
    if isinstance(x, int):
        yield x
    elif isinstance(x, str) and '/' in x:
        yield from continued_fraction_rational(Fraction(x))
    elif isinstance(x, float):
        yield from continued_fraction_rational(Fraction(*Decimal.from_float(x).as_integer_ratio()))
    else:
        yield from continued_fraction_rational(Fraction(*(Decimal(x).as_integer_ratio())))


def convergent(k: int, *elements: int) -> Fraction:
    """Returns the :math:`k`-th convergent of a (simple) continued fraction from a sequence of its elements.

    Given a (simple) continued fraction  :math:`[a_0;a_1,a_2,\\ldots]` the
    :math:`k`-th convergent is defined as:

    .. math::

       C_k = a_0 + \\cfrac{1}{a_1 + \\cfrac{1}{a_2 \\ddots \\cfrac{1}{a_{k-1} + \\cfrac{1}{a_k}}}}

    The result is a :py:class:`fractions.Fraction` instance.
    
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

    This function is a faithful implementation of this algorithm.

    A :py:class:`ValueError` is raised if :math:`k` is not an integer or is an
    integer greater than the number of elements, or if any of the elements are
    not integers.

    Parameters
    ----------
    k : `int`
        The order of the convergent. Must be a non-negative integer less than
        the number of elements.

    *elements : `int`
        A variable-length sequence of integer elements of a continued fraction.

    Returns
    -------
    fractions.Fraction
        A rational fraction constructed from the given sequence of elements of
        a continued fraction, representing the :math:`k`-order convergent of a
        (finite) simple continued fraction as given by a sequence of elements.

    Raises
    ------
    ValueError
        If :math:`k` is not a non-negative integer less than the number of
        elements, or if any of the elements are not integers.

    Examples
    --------
    >>> convergent(0, 3, 4, 12, 4)
    Fraction(3, 1)
    >>> convergent(1, 3, 4, 12, 4)
    Fraction(13, 4)
    >>> convergent(2, 3, 4, 12, 4)
    Fraction(159, 49)
    >>> convergent(3, 3, 4, 12, 4)
    Fraction(649, 200)
    >>> convergent(3)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> convergent(-1, 3, 4, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> convergent(4, 3, 4, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    """
    # Define the order of the continued fraction - may be ``-1`` if no elements
    # are given.
    n = len(elements) - 1

    if n == -1 or not isinstance(k, int) or k < 0 or k > n or any(not isinstance(elements[i], int) or elements[i] < 1 for i in range(1, n + 1)):
        raise ValueError(
            "`k` must be a non-negative integer not exceeding the order of \n"
            "the continued fraction (number of tail elements), and the tail \n"
            "elements must all be positive integers."
        )

    a, b = elements[0], 1
    
    if k == 0:
        return Fraction(a, b)

    c, d = (elements[1] * a) + b, elements[1]

    if k == 1:
        return Fraction(c, d)

    for e in elements[2:k + 1]:
        p, q = (e * c) + a, (e * d) + b
        a, b = c, d
        c, d = p, q

    return Fraction(p, q)


def convergents(*elements: int) -> Generator[Fraction, None, None]:
    """Generates an (ordered) sequence of all convergents of a (simple) continued fraction from a sequence of its elements.

    If :math:`n` is the order of the continued fraction represented by the
    given sequence of its elements then there are :math:`n + 1` convergents
    :math:`C_0, C_1, \\ldots, C_n`, and the function generates these in that
    order.

    See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/exploring-continued-fractions.html#convergents-and-rational-approximations>`_
    for more details on convergents.

    Parameters
    ----------
    *elements : `int`
        A variable-length sequence of integer elements of a (simple)
        continued fraction.

    Yields
    ------
    fractions.Fraction
        Each element generated is a :py:class:`fractions.Fraction` instance and
        a :math:`k`-th convergent of the given continued fraction.

    Raises
    ------
    ValueError
        If there are any non-integer elements, or the tail elements are not
        positive integers.

    Examples
    --------
    >>> tuple(convergents(3))
    (Fraction(3, 1),)
    >>> tuple(convergents(3, 2))
    (Fraction(3, 1), Fraction(7, 2))
    >>> tuple(convergents(3, 4, 12, 4))
    (Fraction(3, 1), Fraction(13, 4), Fraction(159, 49), Fraction(649, 200))
    >>> tuple(convergents(-5, 1, 1, 6, 7))
    (Fraction(-5, 1), Fraction(-4, 1), Fraction(-9, 2), Fraction(-58, 13), Fraction(-415, 93))
    >>> tuple(convergents(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    (Fraction(1, 1), Fraction(3, 2), Fraction(10, 7), Fraction(43, 30), Fraction(225, 157), Fraction(1393, 972), Fraction(9976, 6961), Fraction(81201, 56660), Fraction(740785, 516901), Fraction(7489051, 5225670))

    """
    # Define the order of the continued fraction - may be ``-1`` if no elements
    # are given.
    n = len(elements) - 1

    if n == -1 or any(not isinstance(elements[i], int) or (elements[i] <= 0 and i > 0) for i in range(n + 1)):
        raise ValueError(
            "Continued fraction elements must be integers, and all \n"
            "tail elements (from the 1st element onwards) must be positive."
        )

    a, b = elements[0], 1
    yield Fraction(a, b)

    if n > 0:
        c, d = (elements[1] * a) + b, elements[1]
        yield Fraction(c, d)

        if n > 1:
            for e in elements[2:]:
                p, q = (e * c) + a, (e * d) + b
                yield Fraction(p, q)
                a, b = c, d
                c, d = p, q


def fraction_from_elements(*elements: int) -> Fraction:
    """Returns the rational number represented by a (simple) continued fraction from a sequence of its elements.

    The elements must be given as positional arguments, which means that if
    they are contained in an iterable then they must be unpacked using the
    unpacking operator ``*``, as described in the examples below.

    Parameters
    ----------
    *elements : `int`
        A variable-length sequence of integer elements of a simple continued
        fraction.

    Returns
    -------
    fractions.Fraction
        A rational number constructed from a sequence of elements of a simple
        continued fraction which represents the number.

    Raises
    ------
    ValueError
        If any of the elements are not integers.

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

    return convergent(len(elements) - 1, *elements)


def remainder(k: int, *elements: int) -> Fraction:
    """Returns the :math:`k`-th remainder of a (simple) continued fraction from a sequence of its elements.

    Given a (simple) continued fraction  :math:`[a_0;a_1,a_2,\\ldots]` the
    :math:`k`-th remainder :math:`R_k` is the (simple) continued fraction
    :math:`[a_k; a_{k + 1}, a_{k + 2}, \\ldots]`:

    .. math::

       R_k = a_k + \\cfrac{1}{a_{k + 1} + \\cfrac{1}{a_{k + 2} \\ddots }}

    where :math:`R_0` is just the original continued fraction, i.e.
    :math:`R_0 = [a_0; a_1, a_2, \\ldots]`.

    The remainders satisfy the recurrence relation:

    .. math::

       R_{k - 1} = a_{k - 1} + \\frac{1}{R_k}, \\hskip{3em} k \\geq 1

    If the continued fraction :math:`[a_0; a_1, a_2,\\ldots]` is finite of
    order :math:`n` then all :math:`R_k` are rational. If we let
    :math:`R_k = \\frac{s_k}{t_k}` then the recurrence relation above can
    be written as:

    .. math::

       R_{k - 1} = \\frac{s_{k - 1}}{t_{k - 1}} = \\frac{a_{k - 1}s_k + t_k}{s_k}, \\hskip{3em} k \\geq 1

    As this library only deals with finite continued fractions, this function
    always produces remainders as instances of :py:class:`~fractions.Fraction`.

    The integer :math:`k` must be non-negative and cannot exceed the order
    of the continued fraction, i.e. the number of its tail elements.

    A :py:class:`ValueError` is raised if :math:`k` is not an integer, or is an
    integer greater than the number of elements, or if any of the elements are
    not integers, or if any of the tail elements are not positive integers.

    Parameters
    ----------
    k : `int`
        The index of the remainder. Must be a non-negative integer not
        exceeding the order of the continued fraction.

    *elements : `int`
        A variable-length sequence of integer elements of a (simple) continued
        fraction.

    Returns
    -------
    fractions.Fraction
        A rational fraction constructed from the given sequence of elements of
        a continued fraction, representing its :math:`k`-th remainder, as
        defined above.

    Raises
    ------
    ValueError
        If :math:`k` is not an integer, or is an integer greater than the
        number of elements, or if any of the elements are not integers, or if
        any of the tail elements are not positive integers.

    Examples
    --------
    >>> remainder(0, 3, 4, 12, 4)
    Fraction(649, 200)
    >>> remainder(1, 3, 4, 12, 4)
    Fraction(200, 49)
    >>> remainder(2, 3, 4, 12, 4)
    Fraction(49, 4)
    >>> remainder(3, 3, 4, 12, 4)
    Fraction(4, 1)
    >>> remainder(0, -5, 1, 1, 6, 7)
    Fraction(-415, 93)
    >>> remainder(1, -5, 1, 1, 6, 7)
    Fraction(93, 50)
    >>> remainder(2, -5, 1, 1, 6, 7)
    Fraction(50, 43)
    >>> remainder(3, -5, 1, 1, 6, 7)
    Fraction(43, 7)
    >>> remainder(4, -5, 1, 1, 6, 7)
    Fraction(7, 1)
    >>> remainder(1)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> remainder(-1, 3, 4, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> remainder(4, 3, 4, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> remainder(1, 3, 0, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    >>> remainder(1, 3, -1, 12, 4)
    Traceback (most recent call last):
    ...
    ValueError: `k` must be a non-negative integer not exceeding the order of 
    the continued fraction (number of tail elements), and the tail 
    elements must all be positive integers.
    """
    # Define the order of the continued fraction - may be ``-1`` if no elements
    # are given.
    n = len(elements) - 1

    if n == -1 or not isinstance(k, int) or k < 0 or k > n or any(not isinstance(elements[i], int) or elements[i] < 1 for i in range(1, n + 1)):
        raise ValueError(
            "`k` must be a non-negative integer not exceeding the order of \n"
            "the continued fraction (number of tail elements), and the tail \n"
            "elements must all be positive integers."
        )

    if k == n:
        return Fraction(elements[-1], 1)

    return fraction_from_elements(*elements[k:])


def remainders(*elements: int) -> Generator[Fraction, None, None]:
    """Generates an (ordered) sequence of all remainders of a (simple) continued fraction from a sequence of its elements in descending order of index.

    If :math:`n` is the order of the continued fraction represented by the
    given sequence of its elements then there are :math:`n + 1` remainders
    :math:`R_0, R_1, \\ldots, R_n`, and the function generates these in
    reverse order :math:`R_0, R_1, \\ldots, R_n`.

    See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/exploring-continued-fractions.html#remainders>`_
    for more details on remainders.

    Parameters
    ----------
    *elements : `int`
        A variable-length sequence of integer elements of a (simple)
        continued fraction.

    Yields
    ------
    fractions.Fraction
        Each element generated is a :py:class:`fractions.Fraction` instance and
        a :math:`k`-th remainder of the given continued fraction.

    Raises
    ------
    ValueError
        If no elements are given, or there are any non-integer elements, or
        the tail elements are not positive integers.

    Examples
    --------
    >>> tuple(remainders(3))
    (Fraction(3, 1),)
    >>> tuple(remainders(3, 2))
    (Fraction(2, 1), Fraction(7, 2))
    >>> tuple(remainders(3, 4, 12, 4))
    (Fraction(4, 1), Fraction(49, 4), Fraction(200, 49), Fraction(649, 200))
    >>> tuple(remainders(-5, 1, 1, 6, 7))
    (Fraction(7, 1), Fraction(43, 7), Fraction(50, 43), Fraction(93, 50), Fraction(-415, 93))
    >>> tuple(remainders(1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
    (Fraction(10, 1), Fraction(91, 10), Fraction(738, 91), Fraction(5257, 738), Fraction(32280, 5257), Fraction(166657, 32280), Fraction(698908, 166657), Fraction(2263381, 698908), Fraction(5225670, 2263381), Fraction(7489051, 5225670))
    >>> tuple(remainders())
    Traceback (most recent call last):
    ...
    ValueError: Continued fraction elements must be integers, and all 
    tail elements (from the 1st element onwards) must be positive.
    >>> tuple(remainders(0, 0))
    Traceback (most recent call last):
    ...
    ValueError: Continued fraction elements must be integers, and all 
    tail elements (from the 1st element onwards) must be positive.
    >>> tuple(remainders(1, 0))
    Traceback (most recent call last):
    ...
    ValueError: Continued fraction elements must be integers, and all 
    tail elements (from the 1st element onwards) must be positive.
    >>> tuple(remainders(1, 2, -1))
    Traceback (most recent call last):
    ...
    ValueError: Continued fraction elements must be integers, and all 
    tail elements (from the 1st element onwards) must be positive.
    """
    # Define the order of the continued fraction - may be ``-1`` if no elements
    # are given.
    n = len(elements) - 1

    if n == -1 or any(not isinstance(elements[i], int) or (elements[i] <= 0 and i > 0) for i in range(n + 1)):
        raise ValueError(
            "Continued fraction elements must be integers, and all \n"
            "tail elements (from the 1st element onwards) must be positive."
        )

    a, b = elements[-1], 1
    yield Fraction(a, b)

    if n > 0:
        i = n - 1

        while i >= 0:
            a, b = elements[i] * a + b, a
            yield Fraction(a, b)
            i -= 1


def mediant(r: Fraction, s: Fraction, /, *, dir: str = 'right', k: int = 1) -> Fraction:
    """Returns the :math:`k`-th left- or right-mediant of two rational numbers.

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

    For the left mediant use ``dir="left"``, while for the right use
    ``dir="right"``. The default is ``dir="right"``. For ``k = 1`` the left and
    right mediants are identical to the simple mediant :math:`\\frac{a + c}{b + d}`.

    Parameters
    ----------
    r : `fractions.Fraction`
        The first rational number.

    s : `fractions.Fraction`
        The second rational number.

    dir : `str`, default='right'
        The "direction" of the mediant - `'left'` or `'right'`, as defined
        above.

    k : `int`, default=1
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


#: A :py:func:`functools.partial` binding of :py:func:`mediant` for left-mediants.
left_mediant = functools.partial(mediant, dir="left")


#: A :py:func:`functools.partial` binding of :py:func:`mediant` for right-mediants.
right_mediant = functools.partial(mediant, dir="right")


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/lib.py
    #
    # NOTE: the doctest examples using ``float`` or ``decimal.Decimal`` values
    #       assume a context precision of 28 digits
    decimal.getcontext().prec = 28
    import doctest
    doctest.testmod()
