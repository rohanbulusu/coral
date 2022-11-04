
from utils import typename
from coralset import CoralSet
from maps import BinaryOperation
from absal import is_identity

# TODO: Test this class
class Magma:

    def __init__(self, cset, binary_operation):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not BinaryOperation.is_binary_operation(binary_operation):
            raise TypeError(f'Expected a binary operation, not {binary_operation}')
        self.cset = cset
        self.binop = binary_operation

# TODO: Test this class
class Monoid(Magma):

    def __init__(self, cset, identity, binop):
        super().__init__(cset, binop)
        if not cset.has_element(identity):
            raise ValueError(f'Expected identity element {identity} to be contained in the underlying set {cset}')
        self.identity = identity

