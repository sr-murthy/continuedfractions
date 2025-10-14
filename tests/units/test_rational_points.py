# -- IMPORTS --

# -- Standard libraries --

import decimal

# Set the :py:mod:`decimal` context for the test computations in this module
# using default precision of 28 digits, including the integer part, and 
# turn off the :py:class:`decimal.Inexact` trap
context = decimal.Context(prec=28, Emax=decimal.MAX_EMAX, Emin=decimal.MIN_EMIN)
context.traps[decimal.Inexact] = False
decimal.setcontext(context)

import math

from decimal import Decimal as D
from fractions import Fraction as F

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.continuedfraction import ContinuedFraction as CF
from continuedfractions.rational_points import (
    RationalPoint as RP,
    RationalTuple as RT,
    Dim2RationalCoordinates as D2RC,
    Dim3RationalCoordinates as D3RC,
    HomogeneousCoordinates as HC,
)


class TestRationalTuple:

    @pytest.mark.parametrize(
        "args",
        [
            (D('0'),),
            (0, 1., 2),
            (0, .5),
            (-1/2, 3, 4),
            (D('2'), 3, '4'),
        ]
    )
    def test_RationalTuple___new____invalid_args__value_error_raised(self, args):
        with pytest.raises(ValueError):
            RT(*args)

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3), CF(4, 5), 6),
            (F(1, 2), CF(3, 4), 5),
            (1, -2),
            (CF(1, 2),),
            (0,)
        ]
    )
    def test_RationalTuple___new__(self, args):
        t = RT(*args)
        assert t == args

    @pytest.mark.parametrize(
        "rational_tuple, invalid_arg",
        [
            (RT(1, -2), 3, D('4'),),
            (RT(1, F(   2, 3), CF(-4, 5)), 1.5,),
            (RT(1, -2, 3), -1/2,),
        ]
    )
    def test_RationalTuple_scale(self, rational_tuple, invalid_arg):
        with pytest.raises(ValueError):
            rational_tuple.scale(invalid_arg)

    @pytest.mark.parametrize(
        "rational_tuple, scalar, expected_scaled_rational_tuple",
        [
            (RT(1, -2), 3, RT(3, -6),),
            (RT(1, F(2, 3), CF(-4, 5)), 15, RT(15, 10, -12),),
            (RT(1, -2, 3), -1, RT(-1, 2, -3)),
            (RT(1, F(2, 3), CF(3, 4)), F(1, 2), RT(F(1, 2), F(1, 3), CF(3, 8))),
            (RT(1, -2), 0, RT(0, 0)),
        ]
    )
    def test_RationalTuple_scale(self, rational_tuple, scalar, expected_scaled_rational_tuple):
        received = rational_tuple.scale(scalar)
        assert isinstance(received, RT)
        assert received == expected_scaled_rational_tuple


class TestDim2RationalCoordinates:

    @pytest.mark.parametrize(
        "args",
        [
            (D('0'),),
            (0, 1., 2),
            (0, .5),
            (-1/2, 3, 4),
            (D('2'), 3, '4'),
            (1, F(2, 3), CF(4, 5))
        ]
    )
    def test_Dim2RationalCoordinates___new____invalid_args__value_error_raised(self, args):
        with pytest.raises(ValueError):
            D2RC(*args)

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3)),
            (F(1, 2), CF(3, 4)),
            (1, -2),
            (CF(1, 2), -2),
            (0, 1),
        ]
    )
    def test_Dim2RationalCoordinates___new__(self, args):
        t = D2RC(*args)
        assert t == args

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3)),
            (F(1, 2), CF(3, 4)),
            (1, -2),
            (CF(1, 2), -2),
            (0, 1),
        ]
    )
    def test_Dim2RationalCoordinates_x_and_y_coordinates(self, args):
        t = D2RC(*args)
        assert (t.x, t.y) == args


