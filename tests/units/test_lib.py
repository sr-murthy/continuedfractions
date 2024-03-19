# -- IMPORTS --

# -- Standard libraries --
from fractions import Fraction

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.lib import (
	continued_fraction_rational,
	continued_fraction_real,
	fraction_from_elements,
	convergent,
	mediant,
)


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
		"x",
		[
			(1/1j,),
			("not a numeric string"),
			("1a23"),
		]
	)
	def test_continued_fraction_real__invalid_inputs__value_error_raised(self, x):
		with pytest.raises(ValueError):
			list(continued_fraction_real(x))

	@pytest.mark.parametrize(
	    "x, elements",
	    [
	        (3/2, tuple([1, 2])),
	        ('1.5', tuple([1, 2])),
	        ('-5000', tuple([-5000])),
	        (3.245, tuple([3, 4, 12, 4])),
	        (-649/200, tuple([-4, 1, 3, 12, 4])),
	        (-649/-200, tuple([3, 4, 12, 4])),
	        ('0.3333', tuple([0, 3, 3333])),
	        ('-0.3333', tuple([-1, 1, 2, 3333])),
	        ('-5.25', tuple([-6, 1, 3])),
	        ('5.25', tuple([5, 4])),
	        ('0.3', tuple([0, 3, 3])),
	        (0.1, tuple([0, 10])),
	        ('-3.245', tuple([-4, 1, 3, 12, 4])),
	    ],
	)
	def test_continued_fraction_real__valid_inputs__correct_elements_generated(self, x, elements):
		
		expected = elements

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
	    "elements, k",
	    [
	        ([1., 2.], 1),
	        ([1, 2.], 1),
	        ([1., 2.], 1),
	        ([1, 2], -1),
	        ([1, 2], 2),
	    ],
	)
	def test_convergent__invalid_elements__value_error_raised(self, elements, k):
		with pytest.raises(ValueError):
			convergent(*elements, k=k)

	@pytest.mark.parametrize(
	    "elements, k, expected_convergent",
	    [
	        ([1, 2], 1, Fraction(3, 2)),
	        ([-5000], 0, Fraction(-5000, 1)),
	        ([3, 4, 12, 4], 2, Fraction(159, 49)),
	        ([-4, 1, 3, 12, 4], 3, Fraction(-159, 49)),
	        ([-1, 1, 2], 2, Fraction(-1, 3)),
	        ([0, 3], 1, Fraction(1, 3)),
	        ([4, 2, 6, 7], 2, Fraction(58, 13)),
	        ([-5, 1, 1, 6, 7], 3, Fraction(-58, 13)),
	        ([0, 10], 0, Fraction(0, 1)),
	        ([-2, 1, 5, 3, 4], 4, Fraction(-95, 82)),
	        ([3, 2, 5, 4, 2], 3, Fraction(159, 46)),
	    ],
	)
	def test_convergent__valid_elements__correct_convergent_returned(self, elements, k, expected_convergent):
	
		assert convergent(*elements, k=k) == expected_convergent

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
