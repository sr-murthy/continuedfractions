# -- IMPORTS --

# -- Standard libraries --
import operator

from decimal import Decimal
from fractions import Fraction
from types import MappingProxyType

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.continuedfractions import (
	ContinuedFraction,
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


class TestContinuedFraction:

	@pytest.mark.parametrize(
	    "invalid_inputs",
	    [
	    	('not a number',),
	    	('-1 2',),
	    	('-1 + 2',),
	    	(None,),
	    	([-1, '2'],),
	    	(1, 2, 3,),
	    	(b'bytes of number',),
	    	([],),
	    	((1, 2, 3,)),
	    	(dict(a=1, b=2,)),
	    	(Fraction(1, -2), Decimal(3)),
	    	(Decimal(1), 2),
	    ],
	)
	def test_ContinuedFraction__creation_and_initialisation__invalid_inputs__value_error_raised(self, invalid_inputs):
		with pytest.raises(ValueError):
			ContinuedFraction(*invalid_inputs)

	@pytest.mark.parametrize(
	    """valid_inputs,
	       expected_fraction_obj,
	       expected_elements,
	       expected_order,
	       expected_convergents,
	       expected_ref_mediant""",
	    [
	    	# Case #1
	        (
	        	(3, 2,),
	        	Fraction(3, 2),
	        	(1, 2,),
	        	1,
	        	MappingProxyType({
	        		0: Fraction(1, 1),
	        		1: Fraction(3, 2)
	        	}),
	        	ContinuedFraction(4, 3)
	        ),
	        # Case #2
	        (
	        	('1.5',),
	        	Fraction(3, 2),
	        	(1, 2,),
	        	1,
	        	MappingProxyType({
	        		0: Fraction(1, 1),
	        		1: Fraction(3, 2)
	        	}),
	        	ContinuedFraction(4, 3)
	        ),
	        # Case #3
	        (
	        	('-5000',),
	        	Fraction(-5000),
	        	(-5000,),
	        	0,
	        	MappingProxyType({
	        		0: Fraction(-5000, 1)
	        	}),
	        	ContinuedFraction(-4999, 2)
	        ),
	        # Case #4
	        (
	        	('3.245',),
	        	Fraction(649, 200),
	        	(3, 4, 12, 4),
	        	3,
	        	MappingProxyType({
	        		0: Fraction(3, 1),
	        		1: Fraction(13, 4),
	        		2: Fraction(159, 49),
	        		3: Fraction(649, 200)
	        	}),
	        	ContinuedFraction(650, 201)
	        ),
	        # Case #5
	        (
	        	('-649/200',),
	        	Fraction(-649, 200),
	        	(-4, 1, 3, 12, 4),
				4,
				MappingProxyType({
					0: Fraction(-4, 1),
  	            	1: Fraction(-3, 1),
	              	2: Fraction(-13, 4),
	              	3: Fraction(-159, 49),
	              	4: Fraction(-649, 200)
				}),
				ContinuedFraction(-216, 67)
	        ),
	        # Case #6
	        (
	        	(-649, -200),
	        	Fraction(649, 200),
	        	(3, 4, 12, 4),
	        	3,
	        	MappingProxyType({
	        		0: Fraction(3, 1),
	        		1: Fraction(13, 4),
	        		2: Fraction(159, 49),
	        		3: Fraction(649, 200)
	        	}),
	        	ContinuedFraction(650, 201)
	        ),
	        # Case #7
	        (
	        	('0.3333',),
	        	Fraction(3333, 10000),
	        	(0, 3, 3333),
	        	2,
	        	MappingProxyType({
	        		0: Fraction(0, 1),
	        		1: Fraction(1, 3),
	        		2: Fraction(3333, 10000)
	        	}),
	        	ContinuedFraction(3334, 10001)
	        ),
	        # Case #8
	        (
	        	('-0.3333',),
	        	Fraction(-3333, 10000),
	        	(-1, 1, 2, 3333),
	        	3,
	        	MappingProxyType({
					0: Fraction(-1, 1),
	              	1: Fraction(0, 1),
	              	2: Fraction(-1, 3),
	              	3: Fraction(-3333, 10000)
	        	}),
	        	ContinuedFraction(-3332, 10001)
	        ),
	        # Case #9
	        (
	        	('-5.25',),
	        	Fraction(-21, 4),
	        	(-6, 1, 3),
	        	2,
	        	MappingProxyType({
	        		0: Fraction(-6, 1),
	        		1: Fraction(-5, 1),
	        		2: Fraction(-21, 4)
	        	}),
	        	ContinuedFraction(-4, 1)
	        ),
	        # Case #10
	        (
	        	('123456789',),
	        	Fraction(123456789, 1),
	        	(123456789,),
	        	0,
	        	MappingProxyType({
	        		0: Fraction(123456789, 1)
	        	}),
	        	ContinuedFraction(61728395, 1)
	        ),
	        # Case #11
	        (
	        	('0.3',),
	        	Fraction(3, 10),
	        	(0, 3, 3),
	        	2,
	        	MappingProxyType({
	        		0: Fraction(0, 1),
	        		1: Fraction(1, 3),
	        		2: Fraction(3, 10)	
	        	}),
	        	ContinuedFraction(4, 11)
	        ),
	        # Case #12
	        (
	        	(1, 10,),
	        	Fraction(1, 10),
	        	(0, 10),
	        	1,
	        	MappingProxyType({
	        		0: Fraction(0, 1),
	        		1: Fraction(1, 10)
	        	}),
	        	ContinuedFraction(2, 11)
	        ),
	        # Case #13
	        (
	        	('-3.245',),
	        	Fraction(-649, 200),
	        	(-4, 1, 3, 12, 4),
	        	4,
	        	MappingProxyType({
					0: Fraction(-4, 1),
              		1: Fraction(-3, 1),
					2: Fraction(-13, 4),
					3: Fraction(-159, 49),
					4: Fraction(-649, 200)
	        	}),
	        	ContinuedFraction(-216, 67)
	        ),
	        # Case #14
	        (
	        	(123456789,),
	        	Fraction(123456789, 1),
	        	(123456789,),
	        	0,
	        	MappingProxyType({
	        		0: Fraction(123456789, 1)
	        	}),
	        	ContinuedFraction(61728395, 1)
	        ),
	        # Case #15
	        (
	        	(1.5,),
	        	Fraction(3, 2),
	        	(1, 2,),
	        	1,
	        	MappingProxyType({
	        		0: Fraction(1, 1),
	        		1: Fraction(3, 2)
	        	}),
	        	ContinuedFraction(4, 3)
	        ),
	        # Case #16
	        (
	        	(-3, Fraction(4, 5)),
	        	Fraction(-15, 4),
	        	(-4, 4),
	        	1,
	        	MappingProxyType({
	        		0: Fraction(-4, 1),
	        		1: Fraction(-15, 4)
	        	}),
	        	ContinuedFraction(-14, 5)
	        ),
	        # Case #17
	        (
	        	(Decimal('3.245'),),
	        	Fraction(649, 200),
	        	(3, 4, 12, 4),
	        	3,
	        	MappingProxyType({
	        		0: Fraction(3, 1),
	        		1: Fraction(13, 4),
	        		2: Fraction(159, 49),
	        		3: Fraction(649, 200)
	        	}),
	        	ContinuedFraction(650, 201)
	        )
	    ],
	)
	def test_ContinuedFraction__creation_and_initialisation__valid_inputs__object_correctly_created_and_initialised(
		self,
		valid_inputs,
		expected_fraction_obj,
		expected_elements,
		expected_order,
		expected_convergents,
		expected_ref_mediant
	):
		expected = expected_fraction_obj

		# The received ``ContinuedFraction`` object
		received = ContinuedFraction(*valid_inputs)

		# Compare the received and expected objects AS ``fractions.Fraction``
		# objects
		assert received == expected

		# Compare the element sequences
		assert received.elements == expected_elements

		# Compare the orders
		assert received.order == expected_order

		# Compare the convergents
		assert received.convergents == expected_convergents

		# Compare the segments
		assert all(
			received.segment(k) == ContinuedFraction(expected_convergents[k])
			for k in range(received.order + 1)
		)

		# Compare the remainders
		assert all(
			received.remainder(k) == ContinuedFraction.from_elements(*expected_elements[k:])
			for k in range(received.order + 1)
		)

		assert received.mediant(1) == expected_ref_mediant

	def test_ContinuedFraction__operations(self):
		f1 = ContinuedFraction(649, 200)
		f2 = ContinuedFraction(-649, 200)

		assert f1 + f2 == ContinuedFraction(0, 1)

		assert f1.__radd__(f2) == f2.__radd__(f1)

		assert f1 - f2 == ContinuedFraction(649, 100)

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

		assert abs(f2) == f1
