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
	kth_convergent,
)


class TestContinuedFractionsRational:

	@pytest.mark.parametrize(
	    "x, y",
	    [
	        (-1., 2),
	        (1, -2.),
	        (-1., 2.)

	    ],
	)
	def test_continued_fraction_rational__non_integers__value_error_raised(self, x, y):
		with pytest.raises(ValueError):
			list(continued_fraction_rational(x, y))

	@pytest.mark.parametrize(
	    "x, y",
	    [
	        (-1, 0),
	        (1, -0),
	        (-1, +0)

	    ],
	)
	def test_continued_fraction_rational__zero_denominator__zero_division_error_raised(self, x, y):
		with pytest.raises(ZeroDivisionError):
			list(continued_fraction_rational(x, y))

	@pytest.mark.parametrize(
	    "x, y, elements",
	    [
	        (3, 2, [1, 2]),
	        (-5000, 1, [-5000]),
	        (649, 200, [3, 4, 12, 4]),
	        (-649, 200, [-4, 1, 3, 12, 4]),
	        (-649, -200, [3, 4, 12, 4]),
	        (-1, 3, [-1, 1, 2]),
	        (1, 3, [0, 3]),
	        (415, 93, [4, 2, 6, 7]),
	        (415, -93, [-5, 1, 1, 6, 7]),
	        (10, 100, [0, 10]),
	        (-95, 82, [-2, 1, 5, 3, 4]),
	        (356, 103, [3, 2, 5, 4, 2])
	    ],
	)
	def test_continued_fraction_rational__valid_integers__correct_elements_generated(self, x, y, elements):
		
		expected = elements

		assert list(continued_fraction_rational(x, y)) == expected


class TestContinuedFractionReal:

	@pytest.mark.parametrize(
	    "x, elements",
	    [
	        (3/2, [1, 2]),
	        ('1.5', [1, 2]),
	        ('-5000', [-5000]),
	        (3.245, [3, 4, 12, 4]),
	        (-649/200, [-4, 1, 3, 12, 4]),
	        (-649/-200, [3, 4, 12, 4]),
	        ('0.3333', [0, 3, 3333]),
	        ('-0.3333', [-1, 1, 2, 3333]),
	        ('-5.25', [-6, 1, 3]),
	        ('5.25', [5, 4]),
	        ('0.3', [0, 3, 3]),
	        (0.1, [0, 10]),
	        ('-3.245', [-4, 1, 3, 12, 4]),
	    ],
	)
	def test_continued_fraction_real__valid_inputs__correct_elements_generated(self, x, elements):
		
		expected = elements

		assert list(continued_fraction_real(x)) == expected


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


class TestKthConvergent:

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
	def test_kth_convergent__invalid_elements__value_error_raised(self, elements, k):
		with pytest.raises(ValueError):
			kth_convergent(*elements, k=k)

	@pytest.mark.parametrize(
	    "elements, k, convergent",
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
	def test_kth_convergent__valid_elements__correct_convergent_returned(self, elements, k, convergent):
		
		expected = convergent

		assert kth_convergent(*elements, k=k) == expected
