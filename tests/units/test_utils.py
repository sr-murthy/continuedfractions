# -- IMPORTS --

# -- Standard libraries --

# -- 3rd party libraries --
import pytest

# -- Internal libraries --
from continuedfractions.utils import (
	NamedCallableProxy,
)


class TestNamedCallableProxy:

	@pytest.mark.parametrize(
	    """callable_,
	       name,
	       expected_callable_proxy""",
	    [
	    	# Case #1
	        (
	        	lambda x: x ** 2,
	        	"x |--> x^2",
	        	NamedCallableProxy(lambda x: x ** 2, name="x |--> x^2"),
	        ),
	        # Case #2
	        (
	        	lambda x: x ** 2,
	        	None,
	        	NamedCallableProxy(lambda x: x ** 2),
	        ),
	    ],
	)
	def test_NamedCallableProxy__creation_and_initialisation(
		self,
		callable_,
		name,
		expected_callable_proxy
	):
		expected = expected_callable_proxy

		# The received ``NamedCallableProxy`` object
		received = NamedCallableProxy(callable_, name=name)

		# Compare the received and expected objects
		assert received == expected

		# Compare the names
		assert received._name == expected._name

		# Assert the ``__repr__`` value - comparison with ``expected`` will
		# not work as it is a different object in memory compared to
		# ``received``
		assert received.__repr__()

		# Compare the outputs for ``__call__``
		assert received(1) == expected(1) == 1
		assert received(2) == expected(2) == 4
		assert received(3) == expected(3) == 9
