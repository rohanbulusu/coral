
from inspect import signature
from collections.abc import Sequence
from itertools import combinations

from coralset import CoralSet, REALS, COMPLEX
from utils import typename, unique_choices


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

class ClosureError(ValueError):
	...

class AssociativityError(TypeError):
	...

class CommutativityError(TypeError):
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
		if not all(candidate.domain[0].has_element(sample) for sample in samples):
			raise TypeError(f'Not all sample elements are in the binary operation\'s domain')
		triples = list(combinations(samples, 3))
		for a, b, c in triples:
			if not candidate._func(candidate._func(a, b), c) == candidate._func(a, candidate._func(b, c)):
				return False
		return True
	
	@staticmethod
	def is_commutative(candidate, *samples):
		if not BinaryOperation.is_binary_operation(candidate):
			raise TypeError(f'Expected BinaryOperation, not {typename(candidate)}')
		if len(samples) < 2:
			raise ValueError('Expected at least two sample domain elements')
		if not all(candidate.domain[0].has_element(sample) for sample in samples):
			raise TypeError(f'Not all sample elements are in the binary operation\'s domain')
		pairs = list(combinations(samples, 2))
		for a, b in pairs:
			if not candidate._func(a, b) == candidate._func(b, a):
				return False
		return True

	def __init__(self, _func, left_domain, right_domain):
		super().__init__(_func, (left_domain, right_domain))
		self.left_domain = left_domain
		self.right_domain = right_domain
	
	def __call_(self, a, b):
		return super().__call__(a, b)


class AssociativeOperation(BinaryOperation):

	def __init__(self, _func, left_domain, right_domain):
		super().__init__(_func, left_domain, right_domain)
		self.cached_samples = set()
		self.num_samples = 0

	def __cache_sample(self, sample):
		self.cached_samples.add(sample)
		self.num_samples += 1

	def __call__(self, a, b):
		self.__cache_sample(a)
		self.__cache_sample(b)
		if self.num_samples >= 3:
			if not BinaryOperation.is_associative(self, *unique_choices(list(self.cached_samples), 3)):
				raise AssociativityError('Operation is not associative over the given domain')
		return super().__call__(a, b)


class CommutativeOperation(BinaryOperation):
	
	def __init__(self, _func, left_domain, right_domain):
		super().__init__(_func, left_domain, right_domain)
		self.cached_samples = set()
		self.num_samples = 0

	def __cache_sample(self, sample):
		self.cached_samples.add(sample)
		self.num_samples += 1

	def __call__(self, a, b):
		self.__cache_sample(a)
		self.__cache_sample(b)
		if self.num_samples >= 2:
			if not BinaryOperation.is_commutative(self, *unique_choices(list(self.cached_samples), 2)):
				raise CommutativityError('Operation is not commutative over the given domain')
		return super().__call__(a, b)


# alias for CommutativeOperation
class AbelianOperation(CommutativeOperation):
	...


# operation that's both associative and commutative
class AbelianGroupOperation(BinaryOperation):

	def __init__(self, _func, left_domain, right_domain):
		super().__init__(_func, left_domain, right_domain)
		self.cached_samples = set()
		self.num_samples = 0

	def __cache_sample(self, sample):
		self.cached_samples.add(sample)
		self.num_samples += 1

	def __call__(self, a, b):
		self.__cache_sample(a)
		self.__cache_sample(b)
		if self.num_samples >= 2:
			if not BinaryOperation.is_commutative(self, *unique_choices(list(self.cached_samples), 2)):
				raise CommutativityError('Operation is not commutative over the given domain')
		if self.num_samples >= 3:
			if not BinaryOperation.is_associative(self, *unique_choices(list(self.cached_samples), 3)):
				raise AssociativityError('Operation is not associative over the given domain')
		return super().__call__(a, b)





