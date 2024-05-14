# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pytest
import sympy

# -- Internal libraries --
from continuedfractions.continuedfraction import ContinuedFraction
from continuedfractions.utils import NamedCallableProxy
from continuedfractions.sequences import (
    coprime_integers,
    coprime_pairs,
    farey_sequence,
    KSRMTree,
)


class TestCoprimeIntegers:

    @pytest.mark.parametrize(
        "n, start, stop",
        [
            ("not an integer", 1, None),
            (0, 1, 2),
            (-1, 1, 2),
            (0.1, 1, 2),
            (3, 0, 2),
            (3, 3, 2),
        ]
    )
    def test_coprime_integers__invalid_args__raises_value_error(self, n, start, stop):
        with pytest.raises(ValueError):
            coprime_integers(n, start=start, stop=stop)

    @pytest.mark.parametrize(
        "n, expected_coprime_integers",
        [
            (1, (1,)),
            (2, (1,)),
            (3, (2, 1)),
            (4, (3, 1)),
            (5, (4, 3, 2, 1)),
            (6, (5, 1)),
            (7, (6, 5, 4, 3, 2, 1)),
            (8, (7, 5, 3, 1)),
            (9, (8, 7, 5, 4, 2, 1)),
            (10, (9, 7, 3, 1)),
        ]
    )
    def test_coprime_integers__default_start_and_stop_values(self, n, expected_coprime_integers):
        expected = expected_coprime_integers

        received = coprime_integers(n)

        assert received == expected

    @pytest.mark.parametrize(
        "n, start, stop, expected_coprime_integers",
        [
            (1, 1, None, (1,)),
            (2, 1, None, (1,)),
            (2, 1, 2, (1,)),
            (3, 1, None, (2, 1)),
            (3, 2, None, (2,)),
            (3, 1, 3, (2, 1)),
            (3, 2, 3, (2,)),
            (4, 1, None, (3, 1)),
            (4, 2, None, (3,)),
            (4, 3, None, (3,)),
            (4, 1, 4, (3, 1)),
            (4, 2, 4, (3,)),
            (4, 2, 3, (3,)),
            (5, 1, None, (4, 3, 2, 1)),
            (5, 2, None, (4, 3, 2)),
            (5, 3, None, (4, 3)),
            (5, 4, None, (4,)),
            (5, 1, 5, (4, 3, 2, 1)),
            (5, 2, 5, (4, 3, 2)),
            (5, 2, 4, (4, 3, 2)),
            (5, 2, 3, (3, 2)),
            (6, 1, None, (5, 1)),
            (6, 2, None, (5,)),
            (6, 3, None, (5,)),
            (6, 4, None, (5,)),
            (6, 5, None, (5,)),
            (6, 1, 6, (5, 1)),
            (6, 2, 5, (5,)),
            (6, 2, 4, ()),
            (6, 2, 3, ()),
            (7, 1, None, (6, 5, 4, 3, 2, 1)),
            (7, 2, None, (6, 5, 4, 3, 2)),
            (7, 3, None, (6, 5, 4, 3)),
            (7, 4, None, (6, 5, 4)),
            (7, 5, None, (6, 5)),
            (7, 6, None, (6,)),
            (7, 1, 7, (6, 5, 4, 3, 2, 1)),
            (7, 2, 7, (6, 5, 4, 3, 2)),
            (7, 2, 6, (6, 5, 4, 3, 2)),
            (7, 2, 5, (5, 4, 3, 2)),
            (7, 2, 4, (4, 3, 2)),
            (7, 2, 3, (3, 2)),
            (8, 1, None, (7, 5, 3, 1)),
            (8, 2, None, (7, 5, 3)),
            (8, 3, None, (7, 5, 3)),
            (8, 4, None, (7, 5)),
            (8, 5, None, (7, 5)),
            (8, 6, None, (7,)),
            (8, 7, None, (7,)),
            (8, 1, 8, (7, 5, 3, 1)),
            (8, 2, 8, (7, 5, 3)),
            (8, 2, 7, (7, 5, 3)),
            (8, 2, 6, (5, 3)),
            (8, 2, 5, (5, 3)),
            (8, 2, 4, (3,)),
            (8, 2, 3, (3,)),
            (9, 1, None, (8, 7, 5, 4, 2, 1)),
            (9, 2, None, (8, 7, 5, 4, 2)),
            (9, 3, None, (8, 7, 5, 4)),
            (9, 4, None, (8, 7, 5, 4)),
            (9, 5, None, (8, 7, 5)),
            (9, 6, None, (8, 7)),
            (9, 7, None, (8, 7)),
            (9, 8, None, (8,)),
            (9, 1, 9, (8, 7, 5, 4, 2, 1)),
            (9, 2, 9, (8, 7, 5, 4, 2)),
            (9, 2, 8, (8, 7, 5, 4, 2)),
            (9, 2, 7, (7, 5, 4, 2)),
            (9, 2, 6, (5, 4, 2)),
            (9, 2, 5, (5, 4, 2)),
            (9, 2, 4, (4, 2)),
            (9, 2, 3, (2,)),
            (10, 1, None, (9, 7, 3, 1)),
            (10, 2, None, (9, 7, 3)),
            (10, 3, None, (9, 7, 3)),
            (10, 4, None, (9, 7)),
            (10, 5, None, (9, 7)),
            (10, 6, None, (9, 7)),
            (10, 7, None, (9, 7)),
            (10, 8, None, (9,)),
            (10, 9, None, (9,)),
            (10, 1, 10, (9, 7, 3, 1)),
            (10, 2, 9, (9, 7, 3)),
            (10, 2, 8, (7, 3)),
            (10, 2, 7, (7, 3)),
            (10, 2, 6, (3,)),
            (10, 2, 5, (3,)),
            (10, 2, 4, (3,)),
            (10, 2, 3, (3,)),
        ]
    )
    def test_coprime_integers__custom_start_and_stop_values(self, n, start, stop, expected_coprime_integers):
        expected = expected_coprime_integers

        received = coprime_integers(n, start=start, stop=stop)

        assert received == expected

    @pytest.mark.parametrize(
        "n, expected_totient_value",
        [
            (1, sympy.totient(1)),
            (2, sympy.totient(2)),
            (3, sympy.totient(3)),
            (4, sympy.totient(4)),
            (5, sympy.totient(5)),
            (6, sympy.totient(6)),
            (7, sympy.totient(7)),
            (8, sympy.totient(8)),
            (9, sympy.totient(9)),
            (10, sympy.totient(10)),
            (11, sympy.totient(11)),
            (99, sympy.totient(99)),
            (100, sympy.totient(100)),
            (101, sympy.totient(101)),
            (999, sympy.totient(999)),
            (1000, sympy.totient(1000)),
            (1001, sympy.totient(1001)),
            (9999, sympy.totient(9999)),
            (10000, sympy.totient(10000)),
            (10001, sympy.totient(10001)),
            (99999, sympy.totient(99999)),
            (100000, sympy.totient(100000)),
            (100001, sympy.totient(100001)),
            (999999, sympy.totient(999999)),
            (1000000, sympy.totient(1000000)),
            (1000001, sympy.totient(1000001)),
            (9999999, sympy.totient(9999999)),
            (10000000, sympy.totient(10000000)),
            (10000001, sympy.totient(10000001)),
        ]
    )
    def test_coprime_integers__verify_against_totient_value(self, n, expected_totient_value):
        expected = expected_totient_value

        received = coprime_integers(n)

        assert len(received) == expected


