from __future__ import annotations


__all__ = [
    'rationals',
    'coprime_pairs',
    'FareyFraction',
    'farey_sequence',
    'KSRMTree',
]


# -- IMPORTS --

# -- Standard libraries --
import math
import typing

from itertools import chain

# -- 3rd party libraries --

# -- Internal libraries --
from continuedfractions.utils import NamedCallableProxy
from continuedfractions.continuedfraction import ContinuedFraction


def rationals(
    enumeration: typing.Literal["cantor diagonal", "cantor diagonal transposed", "rectilinear", "rectilinear transposed"],
    positive_only: bool = True
) -> typing.Generator[ContinuedFraction, None, None]:
    """:py:class:`typing.Generator` : An enumerator of rational numbers :math:`\\mathbb{Q}` using an enumeration on Cantor's 2D representation of the rationals.

    By default it generates sequences of all positive rational numbers as
    :py:class:`~continuedfractions.continuedfractions.ContinuedFraction`
    objects with the user-specified enumeration on Cantor's 2D
    representation of the rationals as described in the
    `documentation <https://continuedfractions.readthedocs.io/sources/sequences.html#rationals>`_.

    To include negative rationals and :math:`0` set ``positive_only`` to
    ``False``, as described in the documentation and the docstring examples
    below.

    The enumeration type should be given by the ``enumeration`` argument, which
    should be one of the following:

    * ``"cantor diagonal"``: for the standard way of enumerating rational
    numbers using Cantor diagonalisation (with ``positive_only=False``):
    
    .. math::

        \\frac{1}{1}, \\frac{2}{1}, \\frac{1}{2}, \\frac{1}{3}, \\frac{3}{1}, \\frac{4}{1}, \\frac{3}{2}, \\frac{2}{3}, \\frac{1}{4}, \\ldots

    * ``"cantor diagonal transposed"``: similar to the standard Cantor
    diagonalisation (with ``positive_only=False``), except the enumeration
    proceeds:
    ::

        right 1 step ->
        diagonal down 1 step ->
        down 1 step ->
        diagonal up 2 steps ->
        ...
    
    and produces the sequence:

    .. math::

        \\frac{1}{1}, \\frac{1}{2}, \\frac{2}{1}, \\frac{3}{1}, \\frac{1}{3}, \\frac{1}{4}, \\frac{2}{3}, \\frac{3}{2}, \\frac{4}{1}, \\ldots

    * ``"rectilinear"``: an enumeration which proceeds in a reverse L-shaped
    way (with ``positive_only=False``):
    ::

        down 1 step  ->
        right 1 step -> up 1 step   -> right 1 step ->
        down 2 steps -> left 2 steps -> down 1 step ->
        right 3 steps -> up 3 steps -> right 1 step ->
        down 4 steps  -> left 4 steps -> down 1 step ->
        ...

    and produces the sequence: 
    
    .. math::

       \\frac{1}{1}, \\frac{2}{1}, \\frac{1}{2}, \\frac{1}{3}, \\frac{2}{3}, \\frac{3}{2}, \\frac{3}{1}, \\frac{4}{1}, \\ldots

    * ``"rectilinear transposed"``: an enumeration similar to ``"rectilinear"``
    (with ``positive_only=False``) except the enumeration proceeds:
    ::

        right 1 step  ->
        down 1 step -> left 1 step   -> down 1 step ->
        right 2 steps -> up 2 steps -> right 1 step ->
        down 3 steps -> left 3 steps -> down 1 step ->
        right 4 steps  -> up 4 steps -> right 1 step ->
        ...
    
    and produces the sequence:
    
    .. math::

       \\frac{1}{1}, \\frac{1}{2}, \\frac{2}{1}, \\frac{3}{1}, \\frac{3}{2}, \\frac{2}{3}, \\frac{1}{3}, \\frac{1}{4}, \\ldots

    Parameters
    ----------
    enumeration : str
        A string literal which describes how the rationals should be
        enumerated:

        * ``"cantor diagonal"``
        * ``"cantor diagonal transposed"``
        * ``"rectilinear"``
        * ``"rectilinear transposed"``

        These enumerations are described above in the docstring, and also in
        the `Sphinx documentation <https://continuedfractions.readthedocs.io/sources/pythagorean-triples.html#primitive-pythagorean-triples>`_

    positive_only : bool, default=True
        Whether to generate only the positive rationals, which is true by
        default.

    Yields
    ------
    ContinuedFraction
        The rational numbers are generated as
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
        objects.

    Raises
    ------
    ValueError
        If ``enumeration`` is not an unrecognised or unsupported enumeration.

    Examples
    --------
    >>> rats = rationals(enumeration="cantor diagonal")
    >>> first_ten = [next(rats) for _ in range(10)]
    >>> first_ten
    [ContinuedFraction(1, 1), ContinuedFraction(2, 1), ContinuedFraction(1, 2), ContinuedFraction(1, 3), ContinuedFraction(3, 1), ContinuedFraction(4, 1), ContinuedFraction(3, 2), ContinuedFraction(2, 3), ContinuedFraction(1, 4), ContinuedFraction(1, 5)]
    >>> rats = rationals(enumeration="cantor diagonal", positive_only=False)
    >>> first_ten_plus_zero = [next(rats) for _ in range(11)]
    >>> first_ten_plus_zero
    [ContinuedFraction(0, 1), ContinuedFraction(1, 1), ContinuedFraction(-1, 1), ContinuedFraction(2, 1), ContinuedFraction(-2, 1), ContinuedFraction(1, 2), ContinuedFraction(-1, 2), ContinuedFraction(1, 3), ContinuedFraction(-1, 3), ContinuedFraction(3, 1), ContinuedFraction(-3, 1)]
    >>> rats = rationals(enumeration="cantor diagonal transposed")
    >>> first_ten = [next(rats) for _ in range(10)]
    >>> first_ten
    [ContinuedFraction(1, 1), ContinuedFraction(1, 2), ContinuedFraction(2, 1), ContinuedFraction(3, 1), ContinuedFraction(1, 3), ContinuedFraction(1, 4), ContinuedFraction(2, 3), ContinuedFraction(3, 2), ContinuedFraction(4, 1), ContinuedFraction(5, 1)]
    >>> rats = rationals(enumeration="cantor diagonal transposed", positive_only=False)
    >>> first_ten_plus_zero = [next(rats) for _ in range(11)]
    >>> first_ten_plus_zero
    [ContinuedFraction(0, 1), ContinuedFraction(1, 1), ContinuedFraction(-1, 1), ContinuedFraction(1, 2), ContinuedFraction(-1, 2), ContinuedFraction(2, 1), ContinuedFraction(-2, 1), ContinuedFraction(3, 1), ContinuedFraction(-3, 1), ContinuedFraction(1, 3), ContinuedFraction(-1, 3)]
    >>> rats = rationals(enumeration="rectilinear")
    >>> first_ten = [next(rats) for _ in range(10)]
    >>> first_ten
    [ContinuedFraction(1, 1), ContinuedFraction(2, 1), ContinuedFraction(1, 2), ContinuedFraction(1, 3), ContinuedFraction(2, 3), ContinuedFraction(3, 2), ContinuedFraction(3, 1), ContinuedFraction(4, 1), ContinuedFraction(4, 3), ContinuedFraction(3, 4)]
    >>> rats = rationals(enumeration="rectilinear", positive_only=False)
    >>> first_ten_plus_zero = [next(rats) for _ in range(11)]
    >>> first_ten_plus_zero
    [ContinuedFraction(0, 1), ContinuedFraction(1, 1), ContinuedFraction(-1, 1), ContinuedFraction(2, 1), ContinuedFraction(-2, 1), ContinuedFraction(1, 2), ContinuedFraction(-1, 2), ContinuedFraction(1, 3), ContinuedFraction(-1, 3), ContinuedFraction(2, 3), ContinuedFraction(-2, 3)]
    >>> rats = rationals(enumeration="rectilinear transposed", positive_only=False)
    >>> first_ten_plus_zero = [next(rats) for _ in range(11)]
    >>> first_ten_plus_zero
    [ContinuedFraction(0, 1), ContinuedFraction(1, 1), ContinuedFraction(-1, 1), ContinuedFraction(1, 2), ContinuedFraction(-1, 2), ContinuedFraction(2, 1), ContinuedFraction(-2, 1), ContinuedFraction(3, 1), ContinuedFraction(-3, 1), ContinuedFraction(3, 2), ContinuedFraction(-3, 2)]
    >>> rats = rationals(enumeration="some unknown enumeration")
    >>> next(rats)
    Traceback (most recent call last):
    ...
    ValueError: The value of `enumeration` should be one of the following: "cantor diagonal", "cantor diagonal transposed", "rectilinear" or "rectilinear transposed".
    """
    # Validation of the ``enumeration`` argument.
    enumeration_ = enumeration.strip().lower()
    if enumeration_ not in [
        "cantor diagonal", "cantor diagonal transposed", "rectilinear", "rectilinear transposed"
    ]:
        raise ValueError(
            'The value of `enumeration` should be one of the following: '
            '"cantor diagonal", "cantor diagonal transposed", "rectilinear" '
            'or "rectilinear transposed".'
        )

    if enumeration_ == "cantor diagonal" and positive_only:
        # The diagonal index, starting at ``n = 1``: the first diagonal `D1`
        # which is just ``1/1``.
        n = 1
        yield ContinuedFraction(1, 1)

        while True:
            # Increment the diagonal index, and generate the new diagonal:
            # the diagonal ``D_n`` is given by:
            #
            #     n/1, (n - 1)/2, (n - 2)/3, ... , 1/n
            #
            # if ``n`` is even, while if ``n`` is odd it is given by:
            #
            #    1/n, 2/(n - 1), 3/(n - 2), ... , n/1
            #
            n += 1
            us = range(n, 0, -1) if n % 2 == 0 else range(1, n + 1)
            vs = range(1, n + 1) if n % 2 == 0 else range(n, 0, -1)
            yield from (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
    elif enumeration_ == "cantor diagonal" and not positive_only:
        # When ``positive_only`` is ``False`` we start by generating the
        # ``ContinuedFraction`` object for ``0``.
        yield ContinuedFraction(0, 1)
        n = 0

        while True:
            # Same process as for ``"cantor diagonal"``, except that for each
            # coprime pair ``(u, v)`` on the ``n``-th diagonal we generate the
            # negative continued fraction ``-u/v`` immediately after the
            # positive continued fraction ``u/v``.
            n += 1
            us = range(n, 0, -1) if n % 2 == 0 else range(1, n + 1)
            vs = range(1, n + 1) if n % 2 == 0 else range(n, 0, -1)
            pos_rationals = (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
            yield from chain.from_iterable(((r, -r) for r in pos_rationals))
    elif enumeration_ == "cantor diagonal transposed" and positive_only:
        # The diagonal index, starting at ``n = 1``: the first diagonal `D1`
        # which is just ``1/1``.
        n = 1
        yield ContinuedFraction(1, 1)

        while True:
            # Increment the diagonal index, and generate the new diagonal:
            # the diagonal ``D_n`` is given by:
            #     1/n, 2/(n - 1), 3/(n - 2), ... , n/1  
            # 
            # if ``n`` is even, while if ``n`` is odd it is given by:
            #
            #     n/1, (n - 1)/2, (n - 2)/3, ... , 1/n
            #
            n += 1
            us = range(1, n + 1) if n % 2 == 0 else range(n, 0, -1)
            vs = range(n, 0, -1) if n % 2 == 0 else range(1, n + 1)
            yield from (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
    elif enumeration_ == "cantor diagonal transposed" and not positive_only:
        # When ``positive_only`` is ``False`` we start by generating the
        # ``ContinuedFraction`` object for ``0``.
        yield ContinuedFraction(0, 1)
        n = 0

        while True:
            # Same process as for ``"cantor diagonal transposed"``, except that
            # for each coprime pair ``(u, v)`` on the ``n``-th diagonal we
            # generate the negative continued fraction ``-u/v`` immediately
            # after the positive continued fraction ``u/v``.
            n += 1
            us = range(1, n + 1) if n % 2 == 0 else range(n, 0, -1)
            vs = range(n, 0, -1) if n % 2 == 0 else range(1, n + 1)
            pos_rationals = (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
            yield from chain.from_iterable(((r, -r) for r in pos_rationals))
    elif enumeration_ == "rectilinear" and positive_only:
        # The initial reverse-L index, starting at ``n = 1``: this will
        # generate ``1/1``.
        n = 1
        yield ContinuedFraction(1, 1)

        while True:
            # Increment the reverse-L index, and enumerate the rationals (as
            # described in the documentation) from the  reverse Ls ``⅃_n`` first
            # by first chaining the subsequences ``⅃_{n,1}`` and ``⅃_{n,2}``,
            # both of length ``2n - 1``, to produce the chained subsequence:
            #
            #     n/1, n/2, n/3, ... , n/n, (n - 1)/n, (n - 2)/n, (n - 3)/n, ... , 1/n
            # 
            # if ``n`` is even, or, if ``n`` is odd, as:
            #
            #     1/n, 2/n, 3/n, ... , n/n, n/(n - 1), n/(n - 2), n/(n - 3), ... , n/1
            #
            # and then filtering out composite fractions ``u/v`` in the chained
            # subsequence, i.e. applying ``math.gcd(u, v) == 1``. 
            #
            n += 1
            us = (
                chain((n for _ in range(n)), range(n - 1, 0, -1))
                if n % 2 == 0 else 
                chain(range(1, n + 1), (n for _ in range(n - 1)))
            )
            vs = (
                chain(range(1, n + 1), (n for _ in range(n - 1)))
                if n % 2 == 0 else
                chain((n for _ in range(n)), range(n - 1, 0, -1))
            )
            yield from (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
    elif enumeration_ == "rectilinear" and not positive_only:
        # When ``positive_only`` is ``False`` we start by generating the
        # ``ContinuedFraction`` object for ``0``.
        yield ContinuedFraction(0, 1)
        n = 0

        while True:
            # Same process as for ``"rectilinear"``, except that for each
            # coprime pair ``(u, v)`` on the ``n``-th reverse L ``⅃_n`` we
            # generate the negative continued fraction ``-u/v`` immediately
            # after the positive continued fraction ``u/v``.
            n += 1
            us = (
                chain((n for _ in range(n)), range(n - 1, 0, -1))
                if n % 2 == 0 else 
                chain(range(1, n + 1), (n for _ in range(n - 1)))
            )
            vs = (
                chain(range(1, n + 1), (n for _ in range(n - 1)))
                if n % 2 == 0 else
                chain((n for _ in range(n)), range(n - 1, 0, -1))
            )
            pos_rationals = (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
            yield from chain.from_iterable(((r, -r) for r in pos_rationals))
    elif enumeration_ == "rectilinear transposed" and positive_only:
        # The initial reverse-L index, starting at ``n = 1``: this will
        # generate ``1/1``.
        n = 1
        yield ContinuedFraction(1, 1)

        while True:
            # Increment the reverse-L index, and enumerate the rationals (as
            # described in the documentation) from the  reverse Ls ``⅃_n`` first
            # by first chaining the subsequences ``⅃_{n,1}`` and ``⅃_{n,2}``,
            # both of length ``2n - 1``, to produce the chained subsequence:
            #
            #     1/n, 2/n, 3/n, ... , n/n, n/(n - 1), n/(n - 2), n/(n - 3), ... , n/1
            # 
            # if ``n`` is even, or, if ``n`` is odd, as:
            #
            #     n/1, n/2, n/3, ... , n/n, (n - 1)/n, (n - 2)/n, (n - 3)/n, ... , 1/n
            #
            # and then filtering out composite fractions ``u/v`` in the chained
            # subsequence, i.e. applying ``math.gcd(u, v) == 1``.
            n += 1
            us = (
                chain(range(1, n), (n for _ in range(n)))
                if n % 2 == 0 else
                chain((n for _ in range(n)), range(n - 1, 0, -1))
            )
            vs = (
                chain((n for _ in range(n - 1)), range(n, 0, -1))
                if n % 2 == 0 else
                chain(range(1, n + 1), (n for _ in range(n - 1)))
            )
            yield from (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
    elif enumeration_ == "rectilinear transposed" and not positive_only:
        # When ``positive_only`` is ``False`` we start by generating the
        # ``ContinuedFraction`` object for ``0``.
        yield ContinuedFraction(0, 1)
        n = 0

        while True:
            # Same process as for ``"rectilinear transposed"``, except that
            # for each coprime pair ``(u, v)`` on the ``n``-th reverse L
            # ``⅃_n`` we generate the negative continued fraction ``-u/v``
            # immediately after the positive continued fraction ``u/v``. 
            n += 1
            us = (
                chain(range(1, n), (n for _ in range(n)))
                if n % 2 == 0 else
                chain((n for _ in range(n)), range(n - 1, 0, -1))
            )
            vs = (
                chain((n for _ in range(n - 1)), range(n, 0, -1))
                if n % 2 == 0 else
                chain(range(1, n + 1), (n for _ in range(n - 1)))
            )
            pos_rationals = (ContinuedFraction(u, v) for u, v in zip(us, vs) if math.gcd(u, v) == 1)
            yield from chain.from_iterable(((r, -r) for r in pos_rationals))

    return  # pragma: no cover


def _coprime_integers(n: int, /) -> typing.Generator[int, None, None]:
    """Generates a sequence of (positive) integers :math:`1 \\leq m < n` coprime to a given positive integer :math:`n`.

    The tuple is sorted in descending order of magnitude.

    Parameters
    ----------
    n : int
        The positive integer for which (positive) coprime integers
        :math:`m < n` are sought.

    Raises
    ------
    ValueError
        If :math:`n` is either not a positive integer, or :math:`n > 1` such
        that either the ``start`` value is **not** in the range
        :math:`1..n - 1` or the ``stop`` value is **not** in the range
        :math:`\\text{start} + 1..n`.

    Yields
    ------
    int
        A sequence of (positive) integers :math:`1 \\leq m < n` coprime to a
        given positive integer :math:`n`.

    Examples
    --------
    Examples using the default ``start`` and ``stop`` values:

    >>> tuple(_coprime_integers(1))
    (1,)
    >>> tuple(_coprime_integers(5))
    (4, 3, 2, 1)
    >>> tuple(_coprime_integers(10))
    (9, 7, 3, 1)

    """
    if not isinstance(n, int) or n < 1:
        raise ValueError(
            "`n` must be a positive integer; if `n` > 1 then the "
            "`start` value must be a positive integer in the range 1..n - 1; "
            "and if given the `stop` value must be a positive integer in the "
            "range `start` + 1..n"
        )

    yield from (m for m in range(n, 0, -1) if math.gcd(m, n) == 1)


KSRMTreeNode: typing.TypeAlias = tuple[int, int]        #: Custom type for nodes of the KSRM coprime pairs tree
KSRMTreeBranch: typing.TypeAlias = NamedCallableProxy   #: Custom type for generating branches of the KSRM coprime pairs tree


class KSRMTree:
    """A class implementation of the Kanga-Saunders-Randall-Mitchell (KSRM) ternary trees for representing and generating pairs of all (positive) coprime integers.

    The term "KSRM trees" is the author's, and refers to the trees presented in the following papers:

    * Kanga, A. R. (1990). The Family Tree of Pythagorean Triplets. The Mathematical Gazette, 26(15), 15-17.
    * Mitchell, D. W. (2001). An Alternative Characterisation of All Primitive Pythagorean Triples. The Mathematical Gazette, 85(503), 273-275. https://doi.org/10.2307/3622017
    * Saunders, R., & Randall, T. (1994). The family tree of the Pythagorean triplets revisited. The Mathematical Gazette, 78(482), 190-193. https://doi.org/10.2307/3618576

    .. note::

       The class is named ``KSRMTree`` purely for convenience, but it is
       actually a representation of two (ternary) subtrees.

    .. note::

       The author could not access the Kanga paper online, but the core result
       is described clearly in the papers of Saunders and Randall, and of
       Mitchell.

    See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/sequences.html#ksrm-trees>`_
    for more details.
    """

    # The two slots for the private attributes for the key tree features - the
    # two roots ``(2, 1), (3, 1)``, and the three branch generating functions.
    __slots__ = ('_roots', '_branches')

    _roots: tuple[KSRMTreeNode, KSRMTreeNode]

    _branches: tuple[KSRMTreeBranch]    # noqa: F821

    def __new__(cls) -> KSRMTree:
        """Class constructor.

        Creates and initialises a new instance with the minimum set of required
        attributes - for the roots and branch generating functions, which we
        call branches.
        """
        self = super().__new__(cls)
        self._roots = ((2, 1), (3, 1))
        self._branches = (
            NamedCallableProxy(lambda x, y: (2 * x - y, x), name="KSRM tree branch #1: (x, y) |--> (2x - y, x)"),
            NamedCallableProxy(lambda x, y: (2 * x + y, x), name="KSRM tree branch #2: (x, y) |--> (2x + y, x)"),
            NamedCallableProxy(lambda x, y: (x + 2 * y, y), name="KSRM tree branch #3: (x, y) |--> (x + 2y, y)")
        )

        return self

    @property
    def roots(self) -> typing.Literal[((2, 1), (3, 1))]:
        """:py:class:`tuple`: The tuple of roots of the KSRM trees, which are :math:`(2, 1)` and :math:`(3, 1)`.

        For more details see the following papers:

        * Kanga, A. R. (1990). The Family Tree of Pythagorean Triplets. The Mathematical Gazette, 26(15), 15-17.
        * Mitchell, D. W. (2001). An Alternative Characterisation of All Primitive Pythagorean Triples. The Mathematical Gazette, 85(503), 273-275. https://doi.org/10.2307/3622017
        * Saunders, R., & Randall, T. (1994). The family tree of the Pythagorean triplets revisited. The Mathematical Gazette, 78(482), 190-193. https://doi.org/10.2307/3618576

        or the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/sequences.html#ksrm-trees>`_.

        Examples
        --------
        >>> KSRMTree().roots
        ((2, 1), (3, 1))
        """
        return self._roots

    @property
    def branches(self) -> tuple[KSRMTreeBranch]:    # noqa: F821
        """:py:class:`tuple`: The tuple of three branch generating functions of the KSRM trees.

        There are three branch generating functions, given by the mappings:

        .. math::

           \\begin{align}
           (a, b) &\\longmapsto (2a - b, a) \\\\
           (a, b) &\\longmapsto (2a + b, a) \\\\
           (a, b) &\\longmapsto (a + 2b, b)
           \\end{align}

        For more details see the following papers:

        * Kanga, A. R. (1990). The Family Tree of Pythagorean Triplets. The Mathematical Gazette, 26(15), 15-17.
        * Mitchell, D. W. (2001). An Alternative Characterisation of All Primitive Pythagorean Triples. The Mathematical Gazette, 85(503), 273-275. https://doi.org/10.2307/3622017
        * Saunders, R., & Randall, T. (1994). The family tree of the Pythagorean triplets revisited. The Mathematical Gazette, 78(482), 190-193. https://doi.org/10.2307/3618576

        or the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/sequences.html#ksrm-trees>`_.

        Examples
        --------
        Generating the first two generations of children for the parent
        :math:`(2, 1)`.

        >>> tree = KSRMTree()
        >>> tree.branches
        (NamedCallableProxy("KSRM tree branch #1: (x, y) |--> (2x - y, x)"), NamedCallableProxy("KSRM tree branch #2: (x, y) |--> (2x + y, x)"), NamedCallableProxy("KSRM tree branch #3: (x, y) |--> (x + 2y, y)"))
        >>> tree.branches[0](2, 1)
        (3, 2)
        >>> tree.branches[1](2, 1)
        (5, 2)
        >>> tree.branches[2](2, 1)
        (4, 1)
        >>> tree.branches[0](*tree.branches[0](2, 1))
        (4, 3)
        >>> tree.branches[1](*tree.branches[0](2, 1))
        (8, 3)
        >>> tree.branches[2](*tree.branches[0](2, 1))
        (7, 2)
        >>> tree.branches[0](*tree.branches[1](2, 1))
        (8, 5)
        >>> tree.branches[1](*tree.branches[1](2, 1))
        (12, 5)
        >>> tree.branches[2](*tree.branches[1](2, 1))
        (9, 2)
        >>> tree.branches[0](*tree.branches[2](2, 1))
        (7, 4)
        >>> tree.branches[1](*tree.branches[2](2, 1))
        (9, 4)
        >>> tree.branches[2](*tree.branches[2](2, 1))
        (6, 1)
        """
        return self._branches

    def _backtrack(
        self,
        n: int,
        visited: list[tuple[KSRMTreeNode, KSRMTreeBranch]],     # noqa: F821
        /,
        *,
        node_bound: int = None
    ) -> tuple[KSRMTreeNode, KSRMTreeBranch, int, KSRMTreeBranch]:  # noqa: F821
        """Backtracks on the KSRM coprime pairs trees from a failed node to the nearest previously visited node that satisfies the node bound.

        A private function that backtracks on the KSRM coprime pairs trees: the
        procedure is that, given a (positive) integer :math:`n > 2`, for which
        coprime pairs are being sought, and a sequence (list) of pairs of
        visited nodes and their associated generating branches in the KSRM
        tree, and assuming that the last element of the visited sequence
        contains the node that "failed", the function identifies the nearest
        previously visited node whose first component satisifes the test
        :math:`< n` **and** and whose associated generating branch is not equal
        to the third branch given by :math:`(x, y) \\longmapsto (x + 2y, y)`.

        .. note::

           The function assumes that the last node in the incoming sequence
           of visited nodes and generating branch pairs represents a "failed"
           node, i.e. whose first component failed the test :math:`\\leq n`
           during the search. No attempt is made to validate or verify the
           failed node, and the only purpose of the function is to backtrack
           to the nearest previously visited node which meets the requirements
           listed above.

        .. note::

           There is no input validation as this is a private function which
           will be called from
           :py:meth:`~continuedfractions.sequences.KSRMTree.search_root`. So
           results for invalid arguments will most likely be incorrect or
           unexpected.

        Parameters
        ----------
        n : int
            The (positive) integer :math:`> 2` which is passed by the root
            search method or the general tree search method.

        visited : list
            A sequence of visited nodes and associated generating branches in
            the KSRM coprime pairs tree.

        node_bound : int, default=None
            A bound to check that :math:`a < n` for a node :math:`(a, b)`. The
            actual default value is the incoming :math:`n`, and this is set
            internally.

        Returns
        -------
        tuple
            A tuple consisting of the following values in order: (1) the
            target node in the visited sequence to backtrack to, (2) the
            associated generating branch function (the lambda for branch #1,
            or branch #2, or branch #3), (3) the index of the target node
            and branch pair in the visited sequence, (4) the generating
            branch of the successor node of the target node returned as (1).

        Examples
        --------
        An example where :math:`n = 5` and the failed node is :math:`(6, 1)`,
        which was the successor node to :math:`(4, 1)` from the third branch.

        >>> tree = KSRMTree()
        >>> tree.branches
        (NamedCallableProxy("KSRM tree branch #1: (x, y) |--> (2x - y, x)"), NamedCallableProxy("KSRM tree branch #2: (x, y) |--> (2x + y, x)"), NamedCallableProxy("KSRM tree branch #3: (x, y) |--> (x + 2y, y)"))
        >>> visited = [((2, 1), None), ((4, 1), tree.branches[-1]), ((6, 1), tree.branches[-1])]
        >>> tree._backtrack(5, visited)
        ((2, 1), None, 0, NamedCallableProxy("KSRM tree branch #3: (x, y) |--> (x + 2y, y)"))

        An example where :math:`n = 8` and the failed node is :math:`(19, 8)`,
        which was the successor node to :math:`(8, 3)` from the first branch.

        >>> tree = KSRMTree()
        >>> tree.branches
        (NamedCallableProxy("KSRM tree branch #1: (x, y) |--> (2x - y, x)"), NamedCallableProxy("KSRM tree branch #2: (x, y) |--> (2x + y, x)"), NamedCallableProxy("KSRM tree branch #3: (x, y) |--> (x + 2y, y)"))
        >>> visited = [((2, 1), None), ((3, 2),tree.branches[0]), ((8, 3),tree.branches[1]), ((19, 8), tree.branches[0])]
        >>> tree._backtrack(8, visited)
        ((3, 2), NamedCallableProxy("KSRM tree branch #1: (x, y) |--> (2x - y, x)"), 1, NamedCallableProxy("KSRM tree branch #2: (x, y) |--> (2x + y, x)"))
        """
        # Set the node bound for ``r``: so we require ``a < n`` for the
        # backtracked target node.
        node_bound = node_bound or n

        # Set the current node and branch as the last pair in the visited
        # sequence.
        cur_node, cur_branch = visited[-1]

        # If we've only visited one node it must be the root, and there is
        # no further backtracking possible, so just return appropriately.
        if len(visited) == 1:
            return cur_node, cur_branch, 0, None

        # Otherwise do some initialisation for variables tracking the
        # generating branch for the last visited node, and the current
        # node index.
        last_branch = None
        cur_index = len(visited) - 1

        # The main backtracking loop - while there are more nodes to backtrack
        # to, go back one node, decrement the current node index and set the
        # current node and generating branch, and also set the generating
        # branch of the last visited node before the current node.
        #
        # If the current node passes the test ``a < n` and we are not on the
        # last branch, return the current node, generating branch, index
        # and the generating branch of the last visited node before the current
        # node.
        while cur_index > 0 and (cur_node[0] >= node_bound or last_branch == self.branches[-1]):
            cur_index -= 1
            cur_node, cur_branch = visited[cur_index]
            last_branch = visited[cur_index + 1][1]

        # Return the current node, generating branch, index and the generating
        # branch of the last visited node before the current node.
        return cur_node, cur_branch, cur_index, last_branch

    def search_root(self, n: int, root: KSRMTreeNode, /) -> typing.Generator[KSRMTreeNode, None, None]:
        """Depth-first branch-and-bound generative search function (in pre-order, NLMR), with backtracking and pruning, on the KSRM coprime pairs trees, starting from the given root node.

        The given root node need not be the canonical roots, :math:`(2, 1)`,
        :math:`(3, 1)`, but can be any of their successor nodes.

        It is required that :math:`n \\geq 2`, otherwise a
        :py:class:`ValueError` is raised.

        The search implementation is an iterative version of a depth-first
        branch-and-bound search (DFS) procedure, with backtracking and pruning,
        in which nodes are traversed in NLMR pre-order (root -> left -> mid ->
        right) and bounds and checks are applied to the nodes, including
        pruning failed or unnecessary nodes, before further traversal or
        backtracking:
        
        #. Visit the current node :math:`(a, b)` and check :math:`a \\leq n`.
        #. If the check is successful iteratively traverse the current node's
           first child and its children, then the second child and its 
           children, and then the third child and its children, applying the
           check :math:`a \\leq n` to each visited node.
        #. If a check fails for any node backtrack to the nearest previously
           visited node which meets a stricter check :math:`a < n` and which
           has unvisited child nodes, while pruning all visited intermediate
           nodes after the backtracked target node and leading up to the failed
           node, including the failed node. By design the backtracked target
           node will have untraversed children on at least one branch, and the
           traversal can begin again, as described above.

        Parameters
        ----------
        n : int
            The positive integer for which coprime pairs :math:`(a, b)`, with
            :math:`1 \\leq b < a \\leq n`, are sought.

        root : tuple
            The "root" node from which to search - this can be either of the
            canonical roots, :math:`(2, 1)`, :math:`(3, 1)`, but also any of
            their successor nodes.

        Raises
        ------
        ValueError
            If ``n`` is not an integer or is :math:`< 2`.

        Yields
        ------
        tuple
            Pairs of coprime integers :math:`(a, b)`, with
            :math:`1 \\leq b < a \\leq n`.

        Examples
        --------
        Searching from the root :math:`(2, 1)` for coprime pairs for
        :math:`n = 5`:

        >>> tree = KSRMTree()
        >>> list(tree.search_root(5, (2, 1)))
        [(2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1)]
        >>> assert tree.roots[0] == (2, 1)
        >>> list(tree.search_root(5, tree.roots[0]))
        [(2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1)]

        The same type of search from the root :math:`(3, 1)`:

        >>> list(tree.search_root(5, (3, 1)))
        [(3, 1), (5, 3), (5, 1)]
        >>> assert tree.roots[1] == (3, 1)
        >>> list(tree.search_root(5, tree.roots[1]))
        [(3, 1), (5, 3), (5, 1)]
        """
        # Input validation.
        if not isinstance(n, int) or n <= 1 or not math.gcd(*root) == 1:
            raise ValueError(
                "`n` must be a positive integer >= 2, and `root` must be a "
                "coprime pair (r, s) for integers r > s >= 1"
            )

        if n < root[0]:
            return

        # A stack to store visited nodes and their generating branches.
        visited = []

        # A counter to store the number of nodes searched (or visited) -
        # useful for debugging and also for optimising the search
        # implementation.
        num_nodes_searched = 0

        # Start at the root, initialising variables for the current node
        # and generating branch to that of the root node, and also 
        # initialising a variable to store the generating branch of the
        # successor node of the current node.
        cur_node = root
        cur_branch = last_branch = None
        visited.append((cur_node, cur_branch))
        num_nodes_searched += 1

        # Generate the root
        yield cur_node
                    
        # The iterative backtracking depth-first branch-and-bound search
        # (pre-order, LNMR), with pruning of intermediate and failed nodes.
        while True:
            # If starting from either root, which do not have generating
            # branches, set the current branch to branch #1.
            if cur_branch is None:
                cur_branch = self.branches[0]

            # Generate and visit the next node ``(a, b)``, where ``1 <= b < a``
            # and ``gcd(a, b) = 1`` is guaranteed by the nature of the
            # generating branches.
            cur_node = cur_branch(*cur_node)
            visited.append((cur_node, cur_branch))
            num_nodes_searched += 1

            # If the node satisfies ``a <= n`` and generate it, then update the
            # variable storing the generating branch of the successor node of
            # the current node, and set the current (next generating) branch to
            # branch #1, and continue the DFS.
            #
            # If the node does not satisfy ``a <= n`` backtrack to the nearest
            # satisfying non-root node, prune any unnecessary nodes as needed,
            # and continue the DFS on unexplored branches. If there are no
            # nearest satisfying non-root nodes and all remaining branches have
            # been explored the DFS has ended, and so exit.
            if cur_node[0] <= n:
                yield cur_node
                last_branch = cur_branch
                cur_branch = self.branches[0]
                continue
            else:
                # Backtrack to the nearest satisfying target node, which will
                # become the current node; the current branch and current
                # node index are also updated, as is the variable storing the
                # generating branch of the successor node of the target/current
                # node.
                cur_node, cur_branch, cur_index, last_branch = self._backtrack(n, visited, node_bound=n)

                # Prune all visited intermediate nodes after the backtracked
                # target node leading up to the failed node, including the
                # failed node.
                visited[cur_index + 1:] = []

                # If we've reached the root node, and it has no untraversed
                # children, then we've finished our DFS, so return.
                if cur_node == root and last_branch == self.branches[-1]:
                    return

                # Otherwise, switch to the generating branch of the "next"
                # child node - branch #2 if the current branch is branch #1, or
                # branch #3 (the last branch) if the current branch is #2 - and
                # continue the DFS.
                cur_branch = self.branches[1] if last_branch.name == self.branches[0].name else self.branches[-1]
                continue

        # Not strictly required, but this has been inserted to make
        # debugging easier.
        return

    def search(self, n: int, /) -> typing.Generator[KSRMTreeNode, None, None]:
        """Depth-first branch-and-bound generative search function (in pre-order, NLMR) on the KSRM coprime pairs trees to find all pairs of coprime (positive) integers not exceeding the given integer :math:`n \\geq 1`.
    
        See the :py:meth:`~continuedfractions.sequences.KSRMTree.search_root`
        method for details of the implementation for the root-based search.

        This method mainly calls the root-based search method
        :py:meth:`~continuedfractions.sequences.KSRMTree.search_root` for the
        two canonical roots :math:`(2, 1)` and :math:`(3, 1)`.

        The two KSRM trees are actually only traversed if :math:`n > 3`.

        Parameters
        ----------
        n : int
            The positive integer for which coprime pairs :math:`(a, b)`, with
            :math:`1 \\leq b < a \\leq n`, are sought.

        Raises
        ------
        ValueError
            If ``n`` is not an integer or is :math:`< 1`.

        Yields
        ------
        tuple
            Pairs of coprime integers :math:`(a, b)`, with
            :math:`1 \\leq b < a \\leq n`.

        Examples
        --------
        A few examples of invalid and valid searches:

        >>> tree = KSRMTree()
        >>> list(tree.search("not an integer"))
        Traceback (most recent call last):
        ...
        ValueError: `n` must be a positive integer.
        >>> list(tree.search(1))
        [(1, 1)]
        >>> list(tree.search(2))
        [(1, 1), (2, 1)]
        >>> list(tree.search(3))
        [(1, 1), (2, 1), (3, 2), (3, 1)]
        >>> list(tree.search(5))
        [(1, 1), (2, 1), (3, 2), (4, 3), (4, 1), (3, 1), (5, 4), (5, 3), (5, 2), (5, 1)]
        >>> list(tree.search(10))
        [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (8, 3), (7, 2), (5, 2), (8, 5), (9, 2), (4, 1), (7, 4), (9, 4), (6, 1), (8, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3), (5, 1), (9, 5), (7, 1), (9, 1), (10, 9), (10, 7), (10, 3), (10, 1)]
        """
        if not isinstance(n, int) or n < 1:
            raise ValueError("`n` must be a positive integer.")

        if n == 1:
            yield (1, 1)
        if n == 2:
            yield from ((1, 1), (2, 1))
        elif n == 3:
            yield from ((1, 1), (2, 1), (3, 2), (3, 1))
        elif n > 3:
            yield from chain(
                ((1, 1),),
                self.search_root(n - 1, self.roots[0]),
                self.search_root(n - 1, self.roots[1]),
                ((n, i) for i in _coprime_integers(n))
            )


def coprime_pairs(n: int, /) -> typing.Generator[tuple[int, int], None, None]:
    """Generates a sequence (tuple) of all pairs :math:`(a, b)` of (positive) coprime integers :math:`a, b` such that :math:`a, b <= n`.

    This is a simple but fast implementation of the naive :math:`\\bigO(n^2)``
    algorithm for finding pairs of coprime integers which do not exceed a given
    positive integer :math:`n`.

    It does **not** call on the
    :py:meth:`~continuedfractions.sequences.KSRMTree.search` method, which is
    not as fast as this one.

    A :py:class:`ValueError` is raised if ``n`` is not an :py:class:`int`
    or is an :py:class:`int` less than :math:`1`.

    Parameters
    ----------
    n : int
        The positive integer for which coprime pairs :math:`(a, b)`, with
        :math:`1 \\leq b < a \\leq n`, are sought.

    Raises
    ------
    ValueError
        If ``n`` is not an :py:class:`int` or is an :py:class:`int` less than
        :math:`1`.

    Yields
    ------
    tuple
        A :py:class:`tuple` of pairs of coprime integers :math:`(a, b)`, with
        :math:`1 \\leq b < a \\leq n`.

    Examples
    --------
    A few examples of coprime pairs generation:

    >>> tuple(coprime_pairs(1))
    ((1, 1),)
    >>> tuple(coprime_pairs(2))
    ((1, 1), (2, 1))
    >>> tuple(coprime_pairs(3))
    ((1, 1), (2, 1), (3, 1), (3, 2))
    >>> tuple(coprime_pairs(5))
    ((1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4))
    >>> tuple(coprime_pairs(10))
    ((1, 1), (2, 1), (3, 1), (3, 2), (4, 1), (4, 3), (5, 1), (5, 2), (5, 3), (5, 4), (6, 1), (6, 5), (7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), (8, 1), (8, 3), (8, 5), (8, 7), (9, 1), (9, 2), (9, 4), (9, 5), (9, 7), (9, 8), (10, 1), (10, 3), (10, 7), (10, 9))
    >>> tuple(coprime_pairs("invalid input"))
    Traceback (most recent call last):
    ...
    ValueError: `n` must be a positive integer
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("`n` must be a positive integer")

    yield (1, 1)

    for i in range(1, n + 1):
        for j in (_j for _j in range(1, i) if _j < i and math.gcd(i, _j) == 1):
            yield (i, j)


class FareyFraction(ContinuedFraction):
    """A simple wrapper class for Farey fractions, subclassing :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`.
    """


def farey_sequence(n: int, /) -> typing.Generator[FareyFraction, None, None]:
    """Generates an (ordered) sequence (tuple) of rational numbers forming the Farey sequence of order :math:`n`.

    The elements of the sequence are yielded as
    :py:class:`~continuedfractions.sequences.FareyFraction`
    instances, in ascending order of magnitude.

    See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/sequences.html#sequences-farey-sequences>`_
    for more details.

    Parameters
    ----------
    n : int:
        The order of the Farey sequence.

    Raises
    ------
    ValueError
        If :math:`n` is not a positive integer.

    Yields
    ------
    FareyFraction
        A sequence of
        :py:class:`~continuedfractions.sequences.FareyFraction`
        instances representing the elements of the Farey sequence of order
        :math:`n`, in ascending order of magnitude.

    Examples
    --------
    >>> tuple(farey_sequence(1))
    (FareyFraction(0, 1), FareyFraction(1, 1))
    >>> tuple(farey_sequence(2))
    (FareyFraction(0, 1), FareyFraction(1, 2), FareyFraction(1, 1))
    >>> tuple(farey_sequence(3))
    (FareyFraction(0, 1), FareyFraction(1, 3), FareyFraction(1, 2), FareyFraction(2, 3), FareyFraction(1, 1))
    >>> tuple(farey_sequence(4))
    (FareyFraction(0, 1), FareyFraction(1, 4), FareyFraction(1, 3), FareyFraction(1, 2), FareyFraction(2, 3), FareyFraction(3, 4), FareyFraction(1, 1))
    >>> tuple(farey_sequence(5))
    (FareyFraction(0, 1), FareyFraction(1, 5), FareyFraction(1, 4), FareyFraction(1, 3), FareyFraction(2, 5), FareyFraction(1, 2), FareyFraction(3, 5), FareyFraction(2, 3), FareyFraction(3, 4), FareyFraction(4, 5), FareyFraction(1, 1))
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("`n` must be a positive integer")

    if n == 1:
        yield from (FareyFraction(0, 1), FareyFraction(1, 1))
    else:
        yield FareyFraction(0, 1)
        yield from sorted(FareyFraction(q, p) for (p, q) in coprime_pairs(n))


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     PYTHONPATH="src" python3 -m doctest -v src/continuedfractions/sequences.py
    #
    import doctest
    doctest.testmod()
