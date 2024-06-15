from __future__ import annotations


__all__ = [
    'coprime_integers',
    'coprime_integers_generator',
    'coprime_pairs',
    'coprime_pairs_generator',
    'farey_sequence',
    'farey_sequence_generator',
    'KSRMTree',
]


# -- IMPORTS --

# -- Standard libraries --
import functools
import math
import sys

from itertools import chain, product, starmap
from pathlib import Path
from typing import Generator, Literal, TypeAlias

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.utils import NamedCallableProxy
from continuedfractions.continuedfraction import ContinuedFraction

KSRMNode: TypeAlias = tuple[int, int]   #: Custom type for nodes of the KSRM coprime pairs tree
KSRMBranch: NamedCallableProxy          #: Custom type for generating branches of the KSRM coprime pairs tree


def coprime_integers_generator(n: int, /, *, start: int = 1, stop: int = None) -> Generator[int, None, None]:
    """Generates a sequence of (positive) integers :math:`1 \\leq m < n` coprime to a given positive integer :math:`n`.

    The tuple is sorted in descending order of magnitude.

    The optional ``start`` and ``stop`` parameters can be used to bound the
    the range of (positive) integers in which integers coprime to the given
    :math:`n` are sought.

    For :math:`n = 1, 2` the ``start`` value is effectively ignored, but
    if :math:`n > 1` then the ``start`` value must be an integer in the range
    :math:`1..n - 1`.

    The ``stop`` value defaults to ``None``, which is then internally
    initialised to :math:`n`; if :math:`n > 1` and ``stop`` is given then it
    must be an integer in the range :math:`\\text{start} + 1..n`.

    Parameters
    ----------
    n : int
        The positive integer for which (positive) coprime integers
        :math:`m < n` are sought.

    start : int, default=1
        The lower bound of the range of (positive) integers in which integers
        coprime to the given :math:`n` are sought. For :math:`n = 1, 2` the
        ``start`` value is effectively ignored, but if :math:`n > 1` then the
        ``start`` value must be in the range :math:`1..n - 1`.

    stop : int, default=None
        The upper bound of the range of (positive) integers in which integers
        coprime to the given :math:`n` are sought. The ``stop`` value defaults
        to ``None``, which is then internally initialised to :math:`n`; if
        :math:`n > 1` and ``stop`` is given then it must be an integer in the
        range :math:`\\text{start} + 1..n`.

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

    >>> tuple(coprime_integers_generator(1))
    (1,)
    >>> tuple(coprime_integers_generator(2))
    (1,)
    >>> tuple(coprime_integers_generator(3))
    (2, 1)
    >>> tuple(coprime_integers_generator(4))
    (3, 1)
    >>> tuple(coprime_integers_generator(5))
    (4, 3, 2, 1)
    >>> tuple(coprime_integers_generator(6))
    (5, 1)
    >>> tuple(coprime_integers_generator(7))
    (6, 5, 4, 3, 2, 1)
    >>> tuple(coprime_integers_generator(8))
    (7, 5, 3, 1)
    >>> tuple(coprime_integers_generator(9))
    (8, 7, 5, 4, 2, 1)
    >>> tuple(coprime_integers_generator(10))
    (9, 7, 3, 1)
    >>> tuple(coprime_integers_generator(11))
    (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)

    Examples using custom ``start`` and ``stop`` values:

    >>> tuple(coprime_integers_generator(3, start=0))
    Traceback (most recent call last):
    ...
    ValueError: `n` must be a positive integer; if `n` > 1 then the `start` value must be a positive integer in the range 1..n - 1; and if given the `stop` value must be a positive integer in the range `start` + 1..n
    >>> tuple(coprime_integers_generator(3, start=2))
    (2,)
    >>> tuple(coprime_integers_generator(3, start=3))
    Traceback (most recent call last):
    ...
    ValueError: `n` must be a positive integer; if `n` > 1 then the `start` value must be a positive integer in the range 1..n - 1; and if given the `stop` value must be a positive integer in the range `start` + 1..n
    >>> tuple(coprime_integers_generator(23, start=5, stop=21))
    (21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5)
    >>> tuple(coprime_integers_generator(5, start=2))
    (4, 3, 2)
    >>> tuple(coprime_integers_generator(5, start=3))
    (4, 3)
    >>> tuple(coprime_integers_generator(6, start=2))
    (5,)
    >>> tuple(coprime_integers_generator(6, start=3))
    (5,)
    >>> tuple(coprime_integers_generator(6, start=4))
    (5,)
    >>> tuple(coprime_integers_generator(7, start=2))
    (6, 5, 4, 3, 2)
    >>> tuple(coprime_integers_generator(7, start=3))
    (6, 5, 4, 3)
    >>> tuple(coprime_integers_generator(7, start=4))
    (6, 5, 4)
    >>> tuple(coprime_integers_generator(7, start=5))
    (6, 5)
    """
    if not isinstance(n, int) or n < 1 or (n > 1 and start not in range(1, n)) or (n > 1 and stop and stop not in range(start + 1, n + 1)):
        raise ValueError(
            "`n` must be a positive integer; if `n` > 1 then the "
            "`start` value must be a positive integer in the range 1..n - 1; "
            "and if given the `stop` value must be a positive integer in the "
            "range `start` + 1..n"
        )

    if n in (1, 2):
        yield 1
    else:
        stop = stop or n
        q, r = divmod((stop - start + 1), 10 ** 3)

        if q == 0:
            yield from filter(
                lambda m: math.gcd(m, n) == 1,
                range(stop, start - 1, -1)
            )
        else:
            _start = ((10 ** 3) * q) + (1 if r > 0 else 0)
            
            while _start >= start:
                yield from filter(
                    lambda m: math.gcd(m, n) == 1,
                    range(stop, _start - 1, -1)
                )
                stop = _start - 1
                q -= 1
                _start = ((10 ** 3) * q) + 1


