# -- IMPORTS --

# -- Standard libraries --
from decimal import Decimal
from fractions import Fraction

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.lib import (
	_continued_fraction_rational,
	continued_fraction_rational,
	continued_fraction_real,
	convergent,
	convergents,
	fraction_from_elements,
	mediant,
	remainder,
	remainders,
)


class Test_ContinuedFractionRational:

	@pytest.mark.parametrize(
	    "x, y, elements",
	    [
	        (3, 2, tuple([1, 2])),
	        (-5000, 1, tuple([-5000])),
	        (649, 200, tuple([3, 4, 12, 4])),
	        (-649, 200, tuple([-4, 1, 3, 12, 4])),
	        (-649, -200, tuple([3, 4, 12, 4])),
	        (-1, 3, tuple([-1, 1, 2])),
	        (1, 3, tuple([0, 3])),
	        (415, 93, tuple([4, 2, 6, 7])),
	        (415, -93, tuple([-5, 1, 1, 6, 7])),
	        (10, 100, tuple([0, 10])),
	        (-95, 82, tuple([-2, 1, 5, 3, 4])),
	        (356, 103, tuple([3, 2, 5, 4, 2]))
	    ],
	)
	def test__continued_fraction_rational__valid_integers__correct_elements_generated(self, x, y, elements):
		
		expected = elements

		assert tuple(_continued_fraction_rational(x, y)) == expected


class TestContinuedFractionRational:

	@pytest.mark.parametrize(
	    "r, elements",
	    [
	        (Fraction(3, 2), tuple([1, 2])),
	        (Fraction(-5000), tuple([-5000])),
	        (Fraction(649, 200), tuple([3, 4, 12, 4])),
	        (Fraction(-649, 200), tuple([-4, 1, 3, 12, 4])),
	        (Fraction(-649, -200), tuple([3, 4, 12, 4])),
	        (Fraction(-1, 3), tuple([-1, 1, 2])),
	        (Fraction(1, 3), tuple([0, 3])),
	        (Fraction(415, 93), tuple([4, 2, 6, 7])),
	        (Fraction(415, -93), tuple([-5, 1, 1, 6, 7])),
	        (Fraction(10, 100), tuple([0, 10])),
	        (Fraction(-95, 82), tuple([-2, 1, 5, 3, 4])),
	        (Fraction(356, 103), tuple([3, 2, 5, 4, 2]))
	    ],
	)
	def test_continued_fraction_rational__valid_integers__correct_elements_generated(self, r, elements):
		
		expected = elements

		assert tuple(continued_fraction_rational(r)) == expected


class TestContinuedFractionReal:

	@pytest.mark.parametrize(
	    "x, expected",
	    [
	        (5000, (5000,)),
	        ('-5000', (-5000,)),
	        (float(5000), (5000,)),
	        (Decimal('-5000'), (-5000,)),
	        (3 / 2, (1, 2,)),
	        ('3/2', (1, 2,)),
	        ('1.5', (1, 2,)),
	        (Decimal('1.5'), (1, 2,)),
	        (3.245, (3, 4, 12, 3, 1, 234562480591, 2, 5, 2,)),
	        ('3.245', (3, 4, 12, 4,)),
	        (Decimal('3.245'), (3, 4, 12, 4)),
	       	('-3.245', (-4, 1, 3, 12, 4,)),
	        (-649 / 200, (-4, 1, 3, 12, 3, 1, 234562480591, 2, 5, 2,)),
	        (Decimal(-649 / 200), (-4, 1, 3, 12, 3, 1, 234562480591, 2, 5, 2,)),
	        ('-649/200', (-4, 1, 3, 12, 4,)),
	        (-649 / -200, (3, 4, 12, 3, 1, 234562480591, 2, 5, 2)),
	        (3333 / 10000, (0, 3, 3332, 1, 674191559, 1, 61, 7, 6,)),
	        ('0.3333', (0, 3, 3333,)),
	        (-3333 / 10000, (-1, 1, 2, 3332, 1, 674191559, 1, 61, 7, 6,)),
	        ('-0.3333', (-1, 1, 2, 3333,)),
	        (Decimal('-0.3333'), (-1, 1, 2, 3333,)),
	        (5.25, (5, 4,)),
	        ('5.25', (5, 4,)),
	        (Decimal('5.25'), (5, 4,)),
	        (Decimal(21 / 4), (5, 4,)),
	        (-5.25, (-6, 1, 3,)),
	        ('-5.25', (-6, 1, 3,)),
	        (Decimal(-21 / 4), (-6, 1, 3,)),
	    ],
	)
	def test_continued_fraction_real__valid_inputs__correct_elements_generated(self, x, expected):

		assert tuple(continued_fraction_real(x)) == expected


