
from utils import typename
from coralset import CoralSet
from maps import ClosedOperation, AssociativeOperation
from absal import is_identity


class Magma:

    def __init__(self, cset, binop: ClosedOperation):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not isinstance(binop, ClosedOperation):
            raise TypeError(f'Expected a closed operation, not {typename(binop)}')
        self.cset = cset
        self.binop = binop

# TODO: Test this class
class Monoid(Magma):

    def __init__(self, cset, identity, binop):
        super().__init__(cset, binop)
        if not cset.has_element(identity):
            raise ValueError(f'Expected identity element {identity} to be contained in the underlying set {cset}')
        
        self.identity = identity