class TestDim3RationalCoordinates:

    @pytest.mark.parametrize(
        "args",
        [
            (D('0'),),
            (0, 1., 2),
            (0, .5),
            (-1/2, 3, 4),
            (D('2'), 3, '4'),
            (1, F(1, 2))
        ]
    )
    def test_Dim3RationalCoordinates___new____invalid_args__value_error_raised(self, args):
        with pytest.raises(ValueError):
            D3RC(*args)

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3), CF(4, 5)),
            (F(1, 2), -3, CF(4, 5)),
            (F(1, 2), CF(4, 5), -3),
            (1, CF(-2, 3), F(4, 5)),
            (CF(1, 2), F(-3, 4), 5),
        ]
    )
    def test_Dim3RationalCoordinates___new__(self, args):
        t = D3RC(*args)
        assert t == args

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3), CF(4, 5)),
            (F(1, 2), -3, CF(4, 5)),
            (F(1, 2), CF(4, 5), -3),
            (1, CF(-2, 3), F(4, 5)),
            (CF(1, 2), F(-3, 4), 5),
        ]
    )
    def test_Dim3RationalCoordinates_x_and_y_and_z_coordinates(self, args):
        t = D3RC(*args)
        assert (t.x, t.y, t.z) == args


class TestHomogeneousCoordinates:

    @pytest.mark.parametrize(
        "args",
        [
            (1, F(-2, 3), CF(4, 5)),
            (F(1, 2), -3, CF(4, 5)),
            (F(1, 2), CF(4, 5), -3),
            (1, CF(-2, 3), F(4, 5)),
            (CF(1, 2), F(-3, 4), 5),
        ]
    )
    def test_HomogeneousCoordinates___new__(self, args):
        t = HC(*args)
        assert t == args

    @pytest.mark.parametrize(
        "homogeneous_coordinates, expected_rational_point",
        [
            (HC(1, F(-2, 3), CF(4, 5)), RP(F(5, 4), F(-5, 6)),),
            (HC(F(1, 2), -3, CF(4, 5)), RP(F(5, 8), F(-15, 4)),),
            (HC(F(1, 2), CF(4, 5), -3), RP(F(-1, 6), F(-4, 15)),),
            (HC(1, CF(-2, 3), F(4, 5)), RP(F(5, 4), F(-5, 6)),),
            (HC(CF(1, 2), F(-3, 4), 5), RP(F(1, 10), F(-3, 20))),
        ]
    )
    def test_HomogeneousCoordinates_to_rational_point(self, homogeneous_coordinates, expected_rational_point):
        assert homogeneous_coordinates.to_rational_point() == expected_rational_point


