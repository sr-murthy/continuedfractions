from __future__ import annotations


__all__ = [
    'coprime_pairs',
    'farey_sequence',
    'KSRMTree',
]


# -- IMPORTS --

# -- Standard libraries --
import functools
import sys

from itertools import starmap
from pathlib import Path
from typing import Callable, Generator, Literal, TypeAlias

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.utils import NamedCallableProxy
from continuedfractions.continuedfraction import ContinuedFraction

#: Custom types for annotation in this library
KSRMNode: TypeAlias = tuple[int, int]
KSRMBranch: NamedCallableProxy


class KSRMTree:
    """An implicit/generative tree class implementation of the Kanga-Saunders-Randall-Mitchell (KSRM) disjointed ternary tree for pairs of (positive) coprime integers.

    The term "KSRM tree" is the author's, and refers to a consolidation of
    related but different trees presented by different authors in the
    following papers:

    #. A. R. Kanga, *The Family Tree of Pythagorean Triplets*, Bulletin of the Institute of Mathematics and Its Applications **26**, 15 (1990).
    #. R. Saunders and T. Randall, *The Family Tree of the Pythagorean Triplets Revisited*, The Mathematical Gazette **78**, 190 (1994).
    #. D. W. Mitchell, *An Alternative Characterisation of All Primitive Pythagorean Triples*, The Mathematical Gazette **85**, 273 (2001).

    The trees presented in these papers are directly related to so-called
    `primitive Pythagorean triples <https://en.wikipedia.org/wiki/Pythagorean_triple#Elementary_properties_of_primitive_Pythagorean_triples>`_,
    but have a fundamental consequence for the generation of coprime pairs: all
    pairs of (positive) coprime integers :math:`(r, s)`, can be represented as
    nodes in a disjoint ternary tree, with two "parents" (root nodes),
    :math:`(2, 1)` and :math:`(3, 1)`, in which each parent node has exactly
    three child nodes of the form:

    .. math::

       (r^\\prime, s^\\prime) = \\begin{cases}
                                (2r - s, r), \\hskip{3em} \\text{ branch #} 1 \\\\
                                (2r + s, r), \\hskip{3em} \\text{ branch #} 2 \\\\
                                (r + 2s, s), \\hskip{3em} \\text{ branch #} 3                   
                                \\end{cases}

    where :math:`r, s \\geq 1` and :math:`r > s`, with two pairs of initial
    values given by :math:`(r=2, s=1)`, and :math:`(r=3, s=1)`. Each node in
    the tree is the parent of all nodes that branch from it, but the nodes
    :math:`(2, 1)` and :math:`(3, 1)` are canonical.

    This can be understood more concretely as a generative procedure for
    pairs of (positive) coprime integers, namely: start separately from
    the parents :math:`(2, 1)` and :math:`(3, 1)`, and apply the functions
    given by the mappings below to each parent:

    .. math::

       \\begin{align}
       (r, s) &\\longmapsto (2r - s, r) \\\\
       (r, s) &\\longmapsto (2r + s, r) \\\\
       (r, s) &\\longmapsto (r + 2s, s)
       \\end{align}

    producing the "1st generation" of :math:`3 + 3 = 6` triplets. Repeat the
    same procedure ad infinitum for each generation.

    For each integer :math:`k \\geq 1` the :math:`k`-th generation (for both
    trees) will have a total of :math:`2 \\cdot 3^k` children, and the total
    number of all members up to the :math:`k`-generation will be
    :math:`2(1 + 3 + 3^2 + \\ldots 3^k) = 3(3^k - 1)`.

    Given a positive integer :math:`n` we may ask how many coprime pairs
    :math:`(r, s)` exist such that :math:`r \\leq n` (where as defined above
    we may assume :math:`r > s`). The generative procedure described above,
    augmented with a strategy of pruning branches whose root nodes
    :math:`(r, s)` do not satisfy the condition :math:`r \\leq n`, including
    all the satisfying intermediate visited nodes, will always terminate and
    provide an answer with:

    .. math::

       1 + \\phi(1) + \\phi(2) + \\cdots + \\phi(n) = 1 + \\sum_{k = 1}^n \\phi(k)

    coprime pairs, where :math:`\\phi(k)` is `Euler's totient function <https://en.wikipedia.org/wiki/Euler%27s_totient_function>`_.

    This requires a brief explanation: if :math:`\\mathcal{C}_n` denotes the
    set of all pairwise coprime integers :math:`r, s \\geq 1`, with
    :math:`r > s`, such that :math:`r \\leq n`, then :math:`\\mathcal{C}_n`
    will only contain pairs of type :math:`(r, k)`, for some
    :math:`r < k \\leq n` such that :math:`(r, k) = 1`. For each such :math:`k`
    there are :math:`\\phi(k)` integers, which proves the relation above.
    """

    # The two slots for the private attributes for the key tree features - the
    # two roots ``(2, 1), (3, 1)``, and the three branch generating functions.
    __slots__ = ('_roots', '_branches')

    _roots: tuple[KSRMNode, KSRMNode]

    _branches: tuple[KSRMBranch]

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
    def roots(self) -> Literal[(2, 1), (3, 1)]:
        """:py:class:`tuple`: The tuple of roots of the KSRM tree, which are :math:`(2, 1)` and :math:`(3, 1)`.

        For more details see the following papers:

        #. A. R. Kanga, *The Family Tree of Pythagorean Triplets*, Bulletin of the Institute of Mathematics and Its Applications **26**, 15 (1990).
        #. R. Saunders and T. Randall, *The Family Tree of the Pythagorean Triplets Revisited*, The Mathematical Gazette **78**, 190 (1994).
        #. D. W. Mitchell, *An Alternative Characterisation of All Primitive Pythagorean Triples*, The Mathematical Gazette **85**, 273 (2001).

        Examples
        --------
        >>> KSRMTree().roots
        ((2, 1), (3, 1))
        """
        return self._roots

    @property
    def branches(self) -> tuple[KSRMBranch]:
        """:py:class:`tuple`: The tuple of three branch generating functions of the KSRM tree.

        There are three branch generating functions, given by the mappings:

        .. math::

           \\begin{align}
           (r, s) &\\longmapsto (2r - s, r) \\\\
           (r, s) &\\longmapsto (2r + s, r) \\\\
           (r, s) &\\longmapsto (r + 2s, s)
           \\end{align}

        For more details see the following papers:

        #. A. R. Kanga, *The Family Tree of Pythagorean Triplets*, Bulletin of the Institute of Mathematics and Its Applications **26**, 15 (1990).
        #. R. Saunders and T. Randall, *The Family Tree of the Pythagorean Triplets Revisited*, The Mathematical Gazette **78**, 190 (1994).
        #. D. W. Mitchell, *An Alternative Characterisation of All Primitive Pythagorean Triples*, The Mathematical Gazette **85**, 273 (2001).

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
        visited: list[tuple[KSRMNode, KSRMBranch]],
        /,
        *,
        node_bound: int = None
    ) -> tuple[KSRMNode, KSRMBranch, int, KSRMBranch]:
        """Backtracks on the KSRM coprime pairs tree.

        A private function that backtracks on the KSRM coprime pairs tree: the
        procedure is that, given a (positive) integer :math:`n > 2`, for which
        coprime pairs are being sought, and a sequence (list) of pairs of
        visited nodes and their associated generating branches in the KSRM
        tree, and assuming that the last element of the visited sequence
        contains the node that "failed", the function identifies the nearest
        previously visited node whose first component satisifes the test
        :math:`< n` **and** and whose associated generating branch is not equal
        to the third branch given by :math:`(x, y) \\longmapsto (x + 2y, y)`.

        .. note::

           One key property of the KSRM tree is that, for a given search value
           :math:`n`, if the current node is :math:`(r, s) = (n, s)` and the
           successor node on the first branch, :math:`(2r - s, r)`, fails the
           test :math:`2r - s \\leq n`, then so will the successor nodes on
           the second and third branches.

           This means in the case of a node failure in the search on the first
           branch, all three branches of the predecessor node of the failed
           node can be pruned in the sequence of visited nodes and generating
           branch pairs.

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
            A bound to check that :math:`r < n` for a node :math:`(r, s)`. The
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
        # Set the node bound for ``r``: so we require ``r < n`` for the
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
        # If the current node passes the test ``r < n` and we are not on the
        # last branch, return the current node, generating branch, index
        # and the generating branch of the last visited node before the current
        # node.
        while cur_index > 0:
            cur_index -= 1
            cur_node, cur_branch = visited[cur_index]
            last_branch = visited[cur_index + 1][1]

            if cur_node[0] < node_bound and last_branch != self.branches[-1]:
                return cur_node, cur_branch, cur_index, last_branch        

        # Return the current node, generating branch, index and the generating
        # branch of the last visited node before the current node.
        return cur_node, cur_branch, cur_index, last_branch

    def search_root(self, n: int, root: KSRMNode, /) -> Generator[KSRMNode, None, None]:
        """Backtracking depth-first branch-and-bound search (in pre-order, NLMR) of the KSRM coprime pairs tree from the given root node to find all pairs of coprime (positive) integers not exceeding the given integer :math:`n \\geq 1`.

        The given root node need not be the canonical roots, :math:`(2, 1)`,
        :math:`(3, 1)`, but can be any of their successor nodes.

        It is required that :math:`n \\geq 2`, otherwise a
        :py:class:`ValueError` is raised.

        The search implementation is an iterative version of a backtracking
        depth-first branch-and-bound search (DFS), in which nodes are traversed
        in pre-order, NLMR (next -> left -> mid -> right) and bounds and checks
        are applied to the nodes, before further traversal or backtracking:
        
        #. Visit the current node :math:`(r, s)` and check :math:`r \\leq n`.
        #. If the check is successful iteratively traverse the current node's
           first child and its children, then the second child and its 
           children, and then the third child and its children, applying the
           check :math:`r \\leq n` to each visited node.
        #. If a check fails for any node backtrack to the nearest previously
           visited node which meets a stricter check :math:`r < n` and which
           has unvisited child nodes, while pruning all visited intermediate
           nodes after the backtracked target node and leading up to the failed
           node, including the failed node. By design the backtracked target
           node will have untraversed children on at least one branch, and the
           traversal can begin again, as described above.

        .. note::

           One key property of the KSRM tree used in this implementation is
           that for a given integer :math:`n \\geq 1`, if the current node is
           :math:`(r, s) = (n, s)` and the child node on the first branch,
           :math:`(2r - s, r)`, fails the test :math:`2r - s \\leq n`, then
           so will the child nodes on the second and third branches, and
           thus all three children can be pruned.

        Parameters
        ----------
        n : int
            The positive integer for which coprime pairs :math:`(r, s)`, with
            :math:`1 \\leq s < r \\leq n`, are sought.

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
            Pairs of coprime integers :math:`(r, s)`, with
            :math:`1 \\leq s < r \\leq n`.

        Examples
        --------
        Searching from the root :math:`(2, 1)`:

        >>> tree = KSRMTree()
        >>> list(tree.search_root(5, (2, 1)))
        [(2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1)]
        >>> assert tree.roots[0] == (2, 1)
        >>> list(tree.search_root(5, tree.roots[0]))
        [(2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1)]

        Searching from the root :math:`(3, 1)`.

        >>> list(tree.search_root(5, (3, 1)))
        [(3, 1), (5, 3), (5, 1)]
        >>> assert tree.roots[1] == (3, 1)
        >>> list(tree.search_root(5, tree.roots[1]))
        [(3, 1), (5, 3), (5, 1)]

        Searching from the node :math:`(3, 2)`:

        >>> list(tree.search_root(10, (3, 2)))
        [(3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (10, 3), (8, 3), (7, 2)]
        """
        #import ipdb; ipdb.set_trace()
        # Input validation.
        if not isinstance(n, int) or n <= 1:
            raise ValueError("`n` must be a positive integer >= 2")

        # A stack to store visited nodes and their generating branches
        visited = []

        # Start at the root, initialising variables for the current node
        # and generating branch to that of the root node, and also 
        # initialising a variable to store the generating branch of the
        # successor node of the current node.
        cur_node = root
        cur_branch = last_branch = None
        visited.append((cur_node, cur_branch))

        # Generate the root.
        yield cur_node
                    
        # The iterative backtracking depth-first branch-and-bound search
        # (pre-order, LNMR), with pruning of intermediate and failed nodes.
        while True:
            # If starting from either root, which do not have generating
            # branches, set the current branch to branch #1.
            if cur_branch is None:
                cur_branch = self.branches[0]

            # Generate and visit the next node ``(r, s)``, where ``1 <= s < r``
            # and ``gcd(r, s) = 1`` is guaranteed by the nature of the
            # generating branches.
            cur_node = cur_branch(*cur_node)
            visited.append((cur_node, cur_branch))

            # If the node satisfies ``r <= n`` generate it, update the variable
            # storing the generating branch of the successor node of the
            # current node, and set the current (next generating) branch to
            # branch #1, and continue the DFS.
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
                # child node - branch #2 if the current branch is branch #2, or
                # branch #3 if the current branch is #2 - and continue the
                # search.
                cur_branch = self.branches[1] if last_branch == self.branches[0] else self.branches[-1]
                continue

        # Not strictly required, but this has been inserted to make
        # debugging easier.
        return

    def search(self, n: int, /) -> Generator[KSRMNode, None, None]:
        """Backtracking depth-first branch-and-bound search (in pre-order, NLMR) of the KSRM coprime pairs tree to find all pairs of coprime (positive) integers not exceeding the given integer :math:`n \\geq 1`.
    
        See the :py:meth:`~continuedfractions.sequences.KSRMTree.search_root`
        method for details of the implementation for the root-based search.

        This method simply calls the root-based search method for the two
        canonical roots :math:`(2, 1)` and :math:`(3, 1)`.

        Parameters
        ----------
        n : int
            The positive integer for which coprime pairs :math:`(r, s)`, with
            :math:`1 \\leq s < r \\leq n`, are sought.

        Raises
        ------
        ValueError
            If ``n`` is not an integer or is :math:`< 1`.

        Yields
        ------
        tuple
            Pairs of coprime integers :math:`(r, s)`, with
            :math:`1 \\leq s < r \\leq n`.

        Examples
        --------
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
        [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1), (3, 1), (5, 3), (5, 1)]
        >>> list(tree.search(10))
        [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (10, 3), (8, 3), (7, 2), (5, 2), (8, 5), (9, 2), (4, 1), (7, 4), (10, 7), (9, 4), (6, 1), (8, 1), (10, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3), (5, 1), (9, 5), (7, 1), (9, 1)]
        """
        #import ipdb; ipdb.set_trace()
        if not isinstance(n, int) or n < 1:
            raise ValueError("`n` must be a positive integer >= 1")

        yield 1, 1

        if n > 1:
            yield from self.search_root(n, self.roots[0])

        if n > 2:
            yield from self.search_root(n, self.roots[1])


