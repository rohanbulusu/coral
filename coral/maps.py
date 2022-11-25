
from inspect import signature
from collections.abc import Sequence
import itertools

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

class PropertyError(TypeError):
	...

class ClosureError(PropertyError):
	...

class AssociativityError(PropertyError):
	...

class CommutativityError(PropertyError):
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


class ClosedOperation(Function):

	def __init__(self, _func, domain):
		if not isinstance(domain, CoralSet):
			raise TypeError(f'Expected CoralSet, not {typename(domain)}')
		super().__init__(_func, (domain, domain))
		self.domain = domain
		self.cached_samples = set()
		self.num_samples = 0
		self.indempotents = set()

	@property
	def is_indempotent(self):
		return self.num_samples == len(self.indempotents)
		
	def _cache_sample(self, sample):
		self.cached_samples.add(sample)
		self.num_samples = len(self.cached_samples)

	def __call__(self, a, b):
		self._cache_sample(a)
		self._cache_sample(b)
		result = super().__call__(a, b)
		if not self.domain.has_element(result):
			raise ClosureError(f'Operation output {result} is not in the target {self.domain}')
		if result == a:
			self.indempotents.add(a)
		if result == b:
			self.indempotents.add(b)
		return result

	def is_associative(self, samples):
		if not all(self.domain.has_element(sample) for sample in samples):
			raise DomainError(f'Not all sample elements are in the binary operation\'s domain')
		for a, b, c in itertools.permutations(samples, 3):
			if not self._func(self._func(a, b), c) == self._func(a, self._func(b, c)):
				return False
		return True

	def is_commutative(self, samples):
		if not all(self.domain.has_element(sample) for sample in samples):
			raise DomainError(f'Not all sample elements are in the binary operation\'s domain')
		for a, b in itertools.permutations(samples, 2):
			if not self._func(a, b) == self._func(b, a):
				return False
		return True


class AssociativeOperation(ClosedOperation):

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 3:
			if not self.is_associative(self.cached_samples):
				raise AssociativityError('Operation is not associative over the given domain')
		return result


class CommutativeOperation(ClosedOperation):

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 2:
			if not self.is_commutative(self.cached_samples):
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
			if not self.is_associative(self.cached_samples):
				raise AssociativityError('Operation is not associative over the given domain')
		if self.num_samples >= 2:
			if not self.is_commutative(self.cached_samples):
				raise CommutativityError('Operation is not commutative over the given domain')
		return result


class LatinSquareOperation(ClosedOperation):

	def satisfies_latin_square_property(self, samples):
		for a, b in itertools.permutations(samples, 2):
			left_exists = any(self._func(s, a) == b for s in samples)
			right_exists = any(self._func(a, s) == b for s in samples)
			if left_exists and right_exists:
				return True
		return False
	
	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 2:
			if not self.satisfies_latin_square_property(self.cached_samples):
				raise PropertyError('Operation fails to satisfy the Latin Square Property')
		return result


