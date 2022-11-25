
from pytest import raises

from .maps import *


class TestFunction:

	def test_accepts_lambdas(self):
		assert Function(lambda x: x**2, [REALS])

	def test_accepts_true_functions(self):
		def f(x):
			return x**2
		assert Function(f, [REALS])

	def test_accepts_arguments_in_domain(self):
		assert Function(lambda x: x**2, [REALS])(2) == 4

	def test_handles_multiple_arguments(self):
		assert Function(lambda x, y: x*y, [REALS, REALS])(3, 2) == 6
		assert Function(lambda x, y, z: x*y*z, [REALS, COMPLEX, REALS])(1, 1j, 1) == 1j

	def test_rejects_arguments_outside_domain(self):
		with raises(DomainError):
			assert Function(lambda x: x**2, [REALS])(1j) == -1

	def test_rejects_kwarg_inputs(self):
		with raises(TypeError):
			assert Function(lambda x: x, [REALS])(1, y=2) == 1


class TestAssociativeOperation:

	def test_addition_satisfies_associativity(self):
		real_addition = AssociativeOperation(lambda a, b: a + b, REALS)
		_ = real_addition(1, 2)
		_ = real_addition(2, 3)

	def test_division_fails_associativity(self):
		real_division = AssociativeOperation(lambda a, b: a / b, REALS)
		_ = real_division(1, 2)
		with raises(AssociativityError):
			_ = real_division(3, 4)
			_ = real_division(5, 6)


class TestCommutativeOperation:

	def test_addition_satisfies_commutativity(self):
		real_addition = CommutativeOperation(lambda a, b: a + b, REALS)
		_ = real_addition(1, 2)

	def test_subtraction_fails_commutativity(self):
		real_subtraction = CommutativeOperation(lambda a, b: a - b, REALS)
		with raises(CommutativityError):
			_ = real_subtraction(1, 2)


class TestAbelianOperation:

	def test_addition_is_abelian(self):
		real_addition = AbelianOperation(lambda a, b: a + b, REALS)
		_ = real_addition(1, 2)

	def test_subtraction_is_not_abelian(self):
		real_subtraction = AbelianOperation(lambda a, b: a - b, REALS)
		with raises(CommutativityError):
			_ = real_subtraction(1, 2)


class TestAbelianGroupOperation:

	def test_addition_is_abelian_group_operation(self):
		real_addition = AbelianGroupOperation(lambda a, b: a + b, REALS)
		_ = real_addition(1, 2)

	def test_subtraction_fails_commutativity(self):
		real_subtraction = AbelianGroupOperation(lambda a, b: a - b, REALS)
		with raises(CommutativityError):
			_ = real_subtraction(1, 2)

	def test_operation_fails_associativity(self):
		operation = AbelianGroupOperation(lambda a, b: 2*a + 2*b, REALS)
		_ = operation(1, 2)
		with raises(AssociativityError):
			_ = operation(3, 4)
			_ = operation(5, 6)