class TestFractionFromElements:

	@pytest.mark.parametrize(
	    "elements",
	    [
	        (1, 2.),
	        (1., 2),
	        (1., 2.)
	    ],
	)
	def test_fraction_from_elements__invalid_elements__value_error_raised(self, elements):
		with pytest.raises(ValueError):
			fraction_from_elements(*elements)

	@pytest.mark.parametrize(
	    "elements, fraction",
	    [
	        ([1, 2], Fraction(3, 2)),
	        ([-5000], Fraction(-5000, 1)),
	        ([3, 4, 12, 4], Fraction(649, 200)),
	        ([-4, 1, 3, 12, 4], Fraction(-649, 200)),
	        ([-1, 1, 2], Fraction(-1, 3)),
	        ([0, 3], Fraction(1, 3)),
	        ([4, 2, 6, 7], Fraction(415, 93)),
	        ([-5, 1, 1, 6, 7], Fraction(-415, 93)),
	        ([0, 10], Fraction(1, 10)),
	        ([-2, 1, 5, 3, 4], Fraction(-95, 82)),
	        ([3, 2, 5, 4, 2], Fraction(356, 103)),
	    ],
	)
	def test_fraction_from_elements__valid_elements__correct_fraction_returned(self, elements, fraction):
		
		expected = fraction

		assert fraction_from_elements(*elements) == expected


class TestConvergent:

	@pytest.mark.parametrize(
	    "k, elements",
	    [
	    	(1, []),
	        (1, [1., 2.]),
	        (1, [1, 2.]),
	        (1, [1., 2.]),
	        (-1, [1, 2]),
	        (2, [1, 2]),
	        (1, [1, 0, 2]),
	        (1, [1, 1, -1]),
	        (1, [1, 1, 0, -2]),
	        (2, [1, Decimal('2')]),
	    ],
	)
	def test_convergent__invalid_elements__value_error_raised(self, k, elements):
		with pytest.raises(ValueError):
			convergent(k, *elements)

	@pytest.mark.parametrize(
	    "k, elements, expected_convergent",
	    [
	        (1, [1, 2], Fraction(3, 2)),
	        (0, [-5000], Fraction(-5000, 1)),
	        (2, [3, 4, 12, 4], Fraction(159, 49)),
	        (3, [-4, 1, 3, 12, 4], Fraction(-159, 49)),
	        (2, [-1, 1, 2], Fraction(-1, 3)),
	        (1, [0, 3], Fraction(1, 3)),
	        (2, [4, 2, 6, 7], Fraction(58, 13)),
	        (3, [-5, 1, 1, 6, 7], Fraction(-58, 13)),
	        (0, [0, 10], Fraction(0, 1)),
	        (4, [-2, 1, 5, 3, 4], Fraction(-95, 82)),
	        (3, [3, 2, 5, 4, 2], Fraction(159, 46)),
	    ],
	)
	def test_convergent__valid_elements__correct_convergent_returned(self, k, elements, expected_convergent):
	
		assert convergent(k, *elements) == expected_convergent