class TestRationalPoint:

    @pytest.mark.parametrize(
        "args",
        [
            (0,),
            (0, 1, 2),
            (0, .5),
            (-1/2, 3, 4),
            (D('2'), 3),
        ]
    )
    def test_RationalPoint___new____invalid_args__value_error_raised(self, args):
        with pytest.raises(ValueError):
            RP.__new__(RP.__class__, *args)

    @pytest.mark.parametrize(
        "rational_point",
        [
            (RP(1, 2),),
            (RP(1, F(2, 3)),),
            (RP(F(1, 2), 3),),
            (RP(F(3, 5), F(4, 5)),),
            (RP(F(-3, 5), F(4, 5)),),
        ]
    )
    def test_RationalPoint___repr__(self, rational_point):
        x, y = rational_point[0].coordinates
        assert rational_point[0].__repr__() == f'RationalPoint({x}, {y})'

    @pytest.mark.parametrize(
        "rational_point, expected_x",
        [
            (RP(1, 2), CF(1, 1),),
            (RP(1, F(2, 3)), CF(1, 1),),
            (RP(F(1, 2), 3), CF(1, 2),),
            (RP(F(3, 5), F(4, 5)), CF(3, 5),),
            (RP(F(-3, 5), F(4, 5)), CF(-3, 5),),
        ]
    )
    def test_RationalPoint_x_property(self, rational_point, expected_x):
        assert rational_point.x == expected_x

    @pytest.mark.parametrize(
        "rational_point, y",
        [
            (RP(1, 2), CF(2, 1),),
            (RP(1, F(2, 3)), CF(2, 3),),
            (RP(F(1, 2), 3), CF(3, 1),),
            (RP(F(3, 5), F(4, 5)), CF(4, 5),),
            (RP(F(-3, 5), F(4, 5)), CF(4, 5),),
        ]
    )
    def test_RationalPoint_y_property(self, rational_point, y):
        expected_y = y
        assert rational_point.y == expected_y

    @pytest.mark.parametrize(
        "rational_point, expected_coordinates",
        [
            (RP(1, 2), D2RC(CF(1, 1), CF(2, 1)),),
            (RP(1, F(2, 3)), D2RC(CF(1, 1), CF(2, 3)),),
            (RP(F(1, 2), 3), D2RC(CF(1, 2), CF(3, 1)),),
            (RP(F(3, 5), F(4, 5)), D2RC(CF(3, 5), CF(4, 5)),),
            (RP(F(-3, 5), F(4, 5)), D2RC(CF(-3, 5), CF(4, 5)),),
        ]
    )
    def test_RationalPoint_coordinates_property(self, rational_point, expected_coordinates):
        assert rational_point.coordinates == expected_coordinates

    @pytest.mark.parametrize(
        "rational_point1, invalid_other",
        [
            (RP(0, 0), (1, 2),),
            (RP(1, 2), D('0'),),
            (RP(1, 1), 1.1,),
            (RP(1, 1), -1,),
            (RP(F(1, 2), F(3, 4)), 5,),
        ]
    )
    def test_RationalPoint_dot__invalid_other__value_error_raised(self, rational_point1, invalid_other):
        with pytest.raises(ValueError):
            rational_point1.dot(invalid_other)

    def test_RationalPoint_zero(self):
        assert RP.zero() == RP(0, 0)

    @pytest.mark.parametrize(
        "rational_points, expected_sum",
        [
            ((RP(1, 1), RP(1, 2), RP(1, 3),), RP(3, 6)),
            ((RP(F(1, 2), 1), RP(F(-1, 2), -1),), RP(0, 0)),
            ((RP(0, 0), RP(1, F(-1, 2)), RP(F(3, 5), F(4, 5)), RP(F(5, 12), 6)), RP(F(121, 60), F(63, 10)))
        ]
    )
    def test_RationalPoint_sum(self, rational_points, expected_sum):
        assert RP.sum(*rational_points) == expected_sum

    @pytest.mark.parametrize(
        "rational_point1, invalid_other",
        [
            (RP(0, 0), (0, 0),),
            (RP(1, 1), RP(1, 1),),
            (RP(1, 1), D('0'),),
            (RP(1, 1), 1.1,),
            (RP(1, 1), -1,),
        ]
    )
    def test_RationalPoint_gradient__invalid_other__value_error_raised(self, rational_point1, invalid_other):
        with pytest.raises(ValueError):
            rational_point1.gradient(other=invalid_other)

    @pytest.mark.parametrize(
        "rational_point, expected_gradient",
        [
            (RP(1, 1), CF(1, 1)),
            (RP(1, F(1, 2)), CF(1, 2)),
            (RP(1, 2), CF(2, 1)),
            (RP(-1, 1), CF(-1, 1)),
        ]
    )
    def test_RationalPoint_gradient__no_other_rational_point(self, rational_point, expected_gradient):
        assert rational_point.gradient() == expected_gradient

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_gradient",
        [
            (RP(1, 1), RP(0, 1), CF(0, 1)),
            (RP(1, 1), RP(2, 3), CF(2, 1)),
            (RP(1, 1), RP(2, F(3, 2)), CF(1, 2)),
            (RP(1, 0), RP(0, 1), CF(-1, 1)),
        ]
    )
    def test_RationalPoint_gradient__other_rational_point(self, rational_point1, rational_point2, expected_gradient):
        assert rational_point1.gradient(other=rational_point2) == expected_gradient

    @pytest.mark.parametrize(
        "rational_point, expected_angle, expected_angle_as_degrees",
        [
            (RP(1, 0), D('0'), D('0'),),
            (RP(1, 1), D(math.atan2(1, 1)), D('45'),),
            (RP(0, 1), D(math.atan2(1, 0)), D('90'),),
            (RP(-1, 1), D(math.atan2(1, -1)), D('135'),),
            (RP(-1, 0), D(math.atan2(0, -1)), D('180'),),
            (RP(-1, -1), D(math.atan2(-1, -1)), -D('135'),),
            (RP(0, -1), D(math.atan2(-1, 0)), -D('90'),),
            (RP(1, -1), D(math.atan2(-1, 1)), -D('45'),),
        ]
    )
    def test_RationalPoint_angle__with_pos_x_axis(self, rational_point, expected_angle, expected_angle_as_degrees):
        assert rational_point.angle() == expected_angle
        assert rational_point.angle(as_degrees=True) == expected_angle_as_degrees

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_angle, expected_angle_as_degrees",
        [
            (RP(1, 0), RP(1, 1), D('0.78539816339744827899949086713604629039764404296875'), D('45'),),
            (RP(1, 0), RP(0, 1), D('1.5707963267948965579989817342720925807952880859375'), D('90'),),
            (RP(1, 0), RP(-1, 1), D('2.35619449019234483699847260140813887119293212890625'), D('135'),),
            (RP(1, 0), RP(-1, 0), D('3.141592653589793115997963468544185161590576171875'), D('180'),),
            (RP(1, 1), RP(-1, 1), D('1.5707963267948965579989817342720925807952880859375'), D('90'),),
            (RP(1, 1), RP(1, 1), D('0'), D('0'),),
        ]
    )
    def test_RationalPoint_angle__with_another_rational_point(self, rational_point1, rational_point2, expected_angle, expected_angle_as_degrees):
        assert rational_point1.angle(other=rational_point2) == expected_angle
        assert rational_point1.angle(other=rational_point2, as_degrees=True) == expected_angle_as_degrees

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_dot_product",
        [
            (RP(0, 0), RP(1, 2), CF(0, 1),),
            (RP(1, 2), RP(0, 0), CF(0, 1),),
            (RP(1, 1), RP(1, 1), CF(2, 1),),
            (RP(1, 1), RP(-1, 1), CF(0, 1),),
            (RP(F(1, 2), F(3, 4)), RP(F(-1, 2), F(-3, 4)), CF(-13, 16),),
            (RP(F(3, 5), F(4, 5)), RP(F(3, 5), F(4, 5)), CF(1, 1),),
        ]
    )
    def test_RationalPoint_dot(self, rational_point1, rational_point2, expected_dot_product):
        assert rational_point1.dot(rational_point2) == expected_dot_product

    @pytest.mark.parametrize(
        "rational_point1, invalid_arg",
        [
            (RP(1, 1), 2,),
            (RP(1, 1), 2.0,),
            (RP(1, 1), D('2'),),
        ]
    )
    def test_RationalPoint_det__invalid_arg__value_error_raised(self, rational_point1, invalid_arg):
        with pytest.raises(ValueError):
            rational_point1.det(invalid_arg)

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_det",
        [
            (RP(F(3, 5), F(4, 5)), RP(1, 1), CF(-1, 5),),
            (RP(1, 1), RP(F(5, 4), 2), CF(3, 4),),
            (RP(F(3, 5), F(4, 5)), RP(F(5, 4), 2), CF(1, 5),),
            (RP(F(1, 2), F(1, 2)), RP(1, 1), CF(0, 1)),
            (RP(1, 1), RP(0, 0), CF(0, 1)),
            (RP(0, 0), RP(1, 1), CF(0, 1)),
        ]
    )
    def test_RationalPoint_det(self, rational_point1, rational_point2, expected_det):
        assert rational_point1.det(rational_point2) == expected_det


    @pytest.mark.parametrize(
        "rational_point, expected_orthogonal",
        [
            (RP(0, 0), RP(0, 0)),
            (RP(1, 2), RP(-2, 1)),
            (RP(1, -2), RP(2, 1))
        ]
    )
    def test_RationalPoint_orthogonal(self, rational_point, expected_orthogonal):
        assert rational_point.orthogonal() == expected_orthogonal

    @pytest.mark.parametrize(
        "rational_point, expected_permutation",
        [
            (RP(0, 0), RP(0, 0)),
            (RP(1, 2), RP(2, 1)),
            (RP(1, -2), RP(-2, 1))
        ]
    )
    def test_RationalPoint_permute(self, rational_point, expected_permutation):
        assert rational_point.permute() == expected_permutation

    @pytest.mark.parametrize(
        "rational_point, invalid_x_translate, invalid_y_translate",
        [
            (RP(1, 2), 1/2, -0.1),
            (RP(1, 2), D('1'), None),
        ]
    )
    def test_RationalPoint_translate__invalid_x_or_y_translates__value_error_raised(self, rational_point, invalid_x_translate, invalid_y_translate):
        with pytest.raises(ValueError):
            rational_point.translate(x_by=invalid_x_translate, y_by=invalid_y_translate)

    @pytest.mark.parametrize(
        "rational_point, x_translate, y_translate, expected_translate",
        [
            (RP(1, 2), None, None, RP(1, 2)),
            (RP(0, 0), 1, -1, RP(1, -1)),
            (RP(F(1, 2), F(-2, 3)), F(1, 4), F(-1, 3), RP(F(3, 4), -1)),
            (RP(F(3, 5), F(4, 5)), F(-3, 5), F(-4, 5), RP(0, 0))
        ]
    )
    def test_RationalPoint_translate(self, rational_point, x_translate, y_translate, expected_translate):
        if x_translate and y_translate:
            assert rational_point.translate(x_by=x_translate, y_by=y_translate) == expected_translate
        else:
            assert rational_point.translate() == expected_translate

    @pytest.mark.parametrize(
        "rational_point, invalid_axis",
        [
            (RP(1, 1), "X"),
            (RP(1, 1), "Y"),
        ]
    )
    def test_RationalPoint_reflect__invalid_axis__value_error_raised(self, rational_point, invalid_axis):
        with pytest.raises(ValueError):
            rational_point.reflect(axis=invalid_axis)

    @pytest.mark.parametrize(
        "rational_point, axis, expected_reflection",
        [
            (RP(1, 0), "x", RP(1, 0)),
            (RP(1, 0), "y", RP(-1, 0)),
            (RP(0, 1), "x", RP(0, -1)),
            (RP(0, 1), "y", RP(0, 1)),
            (RP(1, 1), "x", RP(1, -1)),
            (RP(1, 1), "y", RP(-1, 1)),

        ]
    )
    def test_RationalPoint_reflect(self, rational_point, axis, expected_reflection):
        assert rational_point.reflect(axis=axis) == expected_reflection

    @pytest.mark.parametrize(
        "rational_point, expected_norm_squared",
        [
            (RP(0, 0), CF(0, 1),),
            (RP(1, F(2, 3)), CF(13, 9),),
            (RP(F(1, 2), 3), CF(37, 4),),
            (RP(F(3, 5), F(4, 5)), CF(1, 1),),
            (RP(F(-3, 5), F(4, 5)), CF(1, 1),),
        ]
    )
    def test_RationalPoint_norm_squared_property(self, rational_point, expected_norm_squared):
        assert rational_point.norm_squared == expected_norm_squared

    @pytest.mark.parametrize(
        "rational_point, expected_norm",
        [
            (RP(0, 0), D('0'),),
            (RP(1, F(2, 3)), D('1.201850425154663097706407089'),),
            (RP(F(1, 2), 3), D('3.041381265149109844499842123'),),
            (RP(F(3, 5), F(4, 5)), D('1'),),
            (RP(F(-3, 5), F(4, 5)), D('1'),),
        ]
    )
    def test_RationalPoint_norm_property(self, rational_point, expected_norm):
        assert rational_point.norm == expected_norm

    @pytest.mark.parametrize(
        "rational_point, expected_absolute_value",
        [
            (RP(0, 0), D('0'),),
            (RP(1, F(2, 3)), D('1.201850425154663097706407089'),),
            (RP(F(1, 2), 3), D('3.041381265149109844499842123'),),
            (RP(F(3, 5), F(4, 5)), D('1'),),
            (RP(F(-3, 5), F(4, 5)), D('1'),),
        ]
    )
    def test_RationalPoint___abs__(self, rational_point, expected_absolute_value):
        assert abs(rational_point) == expected_absolute_value

    @pytest.mark.parametrize(
        "rational_point1, invalid_other",
        [
            (RP(0, 0), (1, 2),),
            (RP(1, 2), D('0'),),
            (RP(1, 1), 1.1,),
            (RP(1, 1), -1,),
            (RP(F(1, 2), F(3, 4)), 5,),
        ]
    )
    def test_RationalPoint_distance_squared__invalid_other__value_error_raised(self, rational_point1, invalid_other):
        with pytest.raises(ValueError):
            rational_point1.distance_squared(invalid_other)

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_distance_squared",
        [
            (RP(0, 0), RP(1, 2), CF(5, 1),),
            (RP(1, 2), RP(0, 0), CF(5, 1),),
            (RP(1, 1), RP(1, 1), CF(0, 1),),
            (RP(1, 1), RP(-1, 1), CF(4, 1),),
            (RP(F(1, 2), F(3, 4)), RP(F(-1, 2), F(-3, 4)), CF(13, 4),),
            (RP(F(3, 5), F(4, 5)), RP(1, 1), CF(1, 5),),
        ]
    )
    def test_RationalPoint_distance_squared(self, rational_point1, rational_point2, expected_distance_squared):
        assert rational_point1.distance_squared(rational_point2) == expected_distance_squared

    @pytest.mark.parametrize(
        "rational_point1, invalid_other",
        [
            (RP(0, 0), (1, 2),),
            (RP(1, 2), D('0'),),
            (RP(1, 1), 1.1,),
            (RP(1, 1), -1,),
            (RP(F(1, 2), F(3, 4)), 5,),
        ]
    )
    def test_RationalPoint_distance__invalid_other__value_error_raised(self, rational_point1, invalid_other):
        with pytest.raises(ValueError):
            rational_point1.distance(invalid_other)

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_distance",
        [
            (RP(0, 0), RP(1, 2), D('2.236067977499789696409173669'),),
            (RP(1, 1), RP(1, 1), D('0'),),
            (RP(1, 1), RP(-1, 1), D('2'),),
            (RP(F(1, 2), F(3, 4)), RP(F(-1, 2), F(-3, 4)), D('1.802775637731994646559610634'),),
            (RP(F(3, 5), F(4, 5)), RP(1, 1), D('0.4472135954999579392818347337'),),
        ]
    )
    def test_RationalPoint_distance(self, rational_point1, rational_point2, expected_distance):
        assert rational_point1.distance(rational_point2) == expected_distance

    @pytest.mark.parametrize(
        "rational_point, incompatible_operand",
        [
            (RP(1, 0), (1, 0),),
            (RP(1, 0), 1,),
            (RP(1, 1), 1.1,),
            (RP(1, 1), D('1'),),
            (RP(0, 0), RP(1, 0),),
        ]
    )
    def test_RationalPoint_perpendicular_distance__incompatible_operand__value_error_raised(self, rational_point, incompatible_operand):
        with pytest.raises(ValueError):
            rational_point.perpendicular_distance(incompatible_operand)

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_perpendicular_distance",
        [
            (RP(1, 0), RP(0, 1), D('1'),),
            (RP(0, 1), RP(1, 0), D('1'),),
            (RP(1, 0), RP(1, 0), D('0'),),
            (RP(1, 0), RP(-1, 0), D('0'),),
            (RP(F(1, 2), F(1, 2)), RP(0, 1), D('0.7071067811865475244008443621'),),
            (RP(F(1, 2), F(1, 2)), RP(1, 1), D('0'),),
        ]
    )
    def test_RationalPoint_perpendicular_distance(self, rational_point1, rational_point2, expected_perpendicular_distance):
        assert rational_point1.perpendicular_distance(rational_point2) == expected_perpendicular_distance

    @pytest.mark.parametrize(
        "rational_point, expected_is_lattice_point",
        [
            (RP(0, 0), True),
            (RP(F(2, 1), 5), True),
            (RP(F(1, 2), 3), False),
            (RP(F(3, 5), F(4, 5)), False),
            (RP(-1, 2), True),
        ]
    )
    def test_RationalPoint_is_lattice_point(self, rational_point, expected_is_lattice_point):
        assert rational_point.is_lattice_point() == expected_is_lattice_point

    @pytest.mark.parametrize(
        "rational_point1, invalid_other",
        [
            (RP(0, 0), (1, 2),),
            (RP(1, 2), D('0'),),
            (RP(1, 1), 1.1,),
            (RP(1, 1), -1,),
            (RP(F(1, 2), F(3, 4)), 5,),
        ]
    )
    def test_RationalPoint_rectilinear_distance__invalid_other__value_error_raised(self, rational_point1, invalid_other):
        with pytest.raises(ValueError):
            rational_point1.rectilinear_distance(invalid_other)

    @pytest.mark.parametrize(
        "rational_point1, rational_point2, expected_rectilinear_distance",
        [
            (RP(0, 0), RP(1, 2), CF(3, 1),),
            (RP(1, 1), RP(1, 1), CF(0, 1),),
            (RP(1, 1), RP(-1, 1), CF(2, 1),),
            (RP(F(1, 2), F(3, 4)), RP(F(-1, 2), F(-3, 4)), CF(5, 2),),
            (RP(F(3, 5), F(4, 5)), RP(1, 1), CF(3, 5),),
        ]
    )
    def test_RationalPoint_rectilinear_distance(self, rational_point1, rational_point2, expected_rectilinear_distance):
        assert rational_point1.rectilinear_distance(rational_point2) == expected_rectilinear_distance

    @pytest.mark.parametrize(
        "rational_point, expected_rectilinear_norm",
        [
            (RP(0, 0), CF(0, 1),),
            (RP(1, F(2, 3)), CF(5, 3),),
            (RP(F(1, 2), 3), CF(7, 2),),
            (RP(F(3, 5), F(4, 5)), CF(7, 5),),
            (RP(F(-3, 5), F(4, 5)), CF(7, 5),),
        ]
    )
    def test_RationalPoint_rectilinear_norm_property(self, rational_point, expected_rectilinear_norm):
        assert rational_point.rectilinear_norm == expected_rectilinear_norm

    @pytest.mark.parametrize(
        "rational_point, expected_homogeneous_coordinates",
        [
            (RP(0, 0), HC(0, 0, 1),),
            (RP(F(2, 1), 5), HC(2, 5, 1),),
            (RP(F(1, 2), 3), HC(1, 6, 2),),
            (RP(F(3, 5), F(4, 5)), HC(3, 4, 5),),
            (RP(F(-3, 5), F(4, 5)), HC(-3, 4, 5),),
            (RP(-1, 2), HC(-1, 2, 1),),
        ]
    )
    def test_RationalPoint_homogeneous_coordinates_property(self, rational_point, expected_homogeneous_coordinates):
        assert rational_point.homogeneous_coordinates == expected_homogeneous_coordinates

    @pytest.mark.parametrize(
        "rational_point, expected_height",
        [
            (RP(0, 0), 1,),
            (RP(F(2, 1), 5), 5,),
            (RP(F(1, 2), 3), 6,),
            (RP(F(3, 5), F(4, 5)), 5,),
            (RP(F(-3, 5), F(4, 5)), 5,),
            (RP(-1, 2), 2,),
        ]
    )
    def test_RationalPoint_height_property(self, rational_point, expected_height):
        assert rational_point.height == expected_height

    @pytest.mark.parametrize(
        "rational_point, expected_log_height",
        [
            (RP(0, 0), D('0'),),
            (RP(F(2, 1), 5), D('1.6094379124341002817999424223671667277812957763671875'),),
            (RP(F(1, 2), 3), D('1.791759469228054957312679107417352497577667236328125'),),
            (RP(F(3, 5), F(4, 5)), D('1.6094379124341002817999424223671667277812957763671875'),),
            (RP(F(-3, 5), F(4, 5)), D('1.6094379124341002817999424223671667277812957763671875'),),
            (RP(-1, 2), D('0.69314718055994528622676398299518041312694549560546875'),),
        ]
    )
    def test_RationalPoint_log_projective_height_property(self, rational_point, expected_log_height):
        assert rational_point.log_height == expected_log_height

    def test_RationalPoint_rational_operations__invalid_operands__type_errors_raised(self):

        with pytest.raises(TypeError):
            RP(1, 2) + 3
            RP(1, 2) + D('3')
            RP(1, 2) + -.3

            RP(1, 2) - 3
            RP(1, 2) - D('3')
            RP(1, 2) - .3

            D('3') * RP(1, 2)
            .3 * RP(1, 2)

        with pytest.raises(NotImplementedError):
            RP(1, 2) * 3
            RP(3, 4) * RP(1, 2)

    def test_RationalPoint_rational_operations(self):
        r0 = RP(0, 0)

        r1 = RP(1, 1)
        r1_minus = RP(-1, -1)

        pt1 = RP(F(3, 5), F(4, 5))
        pt1_minus = RP(F(-3, 5), F(-4, 5))

        pt2 = RP(F(1, 2), F(3, 4))
        pt2_minus = RP(F(-1, 2), F(-3, 4))

        # Addition:
        #     preserves identity with ``(0, 0)``
        for r in [r1, r1_minus, pt1, pt1_minus]:
            assert r0 + r == r + r0 == r
        #     is associative
        assert r1 + (pt1 + pt2) == (r1 + pt1) + pt2
        #     is commutative
        assert r1 + pt1 == pt1 + r1
        assert r1 + pt2 == pt2 + r1
        assert pt1 + pt2 == pt2 + pt1

        # Negation and subtraction:
        #     sign carries through as expected
        assert -r1 == r1_minus
        assert -pt1 == pt1_minus
        assert -pt2 == pt2_minus
        #     inverses cancel out
        assert r1 + r1_minus == r1_minus + r1 == r0
        assert pt1 + pt1_minus == pt1_minus + pt1 == r0
        assert pt2 + pt2_minus == pt2_minus + pt2 == r0
        #     subtractions as expected
        assert r1 - pt1 == -pt1 + r1 == RP(F(2, 5), F(1, 5))
        assert r1 - pt2 == -pt2 + r1 == RP(F(1, 2), F(1, 4))
        assert pt1 - pt2 == -pt2 + pt1 == RP(F(1, 10), F(1, 20))

        # Scalar left-multiplication
        #     preserves identity with ``1``
        assert 1 * r1 == r1
        assert 1 * pt1 == pt1
        assert 1 * pt2 == pt2
        #     zeroes identity with ``0``
        assert 0 * r1 == r0
        assert 0 * pt1 == r0
        assert 0 * pt2 == r0
        #     distributes over addition of rational points
        assert 2 * (r1 + pt1 + pt2) == 2 * r1 + 2 * pt1 + 2 * pt2

