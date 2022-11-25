
from utils import typename
from coralset import CoralSet
from maps import ClosedOperation, AssociativeOperation, LatinSquareOperation
from absal import is_identity


def validate_identity_element(cset, candidate):
    if not cset.has_element(candidate):
        raise ValueError(f'Expected identity element {candidate} to be contained in {cset}')
    return candidate


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
        super().__init__(cset, binop)
        self.identity = validate_identity_element(cset, identity)    


class Monoid(UnitalMagma):

    def __init__(self, cset, identity, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not {typename(binop)}')
        super().__init__(cset, identity, binop)


class Semigroup(Magma):

    def __init__(self, cset, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not {typename(binop)}')
        super().__init__(cset, binop)


class Quasigroup(Magma):

    def __init__(self, cset, binop: ClosedOperation):
        if not isinstance(binop, ClosedOperation):
            raise TypeError(f'Expected a closed operation, not {typename(binop)}')
        ...




