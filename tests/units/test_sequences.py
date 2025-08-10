# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pytest
import sympy

# -- Internal libraries --
from continuedfractions.continuedfraction import ContinuedFraction
from continuedfractions.utils import NamedCallableProxy
from continuedfractions.sequences import (
    _coprime_integers,
    coprime_pairs,
    FareyFraction,
    farey_sequence,
    KSRMTree,
)


class Test_CoprimeIntegers:

    @pytest.mark.parametrize(
        "n",
        [
            ("not an integer",),
            (0,),
            (-1,),
            (0.1,),
        ]
    )
    def test__coprime_integers__invalid_args__raises_value_error(self, n):
        with pytest.raises(ValueError):
            list(_coprime_integers(n))

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
    def test__coprime_integers__n_in_range_1_to_10(self, n, expected_coprime_integers):
        expected = expected_coprime_integers

        received = tuple(_coprime_integers(n))

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
        ]
    )
    def test__coprime_integers__verify_against_totient_value(self, n, expected_totient_value):
        expected = expected_totient_value

        received = tuple(_coprime_integers(n))

        assert len(received) == expected


class TestKSRMTree:

    def test_KSRMTree__creation_and_initialisation(self):
        tree = KSRMTree()

        assert tree.roots == ((2, 1), (3, 1))

        assert tree.branches[0].name == "KSRM tree branch #1: (x, y) |--> (2x - y, x)"
        assert tree.branches[1].name == "KSRM tree branch #2: (x, y) |--> (2x + y, x)"
        assert tree.branches[-1].name == "KSRM tree branch #3: (x, y) |--> (x + 2y, y)"

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
                ((4, 1), None, 1, NamedCallableProxy(lambda x, y: (x + 2 * y, y))),
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
        expected_backtracked_target_node = expected[0]
        expected_backtracked_target_node_gen_branch = expected[1]
        expected_backtracked_target_node_index = expected[2]
        expected_backtracked_target_node_succ_branch = expected[3]

        received = KSRMTree()._backtrack(n, visited)
        received_backtracked_target_node = received[0]
        received_backtracked_target_node_gen_branch = received[1]
        received_backtracked_target_node_index = received[2]
        received_backtracked_target_node_succ_branch = received[3]


        assert expected_backtracked_target_node == received_backtracked_target_node
        if expected_backtracked_target_node_gen_branch:
            assert expected_backtracked_target_node_gen_branch.name == received_backtracked_target_node_gen_branch.name
        assert expected_backtracked_target_node_index == received_backtracked_target_node_index
        if expected_backtracked_target_node_succ_branch:
            assert expected_backtracked_target_node_succ_branch.name == received_backtracked_target_node_succ_branch.name

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
            tuple(coprime_pairs(n))

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

        received = tuple(coprime_pairs(n))

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
        assert len(tuple(coprime_pairs(n))) == sum(map(sympy.totient, range(1, n + 1)))


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
            tuple(farey_sequence(n))

    @pytest.mark.parametrize(
        """n,
           expected_sequence""",
        [
            # Case #1
            (
                1,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 1),
                ]
            ),
            # Case #2
            (
                2,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 2),
                    FareyFraction(1, 1),
                ],
            ),
            # Case #3
            (
                3,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 3),
                    FareyFraction(1, 2),
                    FareyFraction(2, 3),
                    FareyFraction(1, 1),
                ],
            ),
            # Case #4
            (
                4,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 4),
                    FareyFraction(1, 3),
                    FareyFraction(1, 2),
                    FareyFraction(2, 3),
                    FareyFraction(3, 4),
                    FareyFraction(1, 1),
                ],
            ),
            # Case #5
            (
                5,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 5),
                    FareyFraction(1, 4),
                    FareyFraction(1, 3),
                    FareyFraction(2, 5),
                    FareyFraction(1, 2),
                    FareyFraction(3, 5),
                    FareyFraction(2, 3),
                    FareyFraction(3, 4),
                    FareyFraction(4, 5),
                    FareyFraction(1, 1),
                ],
            ),
            # Case #6
            (
                10,
                [
                    FareyFraction(0, 1),
                    FareyFraction(1, 10),
                    FareyFraction(1, 9),
                    FareyFraction(1, 8),
                    FareyFraction(1, 7),
                    FareyFraction(1, 6),
                    FareyFraction(1, 5),
                    FareyFraction(2, 9),
                    FareyFraction(1, 4),
                    FareyFraction(2, 7),
                    FareyFraction(3, 10),
                    FareyFraction(1, 3),
                    FareyFraction(3, 8),
                    FareyFraction(2, 5),
                    FareyFraction(3, 7),
                    FareyFraction(4, 9),
                    FareyFraction(1, 2),
                    FareyFraction(5, 9),
                    FareyFraction(4, 7),
                    FareyFraction(3, 5),
                    FareyFraction(5, 8),
                    FareyFraction(2, 3),
                    FareyFraction(7, 10),
                    FareyFraction(5, 7),
                    FareyFraction(3, 4),
                    FareyFraction(7, 9),
                    FareyFraction(4, 5),
                    FareyFraction(5, 6),
                    FareyFraction(6, 7),
                    FareyFraction(7, 8),
                    FareyFraction(8, 9),
                    FareyFraction(9, 10),
                    FareyFraction(1, 1),
                ],
            ),
        ],
    )
    def test_farey_sequence(self, n, expected_sequence):
        expected = tuple(expected_sequence)

        received = tuple(farey_sequence(n))

        assert received == expected
