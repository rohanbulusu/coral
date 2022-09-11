
from pytest import raises

from .vector import *


class TestVector:

	def test_vector_equality(self):
		assert Vector(1, 2, 3) == Vector(1, 2, 3)
		assert Vector(0) == Vector(0, 0, 0)

	def test_zero_vector_instantiation(self):
		assert Vector()
		assert Vector(0)
		assert Vector() == Vector(0)
		assert Vector(0).dim == 0
		assert Vector().dim == 0

	def test_accepts_only_numbers(self):
		assert Vector(0)
		assert Vector(1)
		assert Vector(0.1)
		assert Vector(1j)
		assert Vector(1 + 2j)
		with raises(TypeError):
			assert Vector([0])
		with raises(TypeError):
			assert Vector(Vector(1, 2, 3))

	def test_vector_addition(self):
		assert Vector(1, 2, 3) + Vector(0, 0, 0) == Vector(1, 2, 3)
		assert Vector(1, 2, 3) + Vector() == Vector(1, 2, 3)
		assert Vector(1, 2, 3) + Vector(1, 2, 3) == Vector(2, 4, 6)
		with raises(ValueError):
			assert Vector(1, 2) + Vector(1, 2, 3)

	def test_vector_subtraction(self):
		assert Vector(1, 2, 3) - Vector(0, 0, 0) == Vector(1, 2, 3)
		assert Vector(1, 2, 3) - Vector(1, 2, 3) == Vector(0)
		assert Vector(2, 4, 6) - Vector(1, 2, 3) == Vector(1, 2, 3)

	def test_vector_scalar_product(self):
		assert 2 * Vector(1, 2, 3) == Vector(1, 2, 3) * 2
		assert 2 * Vector(1, 2, 3) == Vector(2, 4, 6)
		assert 0 * Vector(1, 2, 3) == Vector(0)

	def test_vector_dot_product(self):
		assert Vector(1, 2, 3) * Vector(1, 1, 1) == 6
		assert Vector(0, 0, 0) * Vector(1, 2, 3) == 0
		assert Vector(0, 1) * Vector(1, 0) == 0
		assert Vector(3, 3) * Vector(3, 3) == 18
		with raises(ValueError):
			assert Vector(1, 2) * Vector(1, 2, 3)

	def test_vector_scalar_division(self):
		assert Vector(2, 4, 6) / 2 == Vector(1, 2, 3)
		assert Vector(1, 2, 3) / 1 == Vector(1, 2, 3)
		with raises(ZeroDivisionError):
			assert Vector(1, 2, 3) / 0


class TestVector2:

	def test_subclassing(self):
		assert issubclass(Vector2, Vector)

	def test_to_complex(self):
		assert complex(Vector2(1, 2)) == 1 + 2j
		assert complex(Vector2()) == 0 + 0j

