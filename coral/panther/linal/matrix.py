
from collections.abc import Sequence

from coral.utils import typename, Number, HasSum, HasProduct
from .vector import Vector


class _MatrixDimension:

	def __init__(self, num_rows, num_cols):
		self.num_rows = num_rows
		self.num_cols = num_cols
		self.is_zero = num_rows == 0 and num_cols == 0

	def __repr__(self):
		return f'({self.num_rows}, {self.num_cols})'


class Matrix:

	def __init__(self, *rows):
		if not all(isinstance(row, Sequence) for row in rows):
			raise TypeError('Expected all Matrix rows to be Sequences')
		if not all(all(isinstance(item, HasSum) for item in row) for row in rows):
			raise TypeError('Expected all Matrix items to be equipped with an endomorphic sum')
		if not all(all(isinstance(item, HasProduct) for item in row) for row in rows):
			raise TypeError('Expected all Matrix items to be equipped with an endomorphic product')
		self.rows = rows
		self.cols = tuple([tuple([row[i] for row in rows]) for i in range(len(rows[0]))])
		self.dim = _MatrixDimension(len(self.rows), len(self.cols))

	def __repr__(self):
		return f'{typename(self)}{self.rows}'

	def copy(self):
		return self.__class__(*self.rows)

	def __neg__(self):
		return self.__class__(*[[-item for item in row] for row in rows])

	def __add__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(f'Expected Matrix, not {typename(other)}')
		if self.dim.is_zero:
			return other.copy()
		if other.dim.is_zero:
			return self.copy()
		return self.__class__(*[[c + o for c, o in zip(c_row, o_row)] for c_row, o_row in zip(self.rows, other.rows)])

	def __sub__(self, other):
		if not isinstance(other, Matrix):
			raise TypeError(f'Expected Matrix, not {typename(other)}')
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, Number):
			return self.__class__(*[[other*item for item in row] for row in self.rows])
		if isinstance(other, Vector):
			return self.__class__(*[[v*item for v, item in zip(other.components, row)] for row in rows])
		if isinstance(other, Matrix):
			return self.__class__(*[
				[sum(s*o for s, o in zip(row, col)) for col in other.cols]
				for row in self.rows
			])
		raise TypeError(f'Expected Number, Vector, or Matrix, not {typename(other)}')

	def __rmul__(self, other):
		return other * self

	def __truediv__(self, other):
		if not isinstance(other, Number):
			raise TypeError(f'Expected Number, not {typename(other)}')
		return (1 / other) * self





