# -- IMPORTS --

# -- Standard libraries --
from decimal import Decimal
from fractions import Fraction
from types import MappingProxyType

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.continuedfraction import (
	ContinuedFraction,
)


class TestContinuedFraction:

	@pytest.mark.parametrize(
	    "invalid_inputs",
	    [
	    	('not a number',),
	    	('-1 2',),
	    	(1, float("nan")),
	    	('-1 + 2',),
	    	(1, 0),
	    	(-1, Fraction(0, 1)),
	    	(None,),
	    	([-1, '2'],),
	    	(1, 2, 3,),
	    	(b'bytes of number',),
	    	([],),
	    	((1, 2, 3,)),
	    	(dict(a=1, b=2,)),
	    	(-2, .3),
	    	(Fraction(1, -2), Decimal(3)),
	    	(Decimal('-1'), 2),
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
	       expected_ref_right_order1_mediant,
	       expected_float_value""",
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
	        	ContinuedFraction(4, 3),
	        	3 / 2
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
	        	ContinuedFraction(4, 3),
	        	3 / 2
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
	        	ContinuedFraction(-4999, 2),
	        	-5000.0
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
	        	ContinuedFraction(650, 201),
	        	3.245

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
				ContinuedFraction(-216, 67),
				-3.245
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
	        	ContinuedFraction(650, 201),
	        	3.245
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
	        	ContinuedFraction(3334, 10001),
	        	0.3333
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
	        	ContinuedFraction(-3332, 10001),
	        	-0.3333
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
	        	ContinuedFraction(-4, 1),
	        	-5.25
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
	        	ContinuedFraction(61728395, 1),
	        	123456789.0
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
	        	ContinuedFraction(4, 11),
	        	0.3
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
	        	ContinuedFraction(2, 11),
	        	0.1
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
	        	ContinuedFraction(-216, 67),
	        	-3.245
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
	        	ContinuedFraction(61728395, 1),
	        	123456789.0
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
	        	ContinuedFraction(4, 3),
	        	1.5
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
	        	ContinuedFraction(-14, 5),
	        	-3.75
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
	        	ContinuedFraction(650, 201),
	        	3.245
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
		expected_ref_right_order1_mediant,
		expected_float_value
	):
		expected = expected_fraction_obj

		# The received ``ContinuedFraction`` object
		received = ContinuedFraction(*valid_inputs)

		# Compare the received and expected objects AS ``fractions.Fraction``
		# objects
		assert received == expected

		# Compare the float values
		assert received.as_float() == expected.numerator / expected.denominator

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

		assert received.mediant(1, dir='right', k=1) == expected_ref_right_order1_mediant

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
	def test_right_mediant__two_fractions__correct_mediant_returned(self, cf1, cf2, k, expected_right_mediant):
	
		assert cf1.mediant(cf2, dir='right', k=k) == expected_right_mediant

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
	def test_left_mediant__two_fractions__correct_mediant_returned(self, cf1, cf2, k, expected_left_mediant):
	
		assert cf1.mediant(cf2, dir='left', k=k) == expected_left_mediant

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

		assert -f1 == ContinuedFraction(-f1.numerator, f1.denominator) == ContinuedFraction(Fraction(-f1))

		assert abs(f2) == f1
