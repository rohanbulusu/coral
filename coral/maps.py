
from inspect import signature
from collections.abc import Sequence

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
			if not domain.is_element(arg):
				raise DomainError(f'Expected element of {domain}, not {arg}')
		return self._func(*args)