class TestConvergents:

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
	def test_convergents__invalid_elements__value_error_raised(self, invalid_elements):
		with pytest.raises(ValueError):
			list(convergents(*invalid_elements))
	@pytest.mark.parametrize(
		"in_elements, expected_convergents",
		[
			((3,), (Fraction(3, 1),)),
			((-3,), (Fraction(-3, 1),)),
			((0,), (Fraction(0, 1),)),
			((0, 2), (Fraction(0, 1), Fraction(1, 2),)),
			((-1, 2), (Fraction(-1, 1), Fraction(-1, 2),)),
			((1, 2,), (Fraction(1, 1), Fraction(3, 2),)),
			((3, 2,), (Fraction(3, 1), Fraction(7, 2),)),
			((3, 4, 12, 4), (Fraction(3, 1), Fraction(13, 4), Fraction(159, 49), Fraction(649, 200),)),
			((-4, 1, 3, 12, 4), (Fraction(-4, 1), Fraction(-3, 1), Fraction(-13, 4), Fraction(-159, 49), Fraction(-649, 200),)),
		]
	)
	def test_convergents__valid_elements__correct_convergents_generated(self, in_elements, expected_convergents):
		assert tuple(convergents(*in_elements)) == tuple(expected_convergents)


class TestRemainder:

	@pytest.mark.parametrize(
	    "k, elements",
	    [
	    	(1, []),
	        (1, [1., 2.]),
	        (1, [1, 2.]),
	        (1, [1., 2.]),
	        (-1, [1, 2, 3]),
	       	(3, [1, 2, 3]),
	       	(1, [1, 0, 3]),
	       	(1, [1, 2, -1]),
	       	(1, [1, 0, -1]),
	        (2, [1, Decimal('2')]),
	    ],
	)
	def test_remainder__invalid_elements__value_error_raised(self, k, elements):
		with pytest.raises(ValueError):
			remainder(k, *elements)

	@pytest.mark.parametrize(
	    "k, elements, expected_remainder",
	    [
	    	(0, [0], Fraction(0, 1)),
	    	(0, [1], Fraction(1, 1)),
	    	(0, [1, 2], Fraction(3, 2)),
	        (1, [1, 2], Fraction(2, 1)),
	        (0, [-5000], Fraction(-5000, 1)),
	        (0, [3, 4, 12, 4], Fraction(649, 200)),
	        (1, [3, 4, 12, 4], Fraction(200, 49)),
	        (2, [3, 4, 12, 4], Fraction(49, 4)),
	        (3, [3, 4, 12, 4], Fraction(4, 1)),
	        (0, [-5, 1, 1, 6, 7], Fraction(-415, 93)),
	        (1, [-5, 1, 1, 6, 7], Fraction(93, 50)),
	        (2, [-5, 1, 1, 6, 7], Fraction(50, 43)),
	        (3, [-5, 1, 1, 6, 7], Fraction(43, 7)),
	        (4, [-5, 1, 1, 6, 7], Fraction(7, 1)),
	    ],
	)
	def test_remainder__valid_elements__correct_remainder_returned(self, k, elements, expected_remainder):
	
		assert remainder(k, *elements) == expected_remainder


