
from .commute import identity_element_is_valid
from .groups import Group
from coral.utils import typename
from coral.coralset import CoralSet
from coral.maps import PropertyError, AbelianGroupOperation, AssociativeOperation

class Ring:
    
    def __init__(self, cset, identity, group_addition, multiplication):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not isinstance(group_addition, AbelianGroupOperation):
            raise PropertyError(f'Expected an abelian group addition, not {typename(group_addition)}')
        if not isinstance(multiplication, AssociativeOperation):
            raise PropertyError(f'Expected an associative multiplication, not {typename(multiplication)}')
        if not identity_element_is_valid(group_addition, identity):
            raise TypeError(f'Expected valid identity for {cset} over {group_addition}, not {identity}')
        self.cset = cset
        self.addition = group_addition
        self.multiplication = multiplication
    
    def add(self, a, b):
        return self.addition(a, b)
    
    def mul(self, a, b):
        return self.multiplication(a, b)

    




