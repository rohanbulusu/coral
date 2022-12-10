
from pytest import fixture, raises

from coral.maps import PropertyError, AbelianGroupOperation, addition_mod, REALS
from coral.coralset import CoralSet
from .groups import *


@fixture
def R_addition():
	return AbelianGroupOperation(lambda a, b: a + b, lambda a, b: a - b, REALS)

@fixture
def R_multiplication():
	return AbelianGroupOperation(lambda a, b: a*b, lambda a, b: a/b, REALS)

@fixture
def R_additive_group(R_addition):
	return Group(REALS, 0, R_addition)

@fixture
def R_multiplicative_group(R_multiplication):
	return Group(REALS, 1, R_multiplication)


class TestGroup:

	def test_accepts_valid_groups(self):
		assert Group(CoralSet((0, 1, 2, 3)), 0, addition_mod(4))

	def test_checks_for_valid_identity(self):
		with raises(ValueError):
			bad_Z3 = Group(CoralSet((0, 1, 2)), 1, addition_mod(3))

	def test_is_subgroup(self, R_additive_group, R_multiplicative_group):
		assert not R_additive_group.is_subgroup(R_multiplicative_group)
		assert Z_mod(50).is_subgroup(R_additive_group)
		assert Z_mod(3).is_subgroup(Z_mod(30))

	def test_has_subgroup(self, R_additive_group):
		assert not Z_mod(3).has_subgroup(Z_mod(30))
		assert R_additive_group.has_subgroup(Z_mod(40))



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




