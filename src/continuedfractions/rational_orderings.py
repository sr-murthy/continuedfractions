__all__ = [
	'farey_sequence',
]


# -- IMPORTS --

# -- Standard libraries --
import functools
import sys

from pathlib import Path
from typing import Generator

# -- 3rd party libraries --

# -- Internal libraries --
sys.path.insert(0, str(Path(__file__).parent.parent))

from continuedfractions.continuedfraction import ContinuedFraction


def _farey_sequence(n: int) -> Generator[ContinuedFraction, None, None]:
	"""Generates the sequence of rational numbers forming the Farey sequence of order :math:`n`.

	Parameters
	----------
	n : int:
		The order of the Farey sequence.

	Yields
	-------
	ContinuedFraction
		A sequence of ``ContinuedFraction`` instances representing the elements
		of the Farey sequence of order :math:`n`.
	"""


@functools.cache
def farey_sequence(n: int) -> tuple[ContinuedFraction]:
	"""Returns a tuple of rational numbers forming the Farey sequence of order :math:`n`.

	This is a cached wrapper for :py:func:`~continuedfractions.rational_orderings._farey_sequence`
	to provide a return value for any given value of :math:`n`.

	The `Farey sequence <https://en.wikipedia.org/wiki/Farey_sequence>`_
	:math:`F_n` of order :math:`n` is an (ordered) sequence of rational numbers
	which is defined recursively as follows:

	.. math::

	   \\begin{align}
	   F_1 &= \\left(\\frac{0}{1}, \\frac{1}{1}\\right) \\\\
	   F_k &= \\left(\\frac{a}{b}\\right) \\text{ s.t. } (a, b) = 1 \\text{ and } b \\leq n,
	          \\hskip{3em} k \\geq 2
	   \\end{align}

	The restriction :math:`(a, b) = 1` (meaning :math:`a` and :math:`b` must
	be coprime) on the numerators and denominators of the fractions in
	:math:`F_n`, combined with :math:`b \\leq n`, means that for each
	:math:`b \\leq n` it contains exactly :math:`\\phi(b)`` fractions of the
	form :math:`\\frac{a}{b}` where :math:`(a, b) = 1`.

	This means that the number of elements :math:`N(n)` in :math:`F_n` is given by:

	.. math::

	   N(n) = 1 + \\phi(1) + \\phi(2) + \\cdots + \\phi(n) = 1 + \\sum_{k = 1}^n \\phi(k)

	where :math:`phi(k)` is `Euler's totient function <https://en.wikipedia.org/wiki/Euler%27s_totient_function>`_.

	The first five Farey sequences are:

	.. math::

	   \\begin{align}
	   F_1 &= \\left( \\frac{0}{1}, \\frac{1}{1} \\right) \\\\
	   F_2 &= \\left( \\frac{0}{1}, \\frac{1}{2}, \\frac{1}{1} \\right) \\\\
	   F_3 &= \\left( \\frac{0}{1}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{1}{1} \\right) \\\\
	   F_4 &= \\left( \\frac{0}{1}, \\frac{1}{4}, \\frac{1}{3}, \\frac{1}{2}, \\frac{2}{3}, \\frac{3}{4}, \\frac{1}{1} \\right) \\\\
	   F_5 &= \\left( \\frac{0}{1}, \\frac{1}{5}, \\frac{1}{4}, \\frac{1}{3}, \\frac{2}{5}, \\frac{1}{2}, \\frac{3}{5}, \\frac{2}{3}, \\frac{3}{4}, \\frac{4}{5}, \\frac{1}{1} \\right)
	   \\end{align}

	Farey sequences have quite interesting properties and relations, as
	described `here <https://en.wikipedia.org/wiki/Farey_sequence>`_.

	Parameters
	----------
	n : int:
		The order of the Farey sequence.

	Returns
	-------
	tuple[ContinuedFraction]
		A :py:class:`tuple` of ``ContinuedFraction`` instances representing the
		elements of the Farey sequence of order :math:`n`.
	"""
	raise NotImplementedError
