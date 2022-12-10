
from pytest import fixture, raises

from .rings import *
from coral.coralset import CoralSet, REALS
from coral.maps import PropertyError, ClosedOperation, AbelianGroupOperation

@fixture
def R_addition():
	return AbelianGroupOperation(lambda a, b: a + b, lambda a, b: a - b, REALS)

@fixture
def R_multiplication():
	return AbelianGroupOperation(lambda a, b: a*b, lambda a, b: a/b, REALS)

@fixture
def R_ring(R_addition, R_multiplication):
	return Ring(REALS, R_addition, R_multiplication)


class TestRing:

	def test_only_accepts_abelian_group_addition(self, R_multiplication):
		with raises(PropertyError):
			bad_R_addition = ClosedOperation(lambda a, b: a + b, REALS)
			assert Ring(REALS, bad_R_addition, R_multiplication)

	def test_only_accepts_associative_multiplication(self, R_addition):
		with raises(PropertyError):
			bad_R_multiplication = ClosedOperation(lambda a, b: a*b, REALS)
			assert Ring(REALS, R_addition, bad_R_multiplication)

	def test_ring_addition(self, R_ring):
		assert R_ring.addition(1, 3) == R_ring.add(1, 3)
		assert R_ring.addition(5, -1) == R_ring.add(5, -1)

	def test_ring_multiplication(self, R_ring):
		assert R_ring.multiplication(1, 4) == R_ring.mul(1, 4)
		assert R_ring.multiplication(5, -3/2) == R_ring.mul(5, -3/2)



