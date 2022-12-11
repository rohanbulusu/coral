
from pytest import fixture, raises, skip

from .rings import *
from coral.coralset import CoralSet, INTEGERS, EVEN_INTEGERS, REALS
from coral.maps import PropertyError, ClosedOperation, AbelianGroupOperation

@fixture
def R_addition():
	return AbelianGroupOperation(lambda a, b: a + b, lambda a, b: a - b, REALS)

@fixture
def R_multiplication():
	return AbelianGroupOperation(lambda a, b: a*b, lambda a, b: a/b, REALS)

@fixture
def R_ring(R_addition, R_multiplication):
	return Ring(REALS, R_addition, 0, R_multiplication)

@fixture
def Z_ring(R_addition, R_multiplication):
	return Ring(INTEGERS, R_addition, 0, R_multiplication)


class TestRing:

	def test_only_accepts_abelian_group_addition(self, R_multiplication):
		with raises(PropertyError):
			bad_R_addition = ClosedOperation(lambda a, b: a + b, REALS)
			assert Ring(REALS, bad_R_addition, 0, R_multiplication)

	def test_only_accepts_associative_multiplication(self, R_addition):
		with raises(PropertyError):
			bad_R_multiplication = ClosedOperation(lambda a, b: a*b, REALS)
			assert Ring(REALS, R_addition, 1, bad_R_multiplication)

	def test_ring_addition(self, R_ring):
		assert R_ring.addition(1, 3) == R_ring.add(1, 3)
		assert R_ring.addition(5, -1) == R_ring.add(5, -1)

	def test_ring_multiplication(self, R_ring):
		assert R_ring.multiplication(1, 4) == R_ring.mul(1, 4)
		assert R_ring.multiplication(5, -3/2) == R_ring.mul(5, -3/2)


class TestIdeal:

	def test_requires_specification_of_cset(self):
		assert Ideal(EVEN_INTEGERS)
		with raises(TypeError):
			assert Ideal({1, 2, 3, 4, 5})

	def test_is_ideal_of_parent_ring(self, Z_ring, R_addition, R_multiplication):
		true_ideal = Ideal(EVEN_INTEGERS)
		assert true_ideal.is_ideal_of(Z_ring)
		whole_ring_ideal = Ideal(Z_ring.cset)
		assert whole_ring_ideal.is_ideal_of(Z_ring)

		partial_ideal = Ideal(CoralSet((1, 2, 3)))
		assert not partial_ideal.is_ideal_of(Z_ring)
		full_ideal = Ideal(CoralSet((-1, 0, 1)))
		ring = Ring(CoralSet((-1, 0, 1)), R_addition, 0, R_multiplication)
		assert full_ideal.is_ideal_of(ring)



