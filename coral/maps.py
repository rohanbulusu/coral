
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

	def __init__(self, _func, input_domains):
		if not callable(_func):
			raise TypeError(f'Expected Callable, not {typename(_func)}')
		if has_kwargs(_func):
			raise ValueError(f'Did not expect kwarg parameters to function')
		if not (isinstance(input_domains, Sequence) and all(isinstance(d, CoralSet) for d in input_domains)):
			raise TypeError(f'Expected Sequence of CoralSets, not {typename(_func)}')
		if not num_args(_func) == len(input_domains):
			raise TypeError(f'Must specify input domains to the proper number of dimensions')
		self._func = _func
		self.input_domains = tuple(input_domains)

	def __call__(self, *args):
		for arg, domain in zip(args, self.input_domains):
			if not domain.has_element(arg):
				raise DomainError(f'Expected element of {domain}, not {arg}')
		return self._func(*args)


class BinaryOperation(Function):

	def __init__(self, _func, left_domain, right_domain):
		super().__init__(_func, (left_domain, right_domain))
		self.left_domain = left_domain
		self.right_domain = right_domain
	
	def __call__(self, a, b):
		return super().__call__(a, b)


class ClosedOperation(Function):

	def __init__(self, _func, domain):
		if not isinstance(domain, CoralSet):
			raise TypeError(f'Expected CoralSet, not {typename(domain)}')
		super().__init__(_func, (domain, domain))
		self.domain = domain
		self.cached_samples = set()
		self.num_samples = 0
		
	def _cache_sample(self, sample):
		self.cached_samples.add(sample)
		self.num_samples += 1

	def __call__(self, a, b):
		self._cache_sample(a)
		self._cache_sample(b)
		result = super().__call__(a, b)
		if not self.domain.has_element(result):
			raise ClosureError(f'Operation output {result} is not in the target {self.domain}')
		return result

	def is_associative(self, a, b, c):
		if not all(self.domain.has_element(sample) for sample in (a, b, c)):
			raise DomainError(f'Not all sample elements are in the binary operation\'s domain')
		if not self._func(self._func(a, b), c) == self._func(a, self._func(b, c)):
			return False
		return True

	def is_commutative(self, a, b):
		if not all(self.domain.has_element(sample) for sample in (a, b)):
			raise DomainError(f'Not all sample elements are in the binary operation\'s domain')
		if not self._func(a, b) == self._func(b, a):
			return False
		return True


class AssociativeOperation(ClosedOperation):

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 3:
			if not self.is_associative(*unique_choices(list(self.cached_samples), 3)):
				raise AssociativityError('Operation is not associative over the given domain')
		return result


class CommutativeOperation(ClosedOperation):

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 2:
			if not self.is_commutative(*unique_choices(list(self.cached_samples), 2)):
				raise CommutativityError('Operation is not commutative over the given domain')
		return result


# alias for CommutativeOperation
class AbelianOperation(CommutativeOperation):
	...


# operation that's both associative and commutative
class AbelianGroupOperation(ClosedOperation):

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 3:
			if not self.is_associative(*unique_choices(list(self.cached_samples), 3)):
				raise AssociativityError('Operation is not associative over the given domain')
		if self.num_samples >= 2:
			if not self.is_commutative(*unique_choices(list(self.cached_samples), 2)):
				raise CommutativityError('Operation is not commutative over the given domain')
		return result


class LatinSquareOperation(ClosedOperation):
	...


