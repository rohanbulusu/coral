
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


class UnitalMagma(Magma):

    def __init__(self, cset, identity, binop: ClosedOperation):
        if not cset.has_element(identity):
            raise ValueError(f'Expected identity element {identity} to be contained in monoid\'s underlying set {cset}')
        super().__init__(cset, binop)
        self.identity = identity    


class Monoid(UnitalMagma):

    def __init__(self, cset, identity, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not {typename(binop)}')
        super().__init__(cset, identity, binop)
        self.identity = identity


class Semigroup(Magma):

    def __init__(self, cset, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not {typename(binop)}')
        super().__init__(cset, binop)



