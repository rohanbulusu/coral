
from inspect import signature
from collections.abc import Sequence
from itertools import combinations

from coralset import CoralSet, REALS, COMPLEX
from utils import typename


def has_kwargs(_func):
	if not callable(_func):
		raise TypeError(f'Expected Callable, not {typename(_func)}')
	return '=' in str(signature(_func))


def num_kwargs(_func):
	if not callable(_func):
		raise TypeError(f'Expected Callable, not {typename(_func)}')
	return str(signature(_func)).count('=')


def num_args(_func):
	if not callable(_func):
		raise TypeError(f'Expected Callable, not {typename(_func)}')
	return len(signature(_func).parameters) - num_kwargs(_func)


class DomainError(ValueError):
	...


class Function:

	def __init__(self, _func, domain):
		if not callable(_func):
			raise TypeError(f'Expected Callable, not {typename(_func)}')
		if has_kwargs(_func):
			raise ValueError(f'Did not expect kwarg parameters to function')
		if not isinstance(domain, Sequence):
			raise TypeError(f'Expected Sequence of CoralSets, not {typename(_func)}')
		if not num_args(_func) == len(domain):
			raise TypeError(f'Must specify domain to the proper number of dimensions')
		self._func = _func
		self.domain = tuple(domain)

	def __call__(self, *args):
		for arg, domain in zip(args, self.domain):
			if not domain.has_element(arg):
				raise DomainError(f'Expected element of {domain}, not {arg}')
		return self._func(*args)


class BinaryOperation(Function):

	@staticmethod
	def is_binary_operation(candidate):
		if not isinstance(candidate, Function):
			return False
		if num_args(candidate._func) != 2:
			return False
		if candidate.domain[0] != candidate.domain[1]:
			return False
		return True
	
	# TODO: Test this method
	@staticmethod
	def is_associative(candidate, *samples):
		if not BinaryOperation.is_binary_operation(candidate):
			return False
		if len(samples) < 3:
			raise ValueError('Expected at least three sample domain elements')
		if not all(isinstance(sample, candidate.domain[0]) for sample in samples):
			raise TypeError(f'Not all sample elements are in the binary operation\'s domain')
		triples = list(combinations(samples, 3))
		for a, b, c in triples:
			if not candidate(candidate(a, b), c) == candidate(a, candidate(b, c)):
				return False
		return True
	
	@staticmethod
	def is_commutative(candidate, *samples):
		if not BinaryOPeration.is_binary_operation(candidate):
			raise TypeError(f'Expected BinaryOperation, not {typename(candidate)}')
		if len(samples) < 2:
			raise ValueError('Expected at least two sample domain elements')
		if not all(isinstance(sample, candidate.domain[0]) for sample in samples):
			raise TypeError(f'Not all sample elements are in the binary operation\'s domain')
		pairs = list(combinations(samples, 2))
		for a, b in pairs:
			if not candidate(a, b) == candidate(b, c):
				return False
		return True

	def __init__(self, _func, left_domain, right_domain):
		super().__init__(self, _func, (left_domain, right_domain))
		self.left_domain = left_domain
		self.right_domain = right_domain
	
	def __call_(self, a, b):
		return super().__call__(a, b)