class TestRemainders:

	@pytest.mark.parametrize(
		"invalid_elements",
		[
			(),
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
	def test_remainders__invalid_elements__value_error_raised(self, invalid_elements):
		with pytest.raises(ValueError):
			tuple(remainders(*invalid_elements))

	@pytest.mark.parametrize(
		"in_elements, expected_remainders",
		[
			((0,), (Fraction(0, 1),)),
			((1,), (Fraction(1, 1),)),
			((-1,), (Fraction(-1, 1),)),
			((0, 2), (Fraction(2, 1), Fraction(1, 2),)),
			((-1, 2), (Fraction(2, 1), Fraction(-1, 2),)),
			((1, 2,), (Fraction(2, 1), Fraction(3, 2),)),
			((3, 2,), (Fraction(2, 1), Fraction(7, 2),)),
			((3, 4, 12, 4), (Fraction(4, 1), Fraction(49, 4), Fraction(200, 49), Fraction(649, 200))),
			((-4, 1, 3, 12, 4), (Fraction(4, 1), Fraction(49, 4), Fraction(151, 49), Fraction(200, 151), Fraction(-649, 200),)),
			((-5, 1, 1, 6, 7), (Fraction(7, 1), Fraction(43, 7), Fraction(50, 43), Fraction(93, 50), Fraction(-415, 93))),
		]
	)
	def test_remainders__valid_elements__correct_remainders_generated(self, in_elements, expected_remainders):
		assert tuple(remainders(*in_elements)) == tuple(expected_remainders)


class TestMediant:


	@pytest.mark.parametrize(
		"rational1, rational2, dir, k",
		[
			(Fraction(1, 2), Fraction(3, 5), "left", 0),
			(Fraction(1, 2), Fraction(3, 5), "not left", 1),
			(Fraction(1, 2), Fraction(3, 5), "right", 0),
			(Fraction(1, 2), Fraction(3, 5), "not right", 1),
			(Fraction(1, 2), Fraction(3, 5), "not left", 0),
			(Fraction(1, 2), Fraction(3, 5), "not right", 0),
		]
	)
	def test_mediant__invalid_dir_or_order__value_error_raised(self, rational1, rational2, dir, k):
		with pytest.raises(ValueError):
			mediant(rational1, rational2, dir=dir, k=k)

	@pytest.mark.parametrize(
	    "rational1, rational2, k, expected_mediant",
	    [
	        (Fraction(1, 2), Fraction(3, 5), 1, Fraction(4, 7)),
	        (Fraction(1, 2), Fraction(3, 5), 2, Fraction(5, 9)),
	        (Fraction(1, 2), Fraction(3, 5), 3, Fraction(6, 11)),
	        (Fraction(1, 2), Fraction(0), 1, Fraction(1, 3)),
	        (Fraction(1, 2), Fraction(1, 2), 1, Fraction(1, 2)),
	        (Fraction(1, 2), Fraction(1, 2), 2, Fraction(1, 2)),
	        (Fraction(1, -2), Fraction(1, 2), 1, Fraction(0, 1)),
	        (Fraction(1, -2), Fraction(1, 2), 2, Fraction(-1, 6)),
	        (Fraction(1, -2), Fraction(1, 2), 3, Fraction(-1, 4)),
	        (Fraction(1, -2), Fraction(1, 2), 10, Fraction(-9, 22)),
	        (Fraction(-1, 2), Fraction(1), 1, Fraction(0, 1)),
	        (Fraction(-1, 2), Fraction(1), 2, Fraction(-1, 5)),
	        (Fraction(-1, 2), Fraction(1), 2, Fraction(-1, 5)),
	        (Fraction(-1, 2), Fraction(-1), 1, Fraction(-2, 3)),
	        (Fraction(-1, 2), Fraction(-1), 2, Fraction(-3, 5)),
	        (Fraction(-1, 2), Fraction(1, -2), 1, Fraction(-1, 2)),
	        (Fraction(-1, 2), Fraction(1, -2), 2, Fraction(-1, 2)),
	        (Fraction(1, 2), Fraction(3, 5), 10 ** 6, Fraction(1000003, 2000005)),
	    ],
	)
	def test_left_mediant__two_ordered_rationals__correct_mediant_returned(self, rational1, rational2, k, expected_mediant):
	
		assert mediant(rational1, rational2, dir='left', k=k) == expected_mediant

	@pytest.mark.parametrize(
	    "rational1, rational2, dir_, k, expected_mediant",
	    [
	        (Fraction(1, 2), Fraction(3, 5), 'right', 1, Fraction(4, 7)),
	        (Fraction(1, 2), Fraction(3, 5), 'right', 2, Fraction(7, 12)),
	        (Fraction(1, 2), Fraction(3, 5), 'right', 3, Fraction(10, 17)),
	        (Fraction(1, 2), Fraction(0), 'right', 1, Fraction(1, 3)),
	        (Fraction(1, 2), Fraction(1, 2), 'right', 1, Fraction(1, 2)),
	        (Fraction(1, -2), Fraction(1, 2), 'right', 1, Fraction(0, 1)),
	        (Fraction(-1, 2), Fraction(1), 'right', 1, Fraction(0, 1)),
	        (Fraction(-1, 2), Fraction(-1), 'right', 1, Fraction(-2, 3)),
	        (Fraction(-1, 2), Fraction(1, -2), 'right', 1, Fraction(-1, 2)),
	        (Fraction(1, 2), Fraction(3, 5), 'right', 10 ** 6, Fraction(3000001, 5000002)),
	    ],
	)
	def test_right_mediant__two_ordered_rationals__correct_mediant_returned(self, rational1, rational2, dir_, k, expected_mediant):
	
		assert mediant(rational1, rational2, dir=dir_, k=k) == expected_mediant
