
import itertools

from .commute import identity_element_is_valid
from .groups import Group
from coral.utils import typename
from coral.coralset import CoralSet, CustomCoralSet
from coral.maps import PropertyError, AbelianGroupOperation, AssociativeOperation

class Ring:
    
    def __init__(self, cset, group_addition, additive_identity, multiplication):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not isinstance(group_addition, AbelianGroupOperation):
            raise PropertyError(f'Expected an abelian group addition, not {typename(group_addition)}')
        if not isinstance(multiplication, AssociativeOperation):
            raise PropertyError(f'Expected an associative multiplication, not {typename(multiplication)}')
        if not identity_element_is_valid(group_addition, additive_identity):
            raise TypeError(f'Expected valid identity for {cset} over {group_addition}, not {additive_identity}')
        
        self.cset = cset
        self.addition = group_addition
        self.additive_identity = additive_identity
        self.multiplication = multiplication

        self.additive_group = Group(self.cset, self.additive_identity, self.addition)
        self.is_infinite = self.cset.is_infinite


    @classmethod
    def from_group(cls, addition_group, multiplication):
        return cls(
            addition_group.cset,  
            addition_group.binop,
            addition_group.identity, 
            multiplication
        )
    
    def add(self, a, b):
        return self.addition(a, b)
    
    def mul(self, a, b):
        return self.multiplication(a, b)


class UnitalRing(Ring):

    def __init__(self, cset, group_addition, additive_identity, multiplication, multiplicative_identity):
        super().__init__(cset, group_addition, additive_identity, multiplication, multiplicative_identity)
        self.multiplicative_identity = multiplicative_identity


class Ideal:

    def __init__(self, cset):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        self.cset = cset

    def is_right_ideal_of(self, ring):
        if not isinstance(ring, Ring):
            raise TypeError(f'Expected Ring, not {typename(ring)}')
        if self.cset == ring.cset:
            return True
        if not ring.is_infinite:
            if self.cset.is_infinite:
                return False
            return all(ring.mul(r, i) in self.cset for r, i in zip(ring.cset.elements, self.cset.elements) if i != ring.additive_identity)
        for set_like in ring.cset._underlying:
            if isinstance(set_like, CustomCoralSet):
                if isinstance(self.cset._underlying[0], CustomCoralSet):
                    return set_like.CLOSURE.has_subset(self.cset._underlying[0].CLOSURE)
                if self.cset.is_infinite:
                    return set_like.CLOSURE.has_subset(self.cset)
                return all(ring.mul(r, i) in self.cset for r, i in zip(self.cset.elements, self.cset.elements))
            if isinstance(set_like, type) and set_like not in self.cset:
                return False
            if not isinstance(set_like, type):
                if not any(item in self.cset for item in set_like):
                    return False
        if not ring.cset.has_subset(self.cset):
            return False
        if not Group(self.cset, ring.additive_identity, ring.addition).is_subgroup(ring.additive_group):
            return False
        return True

    def is_proper_right_ideal_of(self, ring):
        if self.cset == ring.cset:
            return False
        return self.is_right_ideal_of(ring)

    def is_left_ideal_of(self, ring):
        if not isinstance(ring, Ring):
            raise TypeError(f'Expected Ring, not {typename(ring)}')
        if self.cset == ring.cset:
            return True
        if not ring.is_infinite:
            if self.cset.is_infinite:
                return False
            return all(i*r in self.cset for r, i in zip(ring.cset.elements, self.cset.elements) if i != ring.additive_identity)
        for set_like in ring.cset._underlying:
            if isinstance(set_like, CustomCoralSet):
                if isinstance(self.cset._underlying[0], CustomCoralSet):
                   return set_like.CLOSURE.has_subset(self.cset._underlying[0].CLOSURE)
                if self.cset.is_infinite:
                    return set_like.CLOSURE.has_subset(self.cset)
                return all(ring.mul(i, r) in self.cset for r, i in zip(self.cset.elements, self.cset.elements))
            if isinstance(set_like, type) and set_like not in self.cset:
                return False
            if not isinstance(set_like, type):
                if not any(item in self.cset for item in set_like):
                    return False
        if not ring.cset.has_subset(self.cset):
            return False
        if not Group(self.cset, ring.additive_identity, ring.addition).is_subgroup(ring.additive_group):
            return False
        return True

    def is_proper_left_ideal_of(self, ring):
        if self.cset == ring.cset:
            return False
        return self.is_left_ideal_of(ring)

    def is_ideal_of(self, ring):
        return self.is_right_ideal_of(ring) and self.is_left_ideal_of(ring)

    def is_proper_ideal_of(self, ring):
        return self.is_proper_right_ideal_of(ring) and self.is_proper_left_ideal_of(ring)
    