@functools.cache
def coprime_integers(n: int, /, *, start: int = 1, stop: int = None) -> tuple[int]:
    """Returns a sequence of (positive) integers :math:`1 \\leq m < n` coprime to a given positive integer :math:`n`.

    Wrapper of :py:class:`~continuedfractions.sequences.coprime_integers_generator`.

    The tuple is sorted in descending order of magnitude.

    The optional ``start`` and ``stop`` parameters can be used to bound the
    the range of (positive) integers in which integers coprime to the given
    :math:`n` are sought.

    For :math:`n = 1, 2` the ``start`` value is effectively ignored, but
    if :math:`n > 1` then the ``start`` value must be an integer in the range
    :math:`1..n - 1`.

    The ``stop`` value defaults to ``None``, which is then internally
    initialised to :math:`n`; if :math:`n > 1` and ``stop`` is given then it
    must be an integer in the range :math:`\\text{start} + 1..n`.

    Parameters
    ----------
    n : int
        The positive integer for which (positive) coprime integers
        :math:`m < n` are sought.

    start : int, default=1
        The lower bound of the range of (positive) integers in which integers
        coprime to the given :math:`n` are sought. For :math:`n = 1, 2` the
        ``start`` value is effectively ignored, but if :math:`n > 1` then the
        ``start`` value must be in the range :math:`1..n - 1`.

    stop : int, default=None
        The upper bound of the range of (positive) integers in which integers
        coprime to the given :math:`n` are sought. The ``stop`` value defaults
        to ``None``, which is then internally initialised to :math:`n`; if
        :math:`n > 1` and ``stop`` is given then it must be an integer in the
        range :math:`\\text{start} + 1..n`.

    Returns
    -------
    tuple
        A sequence of (positive) integers :math:`1 \\leq m < n` coprime to a
        given positive integer :math:`n`.

    Examples
    --------
    Examples using the default ``start`` and ``stop`` values:

    >>> coprime_integers(1)
    (1,)
    >>> coprime_integers(2)
    (1,)
    >>> coprime_integers(3)
    (2, 1)
    >>> coprime_integers(4)
    (3, 1)
    >>> coprime_integers(5)
    (4, 3, 2, 1)
    >>> coprime_integers(6)
    (5, 1)
    >>> coprime_integers(7)
    (6, 5, 4, 3, 2, 1)
    >>> coprime_integers(8)
    (7, 5, 3, 1)
    >>> coprime_integers(9)
    (8, 7, 5, 4, 2, 1)
    >>> coprime_integers(10)
    (9, 7, 3, 1)
    >>> coprime_integers(11)
    (10, 9, 8, 7, 6, 5, 4, 3, 2, 1)

    Examples using custom ``start`` and ``stop`` values:

    >>> coprime_integers(3, start=2)
    (2,)
    >>> coprime_integers(3, start=3)
    Traceback (most recent call last):
    ...    
    ValueError: `n` must be a positive integer; if `n` > 1 then the `start` value must be a positive integer in the range 1..n - 1; and if given the `stop` value must be a positive integer in the range `start` + 1..n
    >>> coprime_integers(23, start=5, stop=21)
    (21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5)
    >>> coprime_integers(5, start=2)
    (4, 3, 2)
    >>> coprime_integers(5, start=3)
    (4, 3)
    >>> coprime_integers(6, start=2)
    (5,)
    >>> coprime_integers(6, start=3)
    (5,)
    >>> coprime_integers(6, start=4)
    (5,)
    >>> coprime_integers(7, start=2)
    (6, 5, 4, 3, 2)
    >>> coprime_integers(7, start=3)
    (6, 5, 4, 3)
    >>> coprime_integers(7, start=4)
    (6, 5, 4)
    >>> coprime_integers(7, start=5)
    (6, 5)
    """
    return tuple(coprime_integers_generator(n, start=start, stop=stop))