def coprime_pairs(n: int, /) -> Generator[tuple[int], None, None]:
    """A function wrapper to generates a sequence of all pairs of (positive) coprime integers :math:`<= n`.

    Calls the :py:meth:`continuedfractions.sequences.KSRMTree.search` to
    perform the search.

    A :py:class:`ValueError` is raised if ``n`` is not an :py:class:`int`
    or is an :py:class:`int` less than :math:`1`.

    Parameters
    ----------
    n : int
        The positive integer for which coprime pairs :math:`(r, s)`, with
        :math:`1 \\leq s < r \\leq n`, are sought.

    Raises
    ------
    ValueError
        If ``n`` is not an :py:class:`int` or is an :py:class:`int` less than
        :math:`1`.

    Yields
    ------
    tuple
        Pairs of coprime integers :math:`(r, s)`, with
        :math:`1 \\leq s < r \\leq n`.

    Examples
    --------
    >>> list(coprime_pairs(1))
    [(1, 1)]
    >>> list(coprime_pairs(2))
    [(1, 1), (2, 1)]
    >>> list(coprime_pairs(3))
    [(1, 1), (2, 1), (3, 2), (3, 1)]
    >>> list(coprime_pairs(5))
    [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1), (3, 1), (5, 3), (5, 1)]
    >>> list(coprime_pairs(10))
    [(1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7), (9, 8), (10, 9), (10, 3), (8, 3), (7, 2), (5, 2), (8, 5), (9, 2), (4, 1), (7, 4), (10, 7), (9, 4), (6, 1), (8, 1), (10, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3), (5, 1), (9, 5), (7, 1), (9, 1)]
    """
    if not isinstance(n, int) or n < 1:
        raise ValueError("`n` must be a positive integer >= 1")

    yield from KSRMTree().search(n)


