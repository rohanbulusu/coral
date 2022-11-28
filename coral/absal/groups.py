
from .commute import Monoid
from coral.utils import typename
from coral.coralset import CoralSet
from coral.maps import InvertibleOperation, addition_mod


class GroupOperation(InvertibleOperation):

	ASSOCIATIVE = True

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 3:
			if not self.is_associative(self.cached_samples):
				raise AssociativityError('Operation is not associative over the given domain')
		return result

	@classmethod
	def from_invertible(cls, invertible_operation):
		if not isinstance(invertible_operation, InvertibleOperation):
			raise TypeError('Must provide an invertible operation to define a group operation in this way')
		return GroupOperation(invertible_operation._func, invertible_operation._inverse, invertible_operation.domain)


class AbelianGroupOperation(GroupOperation):

	COMMUTATIVE = True

	def __call__(self, a, b):
		result = super().__call__(a, b)
		if self.num_samples >= 2:
			if not self.is_commutative(self.cached_samples):
				raise CommutativityError('Operation is not commutative over the given domain')
		return result


class Group(Monoid):

	def __init__(self, cset, identity, binop: GroupOperation):
		if not isinstance(binop, GroupOperation):
			raise TypeError(f'Expected a group operation, not a {typename(binop)}')
		super().__init__(cset, identity, binop)


def Z_mod(n):
	if not isinstance(n, int):
		raise TypeError('Z can only be partitioned by integer modulo')
	if not n > 0:
		raise ValueError('Z can only be partitioned by positive modulo')
	return Group(CoralSet([*range(n)]), 0, GroupOperation.from_invertible(addition_mod(n)))