# These lists will be initialised every time the module is (re-)loaded, and
# has the effect of caching the function for the values of ``n`` which are
# are used below: 1 to 1000, and then 10 ^^ 4, 10 ^^ 5, 10 ^^ 6, 10 ^^ 7.
[coprime_integers(n) for n in range(1, 1001)]
[coprime_integers(10 ** k) for k in range(4, 8)]


class KSRMTree:
    """An implicit/generative class implementation of the Kanga-Saunders-Randall-Mitchell (KSRM) ternary trees for representing and generating pairs of all (positive) coprime integers.

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

    _roots: tuple[KSRMNode, KSRMNode]

    _branches: tuple[KSRMBranch]    # noqa: F821

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
    def roots(self) -> Literal[tuple([(2, 1), (3, 1)])]:
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
    def branches(self) -> tuple[KSRMBranch]:    # noqa: F821
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
        visited: list[tuple[KSRMNode, KSRMBranch]],     # noqa: F821
        /,
        *,
        node_bound: int = None
    ) -> tuple[KSRMNode, KSRMBranch, int, KSRMBranch]:  # noqa: F821
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

    def search_root(self, n: int, root: KSRMNode, /) -> Generator[KSRMNode, None, None]:
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
                # branch #3 if the current branch is #2 - and continue the
                # search.
                cur_branch = self.branches[1] if last_branch == self.branches[0] else self.branches[-1]
                continue

        # Not strictly required, but this has been inserted to make
        # debugging easier.
        return

    def search(self, n: int, /) -> Generator[KSRMNode, None, None]:
        """Depth-first branch-and-bound generative search function (in pre-order, NLMR) on the KSRM coprime pairs trees to find all pairs of coprime (positive) integers not exceeding the given integer :math:`n \\geq 1`.
    
        See the :py:meth:`~continuedfractions.sequences.KSRMTree.search_root`
        method for details of the implementation for the root-based search.

        This method mainly calls the root-based search method
        :py:meth:`~continuedfractions.sequences.KSRMTree.search_root` for the
        two canonical roots :math:`(2, 1)` and :math:`(3, 1)`.

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
        ValueError: `n` must be a positive integer >= 1
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
            raise ValueError("`n` must be a positive integer >= 1")

        yield 1, 1

        if n == 2:
            yield 2, 1
        elif n > 1:
            yield from self.search_root(n - 1, self.roots[0])

        if n > 2:
            yield from self.search_root(n - 1, self.roots[1])
            yield from tuple(product([n], coprime_integers(n)))


