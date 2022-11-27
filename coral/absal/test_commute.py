
from pytest import raises, fixture

from cmath import log as complex_log
from cmath import sqrt as complex_sqrt

from coral.coralset import REALS, POSITIVE_REALS, COMPLEX
from coral.maps import PropertyError, ClosureError, ClosedOperation, CommutativeOperation, AbelianGroupOperation
from .commute import *


@fixture
def addition():
	return AbelianGroupOperation(lambda a, b: a + b, REALS)

@fixture
def commutative_only():
	return CommutativeOperation(lambda a, b: 2*a + 2*b, REALS)

@fixture
def positive_division():
	return ClosedOperation(lambda a, b: a / b, POSITIVE_REALS)


class TestMagma:

	def test_reals_over_addition_satisfies_magma_axioms(self, addition):
		magma = Magma(REALS, addition)
		assert magma(1, 2) == 3
		assert magma(3, 4) == 7

	def test_reals_over_division_satisfies_magma_axioms(self, positive_division):
		magma = Magma(REALS, positive_division)
		assert magma(4, 2) == 2
		assert magma(9, 3) == 3

	def test_complex_numbers_over_log_satisfies_magma_axioms(self):
		log = ClosedOperation(lambda a, b: complex_log(a, b), COMPLEX)
		magma = Magma(COMPLEX, log)
		assert magma(2 + 4j, 1 + 3j) == complex_log(2 + 4j, 1 + 3j)
		assert magma(100, 10) == 2

	def test_reals_over_square_root_fails_axioms(self):
		sqrt = ClosedOperation(lambda a, b: complex_sqrt(a + b), REALS)
		magma = Magma(REALS, sqrt)
		assert magma(95, 5) == 10
		with raises(ClosureError):
			assert magma(-1, 0) == 1j


class TestUnitalMagma:

	def test_umagma_is_magma(self, addition):
		assert issubclass(UnitalMagma, Magma)
		assert isinstance(UnitalMagma(REALS, 0, addition), Magma)

	def test_reals_over_addition_has_identity(self, addition):
		umagma = UnitalMagma(REALS, 0, addition)
		assert umagma(0, 12) == 12
		assert umagma(12, 0) == 12

	def test_reals_over_division_lacks_identity(self, positive_division):
		umagma = UnitalMagma(POSITIVE_REALS, 1, positive_division)
		with raises(PropertyError):
			assert umagma(2, 1) == 2


class TestMonoid:

	def test_monoid_is_unital_magma(self, addition):
		assert issubclass(Monoid, UnitalMagma)
		assert issubclass(Monoid, Magma)
		assert isinstance(Monoid(REALS, 0, addition), UnitalMagma)
		assert isinstance(Monoid(REALS, 0, addition), Magma)

	def test_non_associative_operation_fails_monoid_axioms(self, commutative_only):
		with raises(TypeError):
			_ = Monoid(REALS, 0, commutative_only)

	def test_reals_over_addition_satisfies_monoid_axioms(self, addition):
		monoid = Monoid(REALS, 0, addition)
		assert monoid(1, 2) == 3
		assert monoid(3, 4) == 7


class TestSemigroup:

	def test_semigroup_is_magma(self, addition):
		assert issubclass(Semigroup, Magma)
		assert isinstance(Semigroup(REALS, addition), Magma)

	def test_non_associative_operation_fails_semigroup_axioms(self, commutative_only):
		with raises(TypeError):
			_ = Semigroup(REALS, commutative_only)

	def test_reals_over_addition_satisfies_semigroup_axioms(self, addition):
		semi = Semigroup(REALS, addition)
		assert semi(1, 2) == 3
		assert semi(3, 4) == 7


class TestQuasigroup:

	def test_quasigroup_is_magma(self, addition):
		assert issubclass(Quasigroup, Magma)
		assert isinstance(Quasigroup(REALS, addition), Magma)

	def test_non_latin_square_operation_fails_quasigroup_axioms(self, positive_division):
		with raises(TypeError):
			_ = Quasigroup(REALS, positive_division)

	def test_reals_over_addition_satisfies_semigroup_axioms(self, addition):
		quasi = Quasigroup(REALS, addition)
		assert quasi(1, 2) == 3
		assert quasi(3, 4) == 7


class TestLoop:

	def test_loop_is_unital_magma(self, addition):
		assert issubclass(Loop, UnitalMagma)
		assert issubclass(Loop, Magma)
		assert isinstance(Loop(REALS, 0, addition), UnitalMagma)
		assert isinstance(Loop(REALS, 0, addition), Magma)

	def test_non_latin_square_operation_fails_loop_axioms(self, positive_division):
		with raises(TypeError):
			_ = Loop(REALS, 0, positive_division)

	def test_reals_over_addition_satisfies_loop_axioms(self, addition):
		loop = Loop(REALS, 0, addition)
		assert loop(1, 2) == 3
		assert loop(3, 5) == 8

