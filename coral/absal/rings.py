
from .groups import Group
from coral.utils import typename
from coral.coralset import CoralSet
from coral.maps import PropertyError, AbelianGroupOperation, AssociativeOperation

class Ring:
    
    def __init__(self, cset, group_addition, multiplication):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not isinstance(group_addition, AbelianGroupOperation):
            raise PropertyError(f'Expected an abelian group addition, not {typename(group_addition)}')
        if not isinstance(multiplication, AssociativeOperation):
            raise PropertyError(f'Expected an associative multiplication, not {typename(multiplication)}')
        self.cset = cset
        self.addition = group_addition
        self.multiplication = multiplication
    
    def add(self, a, b):
        return self.addition(a, b)
    
    def mul(self, a, b):
        return self.multiplication(a, b)

    