class TestKSRMTree:

    def test_KSRMTree__creation_and_initialisation(self):
        tree = KSRMTree()

        assert tree.roots == ((2, 1), (3, 1))

        assert tree.branches == (
            NamedCallableProxy(lambda x, y: (2 * x - y, x), name="KSRM tree branch #1: (x, y) |--> (2x - y, x)"),
            NamedCallableProxy(lambda x, y: (2 * x + y, x), name="KSRM tree branch #2: (x, y) |--> (2x + y, x)"),
            NamedCallableProxy(lambda x, y: (x + 2 * y, y), name="KSRM tree branch #3: (x, y) |--> (x + 2y, y)")
        )

    @pytest.mark.parametrize(
        """n,
           visited,
           expected_backtracked_tuple""",
        [
            # Case #1
            (
                3,
                [
                    ((2, 1), None),
                ],
                ((2, 1), None, 0, None),
            ),
            # Case #2
            (
                5,
                [
                    ((2, 1), None),
                    ((4, 1), NamedCallableProxy(lambda x, y: (x + 2 * y, y))),
                    ((6, 1), NamedCallableProxy(lambda x, y: (x + 2 * y, y)))
                ],
                ((2, 1), None, 0, NamedCallableProxy(lambda x, y: (x + 2 * y, y))),
            ),
            # Case #3
            (
                8,
                [
                    ((2, 1), None),
                    ((3, 2), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((8, 3), NamedCallableProxy(lambda x, y: (2 * x + y, x))),
                    ((19, 8), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                ],
                ((3, 2), NamedCallableProxy(lambda x, y: (2 * x - y, x)), 1, NamedCallableProxy(lambda x, y: (2 * x + y, x))),
            ),
            # Case #4
            (
                10,
                [
                    ((2, 1), None),
                    ((3, 2), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((4, 3), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((5, 4), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((6, 5), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((7, 6), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((8, 7), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((9, 8), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((10, 9), NamedCallableProxy(lambda x, y: (2 * x - y, x))),
                    ((28, 9), NamedCallableProxy(lambda x, y: (x + 2 * y, y))),
                ],
                ((9, 8), NamedCallableProxy(lambda x, y: (2 * x - y, x)), 7, NamedCallableProxy(lambda x, y: (2 * x - y, x))),
            )
        ],
    )
    def test_KSRMTree__backtrack(self, n, visited, expected_backtracked_tuple):
        expected = expected_backtracked_tuple

        received = KSRMTree()._backtrack(n, visited)

        assert received == expected

    @pytest.mark.parametrize(
        """n,
           root
        """,
        [
            ("not an integer", (2, 1)),
            (1, (2, 1)),
            ("not an integer", (3, 1)),
            (1, (3, 1))
        ]
    )
    def test_KSRMTree_search_root__invalid_args__raises_value_error(self, n, root):
        with pytest.raises(ValueError):
            list(KSRMTree().search_root(n, root))

    @pytest.mark.parametrize(
        """n,
           root,
           expected_pairs""",
        [
            # Case #1
            (
                2,
                (2, 1),
                [
                    (2, 1),
                ],
            ),
            # Case #2
            (
                3,
                (2, 1),
                [
                    (2, 1), (3, 2),
                ],
            ),
            # Case #3
            (
                4,
                (2, 1),
                [
                    (2, 1), (3, 2), (4, 3), (4, 1),
                ],
            ),
            # Case #4
            (
                5,
                (2, 1),
                [
                    (2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1),
                ],
            ),
            # Case #5
            (
                10,
                (2, 1),
                [
                    (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7),
                    (9, 8), (10, 9), (10, 3), (8, 3), (7, 2), (5, 2), (8, 5),
                    (9, 2), (4, 1), (7, 4), (10, 7), (9, 4), (6, 1), (8, 1),
                    (10, 1),
                ],
            ),
            # Case #6
            (
                2,
                (3, 1),
                [],
            ),
            # Case #7
            (
                3,
                (3, 1),
                [
                    (3, 1),
                ],
            ),
            # Case #8
            (
                4,
                (3, 1),
                [
                    (3, 1),
                ],
            ),
            # Case #9
            (
                5,
                (3, 1),
                [
                    (3, 1), (5, 3), (5, 1),
                ],
            ),
            # Case #10
            (
                10,
                (3, 1),
                [
                    (3, 1), (5, 3), (7, 5), (9, 7), (7, 3), (5, 1), (9, 5),
                    (7, 1), (9, 1),
                ],
            ),

        ],
    )
    def test_KSRMTree__search_root(self, n, root, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search_root(n, root))

        assert received == expected

    @pytest.mark.parametrize(
        "n",
        [
            ("not an integer",),
            (0,),
            (-1, ),
            (0.1,)
        ]
    )
    def test_KSRMTree_search__invalid_args__raises_value_error(self, n):
        with pytest.raises(ValueError):
            list(KSRMTree().search(n))

    @pytest.mark.parametrize(
        """n,
           expected_pairs""",
        [
            # Case #1
            (
                1,
                [
                    (1, 1),
                ]
            ),
            # Case #2
            (
                2,
                [
                    (1, 1), (2, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    (1, 1), (2, 1), (3, 2), (3, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    (1, 1), (2, 1), (3, 2), (3, 1), (4, 3), (4, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (4, 1), (3, 1),
                    (5, 4), (5, 3), (5, 2), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5),
                    (7, 6), (8, 7), (9, 8), (8, 3), (7, 2), (5, 2),
                    (8, 5), (9, 2), (4, 1), (7, 4), (9, 4), (6, 1),
                    (8, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3),
                    (5, 1), (9, 5), (7, 1), (9, 1), (10, 9), (10, 7),
                    (10, 3), (10, 1),
                ],
            ),
        ],
    )
    def test_KSRMTree_search(self, n, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search(n))

        assert received == expected


class TestCoprimePairs:

    @pytest.mark.parametrize(
        "n",
        [
            ("not an integer",),
            (0,),
            (-1, ),
            (0.1,)
        ]
    )
    def test_coprime_pairs__invalid_args__raises_value_error(self, n):
        with pytest.raises(ValueError):
            coprime_pairs(n)

    @pytest.mark.parametrize(
        """n,
           expected_pairs""",
        [
            # Case #1
            (
                1,
                [
                    (1, 1),
                ]
            ),
            # Case #2
            (
                2,
                [
                    (1, 1), (2, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    (1, 1), (2, 1), (3, 2), (3, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    (1, 1), (2, 1), (3, 2), (3, 1), (4, 3), (4, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (1, 1), (2, 1), (3, 2), (3, 1), (4, 3), (4, 1),
                    (5, 4), (5, 3), (5, 2), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5),
                    (7, 6), (8, 7), (8, 3), (7, 2), (5, 2), (8, 5),
                    (4, 1), (7, 4), (6, 1), (8, 1), (3, 1), (5, 3),
                    (7, 5), (7, 3), (5, 1), (7, 1), (9, 8), (9, 7),
                    (9, 5), (9, 4), (9, 2), (9, 1), (10, 9), (10, 7),
                    (10, 3), (10, 1),
                ],
            ),
        ],
    )
    def test_coprime_pairs(self, n, expected_pairs):
        expected = tuple(expected_pairs)

        received = coprime_pairs(n)

        assert received == expected

    @pytest.mark.parametrize(
        "n",
        [
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            99,
            100,
            101,
            999,
            1000,
            1001,
        ]
    )
    def test_coprime_pairs__verify_against_summatory_totient_value(self, n):
        assert len(coprime_pairs(n)) == sum(map(sympy.totient, range(1, n + 1)))


class TestFareySequence:

    @pytest.mark.parametrize(
        "n",
        [
            ("not an integer",),
            (0,),
            (-1, ),
            (0.1,)
        ]
    )
    def test_farey_sequence__invalid_args__raises_value_error(self, n):
        with pytest.raises(ValueError):
            farey_sequence(n)

    @pytest.mark.parametrize(
        """n,
           expected_sequence""",
        [
            # Case #1
            (
                1,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 1),
                ]
            ),
            # Case #2
            (
                2,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 2),
                    ContinuedFraction(1, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 3),
                    ContinuedFraction(1, 2), ContinuedFraction(2, 3),
                    ContinuedFraction(1, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 4),
                    ContinuedFraction(1, 3), ContinuedFraction(1, 2),
                    ContinuedFraction(2, 3), ContinuedFraction(3, 4),
                    ContinuedFraction(1, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 5),
                    ContinuedFraction(1, 4), ContinuedFraction(1, 3),
                    ContinuedFraction(2, 5), ContinuedFraction(1, 2),
                    ContinuedFraction(3, 5), ContinuedFraction(2, 3),
                    ContinuedFraction(3, 4), ContinuedFraction(4, 5),
                    ContinuedFraction(1, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    ContinuedFraction(0, 1), ContinuedFraction(1, 10),
                    ContinuedFraction(1, 9), ContinuedFraction(1, 8),
                    ContinuedFraction(1, 7), ContinuedFraction(1, 6),
                    ContinuedFraction(1, 5), ContinuedFraction(2, 9),
                    ContinuedFraction(1, 4), ContinuedFraction(2, 7),
                    ContinuedFraction(3, 10), ContinuedFraction(1, 3),
                    ContinuedFraction(3, 8), ContinuedFraction(2, 5),
                    ContinuedFraction(3, 7), ContinuedFraction(4, 9),
                    ContinuedFraction(1, 2), ContinuedFraction(5, 9),
                    ContinuedFraction(4, 7), ContinuedFraction(3, 5),
                    ContinuedFraction(5, 8), ContinuedFraction(2, 3),
                    ContinuedFraction(7, 10), ContinuedFraction(5, 7),
                    ContinuedFraction(3, 4), ContinuedFraction(7, 9),
                    ContinuedFraction(4, 5), ContinuedFraction(5, 6),
                    ContinuedFraction(6, 7), ContinuedFraction(7, 8),
                    ContinuedFraction(8, 9), ContinuedFraction(9, 10),
                    ContinuedFraction(1, 1),
                ],
            ),
        ],
    )
    def test_farey_sequence(self, n, expected_sequence):
        expected = tuple(expected_sequence)

        received = farey_sequence(n)

        assert received == expected