def coprime_pairs_generator(n: int, /) -> Generator[KSRMNode, None, None]:
    """Generates a sequence (tuple) of all pairs of (positive) coprime integers :math:`<= n`.

    Calls the KSRM tree :py:meth:`~continuedfractions.sequences.KSRMTree.search`
    to perform the search up to :math:`n - 1` and then uses
    :py:func:`~continuedfractions.sequences.coprime_integers` for the search
    for pairs involving :math:`n`.

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

    >>> tuple(coprime_pairs_generator(1))
    ((1, 1),)
    >>> tuple(coprime_pairs_generator(2))
    ((1, 1), (2, 1))
    >>> tuple(coprime_pairs_generator(3))
    ((1, 1), (2, 1), (3, 2), (3, 1))
    >>> tuple(coprime_pairs_generator(5))
    ((1, 1), (2, 1), (3, 2), (3, 1), (4, 3), (4, 1), (5, 4), (5, 3), (5, 2), (5, 1))
    >>> tuple(coprime_pairs_generator(10))
    ((1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (8, 3), (7, 2), (5, 2), (8, 5), (4, 1), (7, 4), (6, 1), (8, 1), (3, 1), (5, 3), (7, 5), (7, 3), (5, 1), (7, 1), (9, 8), (9, 7), (9, 5), (9, 4), (9, 2), (9, 1), (10, 9), (10, 7), (10, 3), (10, 1))
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("`n` must be a positive integer >= 1")

    if n == 1:
        yield (1, 1)
    else:
        yield from chain(
            KSRMTree().search(n - 1),
            product([n], coprime_integers(n))
        )


@functools.cache
def coprime_pairs(n: int, /) -> tuple[KSRMNode]:
    """Returns a sequence (tuple) of all pairs of (positive) coprime integers :math:`<= n`.

    Wrapper of :py:func:`~continuedfractions.sequences.coprime_pairs_generator`.

    Parameters
    ----------
    n : int
        The positive integer for which coprime pairs :math:`(a, b)`, with
        :math:`1 \\leq b < a \\leq n`, are sought.

    Returns
    -------
    tuple
        A :py:class:`tuple` of pairs of coprime integers :math:`(a, b)`, with
        :math:`1 \\leq b < a \\leq n`.

    Examples
    --------
    A few examples of computing coprime pairs:

    >>> coprime_pairs(1)
    ((1, 1),)
    >>> coprime_pairs(2)
    ((1, 1), (2, 1))
    >>> coprime_pairs(3)
    ((1, 1), (2, 1), (3, 2), (3, 1))
    >>> coprime_pairs(5)
    ((1, 1), (2, 1), (3, 2), (3, 1), (4, 3), (4, 1), (5, 4), (5, 3), (5, 2), (5, 1))
    >>> coprime_pairs(10)
    ((1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (8, 3), (7, 2), (5, 2), (8, 5), (4, 1), (7, 4), (6, 1), (8, 1), (3, 1), (5, 3), (7, 5), (7, 3), (5, 1), (7, 1), (9, 8), (9, 7), (9, 5), (9, 4), (9, 2), (9, 1), (10, 9), (10, 7), (10, 3), (10, 1))
    """
    return tuple(coprime_pairs_generator(n))


# These lists will be initialised every time the module is (re-)loaded, and
# has the effect of caching the function for the values of ``n`` which are
# are used below: 1 to 101.
[coprime_pairs(n) for n in range(1, 101)]


def farey_sequence_generator(n: int, /) -> Generator[ContinuedFraction, None, None]:
    """Generates an (ordered) sequence (tuple) of rational numbers forming the Farey sequence of order :math:`n`.

    The elements of the sequence are yielded as
    :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
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
    ContinuedFraction
        A sequence of
        :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
        instances representing the elements of the Farey sequence of order
        :math:`n`, in ascending order of magnitude.

    Examples
    --------
    >>> tuple(farey_sequence_generator(1))
    (ContinuedFraction(0, 1), ContinuedFraction(1, 1))
    >>> tuple(farey_sequence_generator(2))
    (ContinuedFraction(0, 1), ContinuedFraction(1, 2), ContinuedFraction(1, 1))
    >>> tuple(farey_sequence_generator(3))
    (ContinuedFraction(0, 1), ContinuedFraction(1, 3), ContinuedFraction(1, 2), ContinuedFraction(2, 3), ContinuedFraction(1, 1))
    >>> tuple(farey_sequence_generator(4))
    (ContinuedFraction(0, 1), ContinuedFraction(1, 4), ContinuedFraction(1, 3), ContinuedFraction(1, 2), ContinuedFraction(2, 3), ContinuedFraction(3, 4), ContinuedFraction(1, 1))
    >>> tuple(farey_sequence_generator(5))
    (ContinuedFraction(0, 1), ContinuedFraction(1, 5), ContinuedFraction(1, 4), ContinuedFraction(1, 3), ContinuedFraction(2, 5), ContinuedFraction(1, 2), ContinuedFraction(3, 5), ContinuedFraction(2, 3), ContinuedFraction(3, 4), ContinuedFraction(4, 5), ContinuedFraction(1, 1))
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("`n` must be a positive integer >= 1")

    if n == 1:
        yield from (ContinuedFraction(0, 1), ContinuedFraction(1, 1))
    else:
        yield from chain(
            (ContinuedFraction(0, 1),),
            sorted(
                starmap(
                    ContinuedFraction,
                    starmap(lambda *x: tuple(reversed(x)), coprime_pairs(n))
                )
            )
        )


@functools.cache
def farey_sequence(n: int, /) -> tuple[ContinuedFraction]:
    """Returns an (ordered) sequence (tuple) of rational numbers forming the Farey sequence of order :math:`n`.

    Wrapper of :py:func:`~continuedfractions.sequences.farey_sequence_generator`.

    The elements of the sequence are returned as
    :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
    instances, in ascending order of magnitude.

    See the `documentation <https://continuedfractions.readthedocs.io/en/latest/sources/sequences.html#sequences-farey-sequences>`_
    for more details.

    Parameters
    ----------
    n : int:
        The order of the Farey sequence.

    Returns
    -------
    tuple
        A :py:class:`tuple` of ``ContinuedFraction`` instances representing the
        elements of the Farey sequence of order :math:`n`, generated in
        ascending order of magnitude.

    Examples
    --------
    >>> farey_sequence(1)
    (ContinuedFraction(0, 1), ContinuedFraction(1, 1))
    >>> farey_sequence(2)
    (ContinuedFraction(0, 1), ContinuedFraction(1, 2), ContinuedFraction(1, 1))
    >>> farey_sequence(3)
    (ContinuedFraction(0, 1), ContinuedFraction(1, 3), ContinuedFraction(1, 2), ContinuedFraction(2, 3), ContinuedFraction(1, 1))
    >>> farey_sequence(4)
    (ContinuedFraction(0, 1), ContinuedFraction(1, 4), ContinuedFraction(1, 3), ContinuedFraction(1, 2), ContinuedFraction(2, 3), ContinuedFraction(3, 4), ContinuedFraction(1, 1))
    >>> farey_sequence(5)
    (ContinuedFraction(0, 1), ContinuedFraction(1, 5), ContinuedFraction(1, 4), ContinuedFraction(1, 3), ContinuedFraction(2, 5), ContinuedFraction(1, 2), ContinuedFraction(3, 5), ContinuedFraction(2, 3), ContinuedFraction(3, 4), ContinuedFraction(4, 5), ContinuedFraction(1, 1))
    """
    return tuple(farey_sequence_generator(n))


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/sequences.py
    #
    import doctest
    doctest.testmod()
