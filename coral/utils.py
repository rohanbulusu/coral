
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

def unique_choices(samples, num_choices):
	if not isinstance(samples, Iterable):
		raise TypeError(f'Cannot select from {typename(samples)}')
	if num_choices > len(samples):
		raise ValueError(f'Cannot select {num_choices} item(s) from a {len(samples)}-element sequence')
	if num_choices == len(samples):
		return tuple(samples)
	choices = [samples[0]]
	while len(choices) != num_choices:
		choices.append(samples[len(choices)])
	return choices


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

