
from coral.utils import typename
from coral.coralset import CoralSet
from coral.maps import PropertyError, ClosedOperation, AssociativeOperation, LatinSquareOperation

def validate_identity_element(cset, candidate):
    if not cset.has_element(candidate):
        raise ValueError(f'Expected identity element {candidate} to be contained in {cset}')
    return candidate


class Magma:

    def __init__(self, cset, binop: ClosedOperation):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not isinstance(binop, ClosedOperation):
            raise TypeError(f'Expected a closed operation, not a {typename(binop)}')
        self.cset = cset
        self.binop = binop

    def __eq__(self, other):
        return self.cset == other.cset and (isinstance(other.binop, self.binop.__class__) or isinstance(self.binop, other.binop.__class__))

    def __contains__(self, item):
        return item in self.cset

    def __call__(self, a, b):
        return self.binop(a, b)


class UnitalMagma(Magma):

    def __init__(self, cset, identity, binop: ClosedOperation):
        super().__init__(cset, binop)
        self.identity = validate_identity_element(cset, identity)

    def __eq__(self, other):
        if not isinstance(other, UnitalMagma):
            return False
        return super().__eq__(other) and self.identity == other.identity

    def __call__(self, a, b):
        if a == self.identity or b == self.identity:
            if not self.binop(a, b) == self.binop(b, a):
                raise PropertyError(f'Identified identity element {self.identity} does not satisfy identity axioms')
        return self.binop(a, b)


class Monoid(UnitalMagma):

    def __init__(self, cset, identity, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not a {typename(binop)}')
        super().__init__(cset, identity, binop)


class Semigroup(Magma):

    def __init__(self, cset, binop: AssociativeOperation):
        if not isinstance(binop, AssociativeOperation):
            raise TypeError(f'Expected an associative operation, not a {typename(binop)}')
        super().__init__(cset, binop)


class Quasigroup(Magma):

    def __init__(self, cset, binop: LatinSquareOperation):
        if not isinstance(binop, LatinSquareOperation):
            raise TypeError(f'Expected an operation satisfying the Latin Square property, not {typename(binop)}')
        super().__init__(cset, binop)


class Loop(UnitalMagma):

    def __init__(self, cset, identity, binop: LatinSquareOperation):
        if not isinstance(binop, LatinSquareOperation):
            raise TypeError(f'Expected an operation satisfying the Latin Square property, not {typename(binop)}')
        super().__init__(cset, identity, binop)