def farey_sequence(n: int, /) -> Generator[ContinuedFraction, None, None]:
    """Generates the sequence of rational numbers forming the Farey sequence of order :math:`n`.

    The elements of the sequence are generated as
    :py:class:`~continuedfractions.continuedfraction.ContinuedFraction`
    instances, in ascending order of magnitude.

    The `Farey sequence <https://en.wikipedia.org/wiki/Farey_sequence>`_
    :math:`F_n` of order :math:`n` is an (ordered) sequence of rational numbers
    which is defined recursively as follows:

    .. math::

       \\begin{align}
       F_1 &= \\left(\\frac{0}{1}, \\frac{1}{1}\\right) \\\\
       F_k &= \\left(\\frac{a}{b}\\right) \\text{ s.t. } (a, b) = 1 \\text{ and } b \\leq n,
              \\hskip{3em} k \\geq 2
       \\end{align}

    The restriction :math:`(a, b) = 1` (meaning :math:`a` and :math:`b` must
    be coprime) on the numerators and denominators of the fractions in
    :math:`F_n`, combined with :math:`b \\leq n`, means that for each
    :math:`b \\leq n` it contains exactly :math:`\\phi(b)`` fractions of the
    form :math:`\\frac{a}{b}` where :math:`(a, b) = 1`.

    This means that the length :math:`LF(n)` of :math:`F_n` is given by:

    .. math::

       LF(n) = 1 + \\phi(1) + \\phi(2) + \\cdots + \\phi(n) = 1 + \\sum_{k = 1}^n \\phi(k)

    where :math:`\\phi(k)` is `Euler's totient function <https://en.wikipedia.org/wiki/Euler%27s_totient_function>`_.

    The first five Farey sequences are:

    .. math::

       \\begin{align}
       F_1 &= \\left( \\frac{0}{1}, \\frac{1}{1} \\right) \\\\
       F_2 &= \\left( \\frac{0}{1}, \\frac{1}{2}, \\frac{1}{1} \\right) \\\\
       F_3 &= \\left( \\frac{0}{1}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{1}{1} \\right) \\\\
       F_4 &= \\left( \\frac{0}{1}, \\frac{1}{4}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{3}{4}, \\frac{1}{1} \\right) \\\\
       F_5 &= \\left( \\frac{0}{1}, \\frac{1}{5}, \\frac{1}{4}, \\frac{1}{3}, \\frac{2}{5}, \\frac{1}{2}, \\frac{3}{5}, \\frac{2}{3}, \\frac{3}{4}, \\frac{4}{5}, \\frac{1}{1} \\right)
       \\end{align}

    Farey sequences have quite interesting properties and relations, as
    described `here <https://en.wikipedia.org/wiki/Farey_sequence>`_.

    Parameters
    ----------
    n : int:
        The order of the Farey sequence.

    Yields
    ------
    ContinuedFraction
        ``ContinuedFraction`` instances representing the elements of the Farey
        sequence of order :math:`n`, generated in ascending order of magnitude.

    Examples
    --------
    >>> list(farey_sequence(1))
    [ContinuedFraction(0, 1), ContinuedFraction(1, 1)]

    >>> list(farey_sequence(2))
    [ContinuedFraction(0, 1), ContinuedFraction(1, 2), ContinuedFraction(1, 1)]

    >>> list(farey_sequence(3))
    [ContinuedFraction(0, 1), ContinuedFraction(1, 3), ContinuedFraction(1, 2), ContinuedFraction(2, 3), ContinuedFraction(1, 1)]

    >>> list(farey_sequence(5))
    [ContinuedFraction(0, 1), ContinuedFraction(1, 5), ContinuedFraction(1, 4), ContinuedFraction(1, 3), ContinuedFraction(2, 5), ContinuedFraction(1, 2), ContinuedFraction(3, 5), ContinuedFraction(2, 3), ContinuedFraction(3, 4), ContinuedFraction(4, 5), ContinuedFraction(1, 1)]
    """
    yield ContinuedFraction(0, 1)

    yield from sorted(
        starmap(
            ContinuedFraction,
            starmap(lambda *x: tuple(reversed(x)), coprime_pairs(n))
        )
    )


if __name__ == "__main__":      # pragma: no cover
    # Doctest the module from the project root using
    #
    #     python -m doctest -v src/continuedfractions/utils.py
    #
    import doctest
    doctest.testmod()
