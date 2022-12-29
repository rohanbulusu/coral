
from coral.utils import typename, zeros, Number, HasSum, HasProduct


class Vector:

	def __init__(self, *components):
		if not all(isinstance(c, HasSum) for c in components):
			raise ValueError('Expected all Vector components to be equipped with an endomorphic sum')
		if not all(isinstance(c, HasProduct) for c in components):
			raise ValueError('Expected all Vector components to be equipped with an endomorphic product')
		self.components = components
		self.dim = 0 if all(c == 0 for c in components) else len(components)
		self.norm = sum([c**2 for c in components])**0.5

	def __repr__(self):
		return f'{typename(self)}{self.components}'

	def copy(self):
		return self.__class__(*self.components)

	def pad_to(self, length):
		if not isinstance(length, int):
			raise TypeError(f'Expected int, not {typename(length)}')
		if not length >= self.dim:
			raise ValueError(f'Expected padded length to be greater than current dim of {self.dim}')
		num_padded_zeros = max(length - self.dim, 0)
		return self.__class__(*self.components, *zeros(num_padded_zeros))

	def __eq__(self, other):
		if not isinstance(other, Vector):
			return False
		if self.dim == 0:
			return other.dim == 0
		return self.components == other.components

	def __neg__(self):
		return self.__class__(*[-c for c in self.components])

	def __add__(self, other):
		if not isinstance(other, Vector):
			raise TypeError(f'Expected {typename(self)}, not {typename(other)}')
		if self.dim == 0:
			return other.copy()
		if other.dim == 0:
			return self.copy()
		if self.dim != other.dim:
			raise ValueError(f'Expected Vectors of the same dimension, not {self.dim} and {other.dim}')
		return self.__class__(*[c + o for c, o in zip(self.components, other.components)])

	def __sub__(self, other):
		if not isinstance(other, Vector):
			raise TypeError(f'Expected {typename(self)}, not {typename(other)}')
		return self + (-other)

	def __mul__(self, other):
		if isinstance(other, Number):
			return self.__class__(*[other*c for c in self.components])
		if isinstance(other, Vector):
			if self.dim == 0 or other.dim == 0:
				return 0
			if self.dim != other.dim:
				raise ValueError(f'Expected Vectors of the same dimension, not {self.dim} and {other.dim}')
			return sum(c*o for c, o in zip(self.components, other.components))
		raise TypeError(f'Expected {typename(self)}, not {typename(other)}')

	def __rmul__(self, other):
		return self * other

	def __truediv__(self, other):
		if not isinstance(other, Number):
			raise TypeError(f'Expected Number, not {typename(other)}')
		return (1 / other) * self

	def __getitem__(self, index):
		if not isinstance(index, int):
			raise TypeError(f'Expected int, not {typename(index)}')
		if self.dim == 0:
			return 0
		return self.components[index]

	@staticmethod
	def sum(*summands):
		total = Vector()
		for summand in summands:
			total = total + summand
		return total

	@staticmethod
	def average(*vectors):
		if len(vectors) == 0:
			raise ValueError('Expected Vectors, recieved no arguments')
		total = Vector.sum(*vectors)
		return total / len(vectors)


class Vector2(Vector):

	def __init__(self, x=0, y=0):
		super().__init__(x, y)
		self.__x = x
		self.__y = y

	@property
	def x(self):
		return self.x

	@property
	def y(self):
		return self.y

	def __complex__(self):
		return complex(self.__x, self.__y)

