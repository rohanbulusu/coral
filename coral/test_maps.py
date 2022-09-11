
from pytest import raises

from maps import *


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
