# -- IMPORTS --

# -- Standard libraries --

import decimal

# Set the :py:mod:`decimal` context for the test computations in this module
# using default precision of 28 digits, including the integer part, and 
# set the :py:class:`decimal.Inexact` trap for computations to signal
# loss of precision due to rounding - this would be useful in debugging
context = decimal.Context(prec=28, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
context.traps[decimal.Inexact] = True
decimal.setcontext(context)

from decimal import Decimal
from fractions import Fraction
from types import MappingProxyType

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.lib import convergent
from continuedfractions.continuedfraction import ContinuedFraction


class TestContinuedFraction:

    @pytest.mark.parametrize(
        """valid_inputs,
           expected_fraction_obj,
           expected_elements,
           expected_order,
           expected_khinchin_mean,
           expected_convergents,
           expected_ref_right_order2_mediant,
           expected_ref_left_order2_mediant,
           expected_ref_simple_mediant,
           expected_float_value,
           expected_decimal_value""",
        [
            # Case #1
            (
                (3, 2,),
                Fraction(3, 2),
                (1, 2,),
                1,
                Decimal('2'),
                (
                    (0, ContinuedFraction(1, 1)),
                    (1, ContinuedFraction(3, 2))
                ),
                ContinuedFraction(5, 4),
                ContinuedFraction(7, 5),
                ContinuedFraction(4, 3),
                3 / 2,
                Decimal('1.5')
            ),
            # Case #2
            (
                ('1.5',),
                Fraction(3, 2),
                (1, 2,),
                1,
                Decimal('2'),
                (
                    (0, ContinuedFraction(1, 1)),
                    (1, ContinuedFraction(3, 2))
                ),
                ContinuedFraction(5, 4),
                ContinuedFraction(7, 5),
                ContinuedFraction(4, 3),
                3 / 2,
                Decimal('1.5')
            ),
            # Case #3
            (
                ('-5000',),
                Fraction(-5000),
                (-5000,),
                0,
                None,
                (
                    (0, ContinuedFraction(-5000, 1)),
                ),
                ContinuedFraction(-1666, 1),
                ContinuedFraction(-3333, 1),
                ContinuedFraction(-4999, 2),
                -5000.0,
                Decimal('-5000')
            ),
            # Case #4
            (
                ('3.245',),
                Fraction(649, 200),
                (3, 4, 12, 4),
                3,
                Decimal('5.76899828122963409526846589869819581508636474609375'),
                (
                    (0, ContinuedFraction(3, 1)),
                    (1, ContinuedFraction(13, 4)),
                    (2, ContinuedFraction(159, 49)),
                    (3, ContinuedFraction(649, 200))
                ),
                ContinuedFraction(651, 202),
                ContinuedFraction(1299, 401),
                ContinuedFraction(650, 201),
                3.245,
                Decimal('3.245')

            ),
            # Case #5
            (
                ('-649/200',),
                Fraction(-649, 200),
                (-4, 1, 3, 12, 4),
                4,
                Decimal('3.464101615137754830442418096936307847499847412109375'),
                (
                    (0, ContinuedFraction(-4, 1)),
                    (1, ContinuedFraction(-3, 1)),
                    (2, ContinuedFraction(-13, 4)),
                    (3, ContinuedFraction(-159, 49)),
                    (4, ContinuedFraction(-649, 200))
                ),
                ContinuedFraction(-647, 202),
                ContinuedFraction(-1297, 401),
                ContinuedFraction(-216, 67),
                -3.245,
                Decimal('-3.245')
            ),
            # Case #6
            (
                (-649, -200),
                Fraction(649, 200),
                (3, 4, 12, 4),
                3,
                Decimal('5.76899828122963409526846589869819581508636474609375'),
                (
                    (0, ContinuedFraction(3, 1)),
                    (1, ContinuedFraction(13, 4)),
                    (2, ContinuedFraction(159, 49)),
                    (3, ContinuedFraction(649, 200))
                ),
                ContinuedFraction(651, 202),
                ContinuedFraction(1299, 401),
                ContinuedFraction(650, 201),
                3.245,
                Decimal('3.245')
            ),
            # Case #7
            (
                ('0.3333',),
                Fraction(3333, 10000),
                (0, 3, 3333),
                2,
                Decimal('99.9949998749937520869934814982116222381591796875'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 3)),
                    (2, ContinuedFraction(3333, 10000))
                ),
                ContinuedFraction(3335, 10002),
                ContinuedFraction(1, 3),
                ContinuedFraction(3334, 10001),
                0.3333,
                Decimal('0.3333')
            ),
            # Case #8
            (
                ('-0.3333',),
                Fraction(-3333, 10000),
                (-1, 1, 2, 3333),
                3,
                Decimal('18.820093199354911206455653882585465908050537109375'),
                (
                    (0, ContinuedFraction(-1, 1)),
                    (1, ContinuedFraction(0, 1)),
                    (2, ContinuedFraction(-1, 3)),
                    (3, ContinuedFraction(-3333, 10000))
                ),
                ContinuedFraction(-3331, 10002),
                ContinuedFraction(-6665, 20001),
                ContinuedFraction(-3332, 10001),
                -0.3333,
                Decimal('-0.3333')
            ),
            # Case #9
            (
                ('-5.25',),
                Fraction(-21, 4),
                (-6, 1, 3),
                2,
                Decimal('1.7320508075688774152212090484681539237499237060546875'),
                (
                    (0, ContinuedFraction(-6, 1)),
                    (1, ContinuedFraction(-5, 1)),
                    (2, ContinuedFraction(-21, 4))
                ),
                ContinuedFraction(-19, 6),
                ContinuedFraction(-41, 9),
                ContinuedFraction(-4, 1),
                -5.25,
                Decimal('-5.25')
            ),
            # Case #10
            (
                ('123456789',),
                Fraction(123456789, 1),
                (123456789,),
                0,
                None,
                (
                    (0, ContinuedFraction(123456789, 1)),
                ),
                ContinuedFraction(123456791, 3),
                ContinuedFraction(246913579, 3),
                ContinuedFraction(61728395, 1),
                123456789.0,
                Decimal('123456789')
            ),
            # Case #11
            (
                ('0.3',),
                Fraction(3, 10),
                (0, 3, 3),
                2,
                Decimal('3.000000000000000444089209850062616169452667236328125'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 3)),
                    (2, ContinuedFraction(3, 10))   
                ),
                ContinuedFraction(5, 12),
                ContinuedFraction(1, 3),
                ContinuedFraction(4, 11),
                0.3,
                Decimal('0.3')
            ),
            # Case #12
            (
                (1, 10,),
                Fraction(1, 10),
                (0, 10),
                1,
                Decimal('10'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 10))
                ),
                ContinuedFraction(1, 4),
                ContinuedFraction(1, 7),
                ContinuedFraction(2, 11),
                0.1,
                Decimal('0.1')
            ),
            # Case #13
            (
                ('-3.245',),
                Fraction(-649, 200),
                (-4, 1, 3, 12, 4),
                4,
                Decimal('3.464101615137754830442418096936307847499847412109375'),
                (
                    (0, ContinuedFraction(-4, 1)),
                    (1, ContinuedFraction(-3, 1)),
                    (2, ContinuedFraction(-13, 4)),
                    (3, ContinuedFraction(-159, 49)),
                    (4, ContinuedFraction(-649, 200))
                ),
                ContinuedFraction(-647, 202),
                ContinuedFraction(-1297, 401),
                ContinuedFraction(-216, 67),
                -3.245,
                Decimal('-3.245')
            ),
            # Case #14
            (
                (123456789,),
                Fraction(123456789, 1),
                (123456789,),
                0,
                None,
                (
                    (0, ContinuedFraction(123456789, 1)),
                ),
                ContinuedFraction(123456791, 3),
                ContinuedFraction(246913579, 3),                
                ContinuedFraction(61728395, 1),
                123456789.0,
                Decimal('123456789')
            ),
            # Case #15
            (
                (1.5,),
                Fraction(3, 2),
                (1, 2,),
                1,
                Decimal('2'),
                (
                    (0, ContinuedFraction(1, 1)),
                    (1, ContinuedFraction(3, 2))
                ),
                ContinuedFraction(5, 4),
                ContinuedFraction(7, 5),
                ContinuedFraction(4, 3),
                1.5,
                Decimal('1.5')
            ),
            # Case #16
            (
                (-3, Fraction(4, 5)),
                Fraction(-15, 4),
                (-4, 4),
                1,
                Decimal('4'),
                (
                    (0, ContinuedFraction(-4, 1)),
                    (1, ContinuedFraction(-15, 4))
                ),
                ContinuedFraction(-13, 6),
                ContinuedFraction(-29, 9),
                ContinuedFraction(-14, 5),
                -3.75,
                Decimal('-3.75')
            ),
            # Case #17
            (
                (Decimal('3.245'),),
                Fraction(649, 200),
                (3, 4, 12, 4),
                3,
                Decimal('5.76899828122963409526846589869819581508636474609375'),
                (
                    (0, ContinuedFraction(3, 1)),
                    (1, ContinuedFraction(13, 4)),
                    (2, ContinuedFraction(159, 49)),
                    (3, ContinuedFraction(649, 200))
                ),
                ContinuedFraction(651, 202),
                ContinuedFraction(1299, 401),               
                ContinuedFraction(650, 201),
                3.245,
                Decimal('3.245')
            ),
            # Case #18
            (
                (ContinuedFraction(1, 10),),
                Fraction(1, 10),
                (0, 10),
                1,
                Decimal('10'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 10))
                ),
                ContinuedFraction(1, 4),
                ContinuedFraction(1, 7),                
                ContinuedFraction(2, 11),
                0.1,
                Decimal('0.1')
            ),
            # Case #19
            (
                (ContinuedFraction(1, 10), 2,),
                Fraction(1, 20),
                (0, 20),
                1,
                Decimal('20'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 20))
                ),
                ContinuedFraction(3, 22),
                ContinuedFraction(3, 41),
                ContinuedFraction(2, 21),
                0.05,
                Decimal('0.05')
            ),
            # Case #20
            (
                (ContinuedFraction(1, 10), Fraction(2, 5),),
                Fraction(1, 4),
                (0, 4),
                1,
                Decimal('4'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 4))
                ),
                ContinuedFraction(1, 2),
                ContinuedFraction(1, 3),
                ContinuedFraction(2, 5),
                0.25,
                Decimal('0.25')
            ),
            # Case #21
            (
                (ContinuedFraction(649, 200), Fraction(415, 93),),
                Fraction(60357, 83000),
                (0, 1, 2, 1, 1, 1, 102, 1, 2, 1, 1, 1, 6),
                12,
                Decimal('1.9160240282353602214726606689509935677051544189453125'),
                (
                    (0, ContinuedFraction(0, 1)),
                    (1, ContinuedFraction(1, 1)),
                    (2, ContinuedFraction(2, 3)),
                    (3, ContinuedFraction(3, 4)),
                    (4, ContinuedFraction(5, 7)),
                    (5, ContinuedFraction(8, 11)),
                    (6, ContinuedFraction(821, 1129)),
                    (7, ContinuedFraction(829, 1140)),
                    (8, ContinuedFraction(2479, 3409)),
                    (9, ContinuedFraction(3308, 4549)),
                    (10, ContinuedFraction(5787, 7958)),
                    (11, ContinuedFraction(9095, 12507)),
                    (12, ContinuedFraction(60357, 83000))
                ),
                ContinuedFraction(60359, 83002),
                ContinuedFraction(120715, 166001),
                ContinuedFraction(60358, 83001),
                0.7271927710843373,
                Decimal('0.7271927710843373493975903614')
            ),
        ],
    )
    def test_ContinuedFraction__creation_and_initialisation__valid_inputs__object_correctly_created_and_initialised(
        self,
        valid_inputs,
        expected_fraction_obj,
        expected_elements,
        expected_order,
        expected_khinchin_mean,
        expected_convergents,
        expected_ref_right_order2_mediant,
        expected_ref_left_order2_mediant,
        expected_ref_simple_mediant,
        expected_float_value,
        expected_decimal_value
    ):
        expected = expected_fraction_obj

        # The received ``ContinuedFraction`` object
        received = ContinuedFraction(*valid_inputs)

        # Compare the received and expected objects AS ``fractions.Fraction``
        # objects
        assert received == expected

        # Compare the float values
        assert received.as_float() == expected_float_value

        # Compare the decimal values
        try:
            assert received.as_decimal() == expected_decimal_value
        except decimal.Inexact:
            pass

        # Compare the element sequences
        assert received.elements == expected_elements

        # Compare the orders
        assert received.order == expected_order

        # Compare the Khinchin means
        assert received.khinchin_mean == expected_khinchin_mean

        # Compare the convergents using the ``.convergent`` method
        assert not any(
            received.convergent(k) != expected_convergents[k][1]
            for k in range(received.order + 1)
        )

        # Compare the convergents using the ``.convergents`` property
        assert tuple(received.convergents) == expected_convergents

        # Compare the even-order convergents using the ``.even_order_convergents` property
        assert tuple(received.even_convergents) == tuple((k, expected_convergents[k][1]) for k in range(0, received.order + 1, 2))

        # Compare the order-order convergents using the ``.odd_order_convergents` property
        assert tuple(received.odd_convergents) == tuple((k, expected_convergents[k][1]) for k in range(1, received.order + 1, 2))

        # Compare the 2nd order right- and left-mediants, and also the simple
        # mediant, using a reference continued fraction of ``1/1``
        assert received.right_mediant(1, k=2) == expected_ref_right_order2_mediant
        assert received.left_mediant(1, k=2) == expected_ref_left_order2_mediant
        assert received.mediant(1) == expected_ref_simple_mediant

        expected_remainders = tuple(
            (k, ContinuedFraction.from_elements(*expected_elements[k:]))
            for k in reversed(range(received.order + 1))
        )
        # Compare the remainders using the ``.remainder`` method
        assert all(
            received.remainder(k) == expected_remainders[::-1][k][1]
            for k in reversed(range(received.order + 1))
        )

        # Compare the remainders using the ``.remainders`` property
        assert tuple(received.remainders) == expected_remainders

    @pytest.mark.parametrize(
        "invalid_elements",
        [
            (0, 0),
            (1, 0),
            (1, -1),
            (3, 0, 12, 4),
            (-3, -1, 12, 4),
            (3, 4, 0, 4),
            (-3, 4, -1, 4),
            (3, 4, 12, 0),
            (-3, 4, 12, -1),
            (3, 0, 0, 4),
            (-3, 0, 12, 0),
            (3, 4, 0, 0),
            (-3, 0, -1, 4),
            (3, 0, 12, -1),
            (-3, 4, 0, -1),
        ]
    )
    def test_ContinuedFraction__from_elements__invalid_elements__value_error_raised(self, invalid_elements):
        with pytest.raises(ValueError):
            ContinuedFraction.from_elements(*invalid_elements)

    @pytest.mark.parametrize(
        "elements, expected",
        [
            ((-2,), ContinuedFraction(-2, 1)),
            ((-2, 2,), ContinuedFraction(-3, 2)),
            ((-2, 1, 1,), ContinuedFraction(-3, 2)),
            ((-1,), ContinuedFraction(-1, 1)),
            ((-1, 2,), ContinuedFraction(-1, 2)),
            ((-1, 1, 1,), ContinuedFraction(-1, 2)),
            ((-0,), ContinuedFraction(0, 1)),
            ((0, 2,), ContinuedFraction(1, 2)),
            ((0, 1, 1,), ContinuedFraction(1, 2)),
            ((1, 2,), ContinuedFraction(3, 2)),
            ((1, 1, 1,), ContinuedFraction(3, 2))
        ]
    )
    def test_ContinuedFraction__from_elements__valid_elements__correct_fraction_returned(self, elements, expected):
            received = ContinuedFraction.from_elements(*elements)

            assert received == expected
            assert received.elements == expected.elements

    @pytest.mark.parametrize(
        "instance, invalid_elements",
        [
            (ContinuedFraction(1, 2), ()),
            (ContinuedFraction(1, 2), ("invalid", 1)),
            (ContinuedFraction(1, 2), (1, 2, 0)),
            (ContinuedFraction(1, 2), (1, 2, -1)),
        ],
    )
    def test_ContinuedFraction__extend__invalid_elements__value_error_raised(self, instance, invalid_elements):
        with pytest.raises(ValueError):
            instance.extend(*invalid_elements)

    @pytest.mark.parametrize(
        "instance, new_elements, expected_comparative_instance",
        [
            (ContinuedFraction(0, 1), (2,), ContinuedFraction(1, 2)),
            (ContinuedFraction(1, 1), (2,), ContinuedFraction(3, 2)),
            (ContinuedFraction(3, 2), (3,), ContinuedFraction(10, 7)),
            (ContinuedFraction(649, 200), (5, 2), ContinuedFraction(7457, 2298)),
            (ContinuedFraction(-415, 93), (2, 1, 5), ContinuedFraction(-7403, 1659))
        ]
    )
    def test_ContinuedFraction__extend__valid_elements__correctly_extended(self, instance, new_elements, expected_comparative_instance):
        original_id = id(instance)
        original_elements = instance.elements

        instance.extend(*new_elements)

        assert id(instance) == original_id
        assert instance == expected_comparative_instance
        assert hash(instance) == hash(expected_comparative_instance)
        assert instance == ContinuedFraction.from_elements(*original_elements, *new_elements)
        assert instance.order == expected_comparative_instance.order
        assert tuple(instance.convergents) == tuple(expected_comparative_instance.convergents)
        assert tuple(instance.remainders) == tuple(expected_comparative_instance.remainders)
        assert instance.khinchin_mean == expected_comparative_instance.khinchin_mean

    @pytest.mark.parametrize(
        "instance, invalid_elements",
        [
            (ContinuedFraction(1, 2), ()),
            (ContinuedFraction(1, 2), ("invalid", 1)),
            (ContinuedFraction(649, 200), (4, 12)),
            (ContinuedFraction(649, 200), (3, 4, 12, 4)),
            (ContinuedFraction(649, 200), (3, 4, 4)),
        ],
    )
    def test_ContinuedFraction__truncate__invalid_elements__value_error_raised(self, instance, invalid_elements):
        with pytest.raises(ValueError):
            instance.truncate(*invalid_elements)

    @pytest.mark.parametrize(
        "instance, tail_elements, expected_comparative_instance",
        [
            (ContinuedFraction(1, 2), (2,), ContinuedFraction(0, 1)),
            (ContinuedFraction(3, 2), (2,), ContinuedFraction(1, 1)),
            (ContinuedFraction(649, 200), (4,), ContinuedFraction(159, 49)),
            (ContinuedFraction(649, 200), (12, 4,), ContinuedFraction(13, 4)),
            (ContinuedFraction(649, 200), (4, 12, 4,), ContinuedFraction(3, 1)),
            (ContinuedFraction(-415, 93), (7,), ContinuedFraction(-58, 13)),
            (ContinuedFraction(-415, 93), (6, 7,), ContinuedFraction(-9, 2)),
            (ContinuedFraction(-415, 93), (1, 6, 7,), ContinuedFraction(-4, 1)),
            (ContinuedFraction(-415, 93), (1, 1, 6, 7,), ContinuedFraction(-5, 1)),
        ]
    )
    def test_ContinuedFraction__truncate__valid_elements__correctly_truncated(self, instance, tail_elements, expected_comparative_instance):
        original_id = id(instance)
        original_elements = instance.elements
        order = instance.order
        truncation_length = len(tail_elements)

        instance.truncate(*tail_elements)

        assert id(instance) == original_id
        assert instance == expected_comparative_instance
        assert hash(instance) == hash(expected_comparative_instance)
        assert instance == ContinuedFraction.from_elements(*original_elements[:order + 1 - truncation_length])
        assert instance.order == expected_comparative_instance.order
        assert tuple(instance.convergents) == tuple(expected_comparative_instance.convergents)
        assert tuple(instance.remainders) == tuple(expected_comparative_instance.remainders)
        assert instance.khinchin_mean == expected_comparative_instance.khinchin_mean

    @pytest.mark.parametrize(
        "cf1, cf2, k, expected_left_mediant",
        [
            (ContinuedFraction(1, 2), Fraction(3, 5), 1, ContinuedFraction(4, 7)),
            (ContinuedFraction(1, 2), ContinuedFraction(3, 5), 2, ContinuedFraction(5, 9)),
            (ContinuedFraction(1, 2), Fraction(3, 5), 3, ContinuedFraction(6, 11)),
            (ContinuedFraction(1, 2), ContinuedFraction(0), 1, ContinuedFraction(1, 3)),
            (ContinuedFraction(1, 2), Fraction(1, 2), 1, ContinuedFraction(1, 2)),
            (ContinuedFraction(1, -2), ContinuedFraction(1, 2), 1, ContinuedFraction(0, 1)),
            (ContinuedFraction(1, -2), ContinuedFraction(1, 2), 2, ContinuedFraction(-1, 6)),
            (ContinuedFraction(1, -2), ContinuedFraction(1, 2), 3, ContinuedFraction(-1, 4)),
            (ContinuedFraction(-1, 2), Fraction(1), 1, ContinuedFraction(0, 1)),
            (ContinuedFraction(-1, 2), Fraction(1), 2, ContinuedFraction(-1, 5)),
            (ContinuedFraction(-1, 2), Fraction(1), 3, ContinuedFraction(-2, 7)),
            (ContinuedFraction(-1, 2), ContinuedFraction(-1), 1, ContinuedFraction(-2, 3)),
            (ContinuedFraction(-1, 2), ContinuedFraction(-1), 2, ContinuedFraction(-3, 5)),
            (ContinuedFraction(-1, 2), ContinuedFraction(-1), 3, ContinuedFraction(-4, 7)),
            (ContinuedFraction(-1, 2), Fraction(1, -2), 1, ContinuedFraction(-1, 2)),
            (ContinuedFraction(1, 2), Fraction(3, 5), 10 ** 6, ContinuedFraction(1000003, 2000005)),
        ],
    )
    def test_ContinuedFraction__left_mediant__two_fractions__correct_mediant_returned(self, cf1, cf2, k, expected_left_mediant):
    
        assert cf1.left_mediant(cf2, k=k) == expected_left_mediant

    @pytest.mark.parametrize(
        "cf1, cf2, k, expected_right_mediant",
        [
            (ContinuedFraction(1, 2), Fraction(3, 5), 1, ContinuedFraction(4, 7)),
            (ContinuedFraction(1, 2), ContinuedFraction(3, 5), 2, ContinuedFraction(7, 12)),
            (ContinuedFraction(1, 2), Fraction(3, 5), 3, ContinuedFraction(10, 17)),
            (ContinuedFraction(1, 2), ContinuedFraction(0), 1, ContinuedFraction(1, 3)),
            (ContinuedFraction(1, 2), Fraction(1, 2), 1, ContinuedFraction(1, 2)),
            (ContinuedFraction(1, -2), ContinuedFraction(1, 2), 1, ContinuedFraction(0, 1)),
            (ContinuedFraction(-1, 2), Fraction(1), 1, ContinuedFraction(0, 1)),
            (ContinuedFraction(-1, 2), ContinuedFraction(-1), 1, ContinuedFraction(-2, 3)),
            (ContinuedFraction(-1, 2), Fraction(1, -2), 1, ContinuedFraction(-1, 2)),
            (ContinuedFraction(1, 2), Fraction(3, 5), 10 ** 6, ContinuedFraction(3000001, 5000002)),
        ],
    )
    def test_ContinuedFraction__right_mediant__two_fractions__correct_mediant_returned(self, cf1, cf2, k, expected_right_mediant):
    
        assert cf1.right_mediant(cf2, k=k) == expected_right_mediant

    @pytest.mark.parametrize(
        "cf1, cf2, expected_simple_mediant",
        [
            (ContinuedFraction(1, 2), Fraction(3, 5), ContinuedFraction(4, 7)),
            (ContinuedFraction(1, 2), ContinuedFraction(3, 5), ContinuedFraction(4, 7)),
            (ContinuedFraction(1, 2), ContinuedFraction(0), ContinuedFraction(1, 3)),
            (ContinuedFraction(1, 2), Fraction(1, 2), ContinuedFraction(1, 2)),
            (ContinuedFraction(1, -2), ContinuedFraction(1, 2), ContinuedFraction(0, 1)),
            (ContinuedFraction(-1, 2), Fraction(1), ContinuedFraction(0, 1)),
            (ContinuedFraction(-1, 2), ContinuedFraction(-1), ContinuedFraction(-2, 3)),
            (ContinuedFraction(-1, 2), Fraction(1, -2), ContinuedFraction(-1, 2)),
        ],
    )
    def test_ContinuedFraction__simple_mediant__two_fractions__correct_mediant_returned(self, cf1, cf2, expected_simple_mediant):
    
        assert cf1.mediant(cf2) == expected_simple_mediant

    @pytest.mark.parametrize(
        "k, m",
        [
            ("not an int", -1),
            ("not an int", 0),
            ("not an int", 1),
            (-1, "not an int"),
            (0, "not an int"),
            (1, "not an int"),
            ("not an int", "not an int"),
            (0, 0),
            (1, 0),
            (0, 1),
            (-1, -1),
            (1, -1),
            (-1, 1),
            (5, 1),
        ]
    )
    def test_ContinuedFraction__semiconvergent__invalid_args(self, k, m):
        test_cf = ContinuedFraction(-415, 93)

        with pytest.raises(ValueError):
            test_cf.semiconvergent(k, m)

    @pytest.mark.parametrize(
        "k, m, expected_semiconvergent",
        [
            (1, 1, ContinuedFraction(-9, 2)),
            (2, 1, ContinuedFraction(-13, 3)),
            (2, 2, ContinuedFraction(-22, 5)),
            (3, 1, ContinuedFraction(-67, 15)),
            (3, 2, ContinuedFraction(-125, 28)),
            (3, 3, ContinuedFraction(-183, 41)),
            (4, 1, ContinuedFraction(-473, 106)),
            (4, 2, ContinuedFraction(-888, 199)),
            (4, 3, ContinuedFraction(-1303, 292)),
            (4, 4, ContinuedFraction(-1718, 385)),
        ]
    )
    def test_ContinuedFraction__semiconvergent__valid_args__correct_semiconvergent_returned(self, k, m, expected_semiconvergent):
        test_cf = ContinuedFraction(-415, 93)

        assert test_cf.semiconvergent(k, m) == expected_semiconvergent
        assert test_cf.semiconvergent(k, m) == test_cf.convergent(k - 1).right_mediant(test_cf.convergent(k), k=m)

    def test_ContinuedFraction__rational_operations(self):
        f0 = ContinuedFraction(2, 1)
        f1 = ContinuedFraction(649, 200)
        f2 = ContinuedFraction(-649, 200)
        f3 = ContinuedFraction(3, 2)
        f4 = ContinuedFraction(5, 3)

        assert -f0 == -(f0) == f0.__neg__() == ContinuedFraction(*convergent(0, -2).as_integer_ratio())

        assert -f1 == f2 == f1.__neg__() == ContinuedFraction(*convergent(4, -4, 1, 3, 12, 4).as_integer_ratio())

        assert -f2 == f1 == f2.__neg__()

        assert -f3 == -(f3) == f3.__neg__() == ContinuedFraction(*convergent(1, -2, 2).as_integer_ratio())

        assert -f4 == -(f4) == f4.__neg__() == ContinuedFraction(*convergent(1, -2, 3).as_integer_ratio())

        assert f1 + f2 == ContinuedFraction(0, 1)

        assert f1 + 1 == 1 + f1 == ContinuedFraction('4.245')

        assert f1.__radd__(f2) == f2.__radd__(f1)

        assert f1.__radd__(1) == 1 + f1

        assert f1 - f2 == ContinuedFraction(649, 100)

        assert f1 - 1 == ContinuedFraction('2.245')

        assert 1 - f1 == f1.__rsub__(1) == ContinuedFraction('-2.245')

        assert f1 - 4 == ContinuedFraction('-0.755')

        assert 4 - f1 == ContinuedFraction('0.755')

        assert f1.__rsub__(f2) == f2.__radd__(-f1)

        assert -f1 + f2 == ContinuedFraction(-649, 100)

        assert -f1 - f2 == ContinuedFraction(0, 1)

        assert f1 * f2 == ContinuedFraction(-421201, 40000)

        assert f1.__rmul__(f2) == f2.__rmul__(f1)

        assert f1 * 0 == f2 * 0 == ContinuedFraction(0, 1)

        assert f1 * 1 == f2 * -1

        assert f1 / f2 == ContinuedFraction(-1, 1)

        assert f1 // f2 == f2 // f1

        assert f1 // 2 == ContinuedFraction(1, 1)

        assert 2 // f1 == ContinuedFraction(0, 1)

        assert f1 * (1 / f2) == f1 * (f2 ** -1) == ContinuedFraction(-1, 1)

        assert divmod(f1, f2) == (ContinuedFraction(-1, 1), ContinuedFraction(0, 1))

        assert f1.__rdivmod__(f2) == (ContinuedFraction(-1, 1), ContinuedFraction(0, 1))

        assert f1.__rdivmod__(2) == (ContinuedFraction(0, 1), ContinuedFraction(2, 1))

        assert f2.__rdivmod__(2) == (ContinuedFraction(-1, 1), ContinuedFraction(-249, 200))

        assert f1 ** 3 == ContinuedFraction(273359449, 8000000)

        assert f1.__rpow__(2) == Fraction(2) ** f1

        assert +f1 == f1

        assert -f1 == ContinuedFraction(-f1.numerator, f1.denominator) == ContinuedFraction(Fraction(-f1))

        assert abs(f2) == f1

    @pytest.mark.parametrize(
        "operand, expected, expected_elements",
        [
            (ContinuedFraction(-2, 1), ContinuedFraction(2, 1), (2,)),
            (ContinuedFraction(-1, 1), ContinuedFraction(1, 1), (1,)),
            (ContinuedFraction(-0, 1), ContinuedFraction(0, 1), (0,)),
            (ContinuedFraction(1, 1), ContinuedFraction(-1, 1), (-1,)),
            (ContinuedFraction(2, 1), ContinuedFraction(-2, 1), (-2,)),
            (ContinuedFraction(-649, 200), ContinuedFraction(649, 200), (3, 4, 12, 4,)),
            (ContinuedFraction(-3, 2), ContinuedFraction(3, 2), (1, 2,)),
            (ContinuedFraction(-4, 3), ContinuedFraction(4, 3), (1, 3,)),
            (ContinuedFraction(-1, 2), ContinuedFraction(1, 2), (0, 2,)),
            (ContinuedFraction(-1, 3), ContinuedFraction(1, 3), (0, 3,)),
            (ContinuedFraction(-0, 1), ContinuedFraction(0, 1), (0,)),
            (ContinuedFraction(1, 3), ContinuedFraction(-1, 3), (-1, 1, 2)),
            (ContinuedFraction(1, 2), ContinuedFraction(-1, 2), (-1, 2,)),
            (ContinuedFraction(4, 3), ContinuedFraction(-4, 3), (-2, 1, 2,)),
            (ContinuedFraction(3, 2), ContinuedFraction(-3, 2), (-2, 2,)),
            (ContinuedFraction(649, 200), ContinuedFraction(-649, 200), (-4, 1, 3, 12, 4,)),
        ]
    )
    def test___neg__(self, operand, expected, expected_elements):
        received = -operand

        assert expected == received
        assert received.elements == expected_elements
