
from .utils import typename, chain


class CoralSet:

    def __init__(self, *set_like):
        if not all(all(hasattr(element, '__eq__') for element in sub_set_like) for sub_set_like in set_like if not isinstance(sub_set_like, type)):
            raise TypeError('All set elements must have an equality measure')
        self.is_infinite = any(isinstance(sub_set_like, type) for sub_set_like in set_like)
        self._underlying = set_like if self.is_infinite else list(set_like)

    def __repr__(self):
        return f'CoralSet{tuple(self._underlying)}'

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        # both sets are infinite
        if self.is_infinite and other.is_infinite:
            return all(item in other._underlying for item in self._underlying)
        # one of the two sets are infinite
        if self.is_infinite or other.is_infinite:
            return False
        # both sets are finite
        return set(*self._underlying) == set(*other._underlying)

    def has_element(self, candidate):
        if self.is_infinite:
            for sub_set_like in self._underlying:
                if isinstance(sub_set_like, type) and isinstance(candidate, sub_set_like):
                    return True
                if not isinstance(sub_set_like, type) and candidate in sub_set_like:
                    return True
            return False
        return any(candidate in subset for subset in self._underlying)

    def __contains__(self, item):
        return self.has_element(item)

    def __or__(self, other):
        if not isinstance(other, self.__class__):
            raise TypeError(f'Expected {typename(self)}, not {typename(other)}')
        # both sets are finite
        if not any([self.is_infinite, other.is_infinite]):
            return self.__class__(chain(*self._underlying, *other._underlying))
        # both sets are infinite
        if self.is_infinite and other.is_infinite:
            return self.__class__(*self._underlying, *other._underlying)
        return self.__class__(*self._underlying, *other._underlying)


class PositiveRealsMeta(type):

    def __instancecheck__(cls, instance):
        return isinstance(instance, (int, float)) and instance > 0


class PositiveReals(metaclass=PositiveRealsMeta):
    ...


class RealNumbersMeta(type):

    def __instancecheck__(cls, instance):
        is_on_real_locus = isinstance(instance, complex) and instance.imag == 0
        return isinstance(instance, (int, float)) or is_on_real_locus


class Reals(metaclass=RealNumbersMeta):
    ...


REALS = CoralSet(Reals)
POSITIVE_REALS = CoralSet(PositiveReals)
COMPLEX = REALS | CoralSet(complex)
NUMBERS = COMPLEX

