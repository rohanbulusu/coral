
from .commute import Monoid
from coral.utils import typename
from coral.coralset import CoralSet
from coral.maps import InvertibleOperation, GroupOperation, addition_mod

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