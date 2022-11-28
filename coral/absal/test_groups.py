
from pytest import raises

from coral.maps import PropertyError, addition_mod
from coral.coralset import CoralSet
from .groups import *


class TestGroup:

	def test_accepts_valid_groups(self):
		assert Group(CoralSet((0, 1, 2, 3)), 0, addition_mod(4))

	def test_checks_for_valid_identity(self):
		bad_Z3 = Group(CoralSet((0, 1, 2)), 1, addition_mod(3))
		assert bad_Z3(1, 2) != 2
		assert bad_Z3(0, 2) == 2


class TestZn:

	def test_has_proper_modulo(self):
		Z4 = Z_mod(4)
		assert Z4 == Group(CoralSet((0, 1, 2, 3)), 0, addition_mod(4))

	def test_has_proper_elements(self):
		Z5 = Z_mod(5)
		assert 0 in Z5
		assert 1 in Z5
		assert 2 in Z5
		assert 3 in Z5
		assert 4 in Z5
		assert 5 not in Z5




