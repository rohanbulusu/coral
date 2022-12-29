
from collections.abc import Iterable

def typename(_obj):
	return _obj.__class__.__name__

def _generator_chain(*iterables):
	for i in iterables:
		yield from i

def chain(*iterators):
	if not all(isinstance(i, Iterable) for i in iterators):
		raise TypeError(f'Expected Iterable, not {typename(i)}')

	return tuple(_generator_chain(*iterators))

def zeros(n):
	if not isinstance(n, int):
		raise TypeError(f'Expected int, got {typename(n)}')
	if not n >= 0:
		raise ValueError(f'Expected length to be greater than 0, not {n}')
	return (0 for _ in range(n))

def ones(n):
	if not isinstance(n, int):
		raise TypeError(f'Expected int, got {typename(n)}')
	if not n >= 0:
		raise ValueError(f'Expected length to be greater than 0, not {n}')
	return [1 for _ in range(n)]


class _NumberMeta(type):

	def __instancecheck__(cls, instance):
		return isinstance(instance, (int, float, complex))

class Number(metaclass=_NumberMeta):
	...


class _HasSumMeta(type):

	def __instancecheck__(cls, instance):
		return '__add__' in instance.__class__.__dict__

class HasSum(metaclass=_HasSumMeta):
	...


class _HasProductMeta(type):

	def __instancecheck__(cls, instance):
		return '__mul__' in instance.__class__.__dict__

class HasProduct(metaclass=_HasProductMeta):
	...

