__all__ = [
    'continued_fraction_rational',
    'continued_fraction',
]


# -- IMPORTS --

# -- Standard libraries --
import decimal
import fractions

# -- 3rd party libraries --

# -- Internal libraries --


def continued_fraction_rational(x: int, y: int) -> Generator[int, None, None]:
    """
    Generates the (integer) elements of the continued fraction representation
    of the rational number ``x/y``, with numerator ``x`` and denominator ``y``.

    If ``y``, the denominator, is zero a ``ValueError`` is raised.

    If ``x`` and ``y`` are both negative the result is the same as when they
    are both positive: in this case the elements of the rational number given
    by ``-x/y`` are generated.

    If only one of ``x`` or ``y`` is negative the elements are generated in
    such a way that either (1) the first element is ``0`` if ``x/y < 0``,
    the second element is negatibve, and subsequent elements are all positive,
    or (2) the first element is nonzero and negative, while all subsequent
    elements are positive.
    """
    num, denum = x, y

    if denum == 0:
        raise ValueError("The denominator must be a non-zero integer")
 
    if num < 0 and denum < 0:
        num, denum = -num, -denum

    if num < 0 or denum < 0:
        if num < 0:
            elems = continued_fraction_rational(-num, denum)
        else:
            elems = continued_fraction_rational(num, -denum)

        elem = next(elems)
        if elem == 0:
            yield elem
            yield -next(elems)
        else:
            yield -elem

        for elem in elems:
            yield elem
            
        return        

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
