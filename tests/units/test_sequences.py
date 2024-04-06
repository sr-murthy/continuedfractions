# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pytest
import sympy

# -- Internal libraries --
from continuedfractions.continuedfraction import ContinuedFraction
from continuedfractions.utils import NamedCallableProxy
from continuedfractions.sequences import (
    coprime_pairs,
    farey_sequence,
    KSRMTree,
)


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
    def test_KSRMTree__search_root__non_strict_mode(self, n, root, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search_root(n, root))

        assert received == expected

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
                    (3, 2),
                ],
            ),
            # Case #3
            (
                4,
                (2, 1),
                [
                    (4, 3), (4, 1),
                ],
            ),
            # Case #4
            (
                5,
                (2, 1),
                [
                    (5, 4), (5, 2),
                ],
            ),
            # Case #5
            (
                10,
                (2, 1),
                [
                    (10, 9), (10, 3), (10, 7), (10, 1),
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
                [],
            ),
            # Case #9
            (
                5,
                (3, 1),
                [
                    (5, 3), (5, 1),
                ],
            ),
            # Case #10
            (
                10,
                (3, 1),
                [],
            ),

        ],
    )
    def test_KSRMTree__search_root__strict_mode(self, n, root, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search_root(n, root, strict=True))

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
                    (1, 1), (2, 1), (3, 2), (4, 3), (4, 1), (3, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1),
                    (3, 1), (5, 3), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6),
                    (8, 7), (9, 8), (10, 9), (10, 3), (8, 3), (7, 2), (5, 2),
                    (8, 5), (9, 2), (4, 1), (7, 4), (10, 7), (9, 4), (6, 1),
                    (8, 1), (10, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3),
                    (5, 1), (9, 5), (7, 1), (9, 1),
                ],
            ),
        ],
    )
    def test_KSRMTree_search__not_strict_mode(self, n, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search(n))

        assert received == expected

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
                    (2, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    (3, 2), (3, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    (4, 3), (4, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (5, 4), (5, 2), (5, 3), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (10, 9), (10, 3), (10, 7), (10, 1),
                ],
            ),
        ],
    )
    def test_KSRMTree_search__strict_mode(self, n, expected_pairs):
        expected = expected_pairs

        received = list(KSRMTree().search(n, strict=True))

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
                    (1, 1), (2, 1), (3, 2), (4, 3), (4, 1), (3, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (5, 2), (4, 1),
                    (3, 1), (5, 3), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (1, 1), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6),
                    (8, 7), (9, 8), (10, 9), (10, 3), (8, 3), (7, 2), (5, 2),
                    (8, 5), (9, 2), (4, 1), (7, 4), (10, 7), (9, 4), (6, 1),
                    (8, 1), (10, 1), (3, 1), (5, 3), (7, 5), (9, 7), (7, 3),
                    (5, 1), (9, 5), (7, 1), (9, 1),
                ],
            ),
        ],
    )
    def test_coprime_pairs__non_strict_mode(self, n, expected_pairs):
        expected = tuple(expected_pairs)

        received = coprime_pairs(n)

        assert received == expected

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
                    (2, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    (3, 2), (3, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    (4, 3), (4, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    (5, 4), (5, 2), (5, 3), (5, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    (10, 9), (10, 3), (10, 7), (10, 1),
                ],
            ),
        ],
    )
    def test_coprime_pairs__strict_mode(self, n, expected_pairs):
        expected = tuple(expected_pairs)

        received = coprime_pairs(n, strict=True)

        assert received == expected

    @pytest.mark.parametrize(
        "n",
        [
            1,
            2,
            3,
            4,
            10,
            100,
            1000,
        ]
    )
    def test_coprime_pairs__non_strict_mode__verify_against_summatory_totient_value(self, n):
        assert len(coprime_pairs(n)) == sum(map(sympy.totient, range(1, n + 1)))

    @pytest.mark.parametrize(
        "n",
        [
            1,
            2,
            3,
            4,
            10,
            100,
            1000,
        ]
    )
    def test_coprime_pairs__strict_mode__verify_against_totient_value(self, n):
        assert len(coprime_pairs(n, strict=True)) == sympy.totient(n)


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
