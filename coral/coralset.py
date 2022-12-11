
from .utils import typename, chain


class CoralSet:

    def __init__(self, *set_like):
        if not all(all(hasattr(element, '__eq__') for element in sub_set_like) for sub_set_like in set_like if not isinstance(sub_set_like, type)):
            raise TypeError('All set elements must have an equality measure')
        self.is_infinite = any(isinstance(sub_set_like, type) for sub_set_like in set_like)
        self._underlying = set_like if self.is_infinite else list(set_like)

    def __repr__(self):
        return f'CoralSet{tuple(self._underlying)}'

    @property
    def elements(self):
        if self.is_infinite:
            raise ValueError(f'Cannot list all elements of an infinite set')
        return chain(*self._underlying)

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
        
    def __contains__(self, candidate):
        if self.is_infinite:
            for sub_set_like in self._underlying:
                if isinstance(sub_set_like, type) and isinstance(candidate, sub_set_like):
                    return True
                if not isinstance(sub_set_like, type) and candidate in sub_set_like:
                    return True
            return False
        return any(candidate in subset for subset in self._underlying)

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

    def has_subset(self, candidate):
        if not isinstance(candidate, CoralSet):
            raise TypeError(f'Expected {typename(self)}, not {typename(candidate)}')
        # ensures this method only implements a PROPER subset
        if self == candidate:
            return False

        if isinstance(self._underlying[0], CustomCoralSet) and isinstance(candidate._underlying[0], CustomCoralSet):
            return self._underlying[0].CLOSURE.has_subset(candidate._underlying[0].CLOSURE)
        if isinstance(self._underlying[0], CustomCoralSet):
            return self._underlying[0].CLOSURE.has_subset(candidate)
        if isinstance(candidate._underlying[0], CustomCoralSet):
            return candidate._underlying[0].CLOSURE.has_subset(self)  

        # if both sets are infinite
        if self.is_infinite and candidate.is_infinite:
            for c_set_like in candidate._underlying:
                if c_set_like not in self._underlying:
                    if isinstance(c_set_like, type):
                        return False
                    for element in c_set_like:
                        if any(isinstance(element, s_set_like) for s_set_like in self._underlying if isinstance(s_set_like, type)):
                            continue
                        if not any(element in s_set_like for s_set_like in self._underlying if not isinstance(s_set_like, type)):
                            return False
            return True
        # if self is infinite and candidate is finite
        if self.is_infinite:
            return all(
                all(any(isinstance(item, T) for T in self._underlying) for item in sub_set_like)
                for sub_set_like in candidate._underlying
            )
        # if candidate is infinite and self is finite
        if candidate.is_infinite:
            return False
        # if both sets are finite
        return (self | candidate) == self

    def is_subset(self, candidate):
        if not isinstance(candidate, CoralSet):
            raise TypeError(f'Expected {typename(self)}, not {typename(candidate)}')
        return candidate.has_subset(self)


COMPLEX = CoralSet(int) | CoralSet(float) | CoralSet(complex)


class CustomCoralSet(type):
    CLOSURE = tuple()


class _RealLocusMeta(CustomCoralSet):

    CLOSURE = COMPLEX

    def __instancecheck__(cls, instance):
        if isinstance(instance, (int, float)):
            return True
        return isinstance(instance, complex) and instance.imag == 0


class _RealLocus(metaclass=_RealLocusMeta):
    ...


REALS = CoralSet(_RealLocus)


class _PositiveRealsMeta(CustomCoralSet):

    CLOSURE = CoralSet(int) | CoralSet(float)

    def __instancecheck__(cls, instance):
        return isinstance(instance, (int, float)) and instance > 0


class _PositiveReals(metaclass=_PositiveRealsMeta):
    ...


POSITIVE_REALS = CoralSet(_PositiveReals)


class _IntegersMeta(CustomCoralSet):

    CLOSURE = CoralSet(int) | CoralSet(float)

    def __instancecheck__(cls, instance):
        return isinstance(instance, int)


class _Integers(metaclass=_IntegersMeta):
    ...


INTEGERS = CoralSet(_Integers)


class _EvenIntegersMeta(CustomCoralSet):

    CLOSURE = CoralSet(int)

    def __instancecheck__(cls, instance):
        return isinstance(instance, int) and (instance % 2 == 0)


class _EvenIntegers(metaclass=_EvenIntegersMeta):
    ...


EVEN_INTEGERS = CoralSet(_EvenIntegers)

