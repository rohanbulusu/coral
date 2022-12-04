
from pytest import fixture

from .coralset import *

@fixture
def Z():
    return CoralSet(int)

@fixture
def R(Z):
    return CoralSet(float) | Z

@fixture
def C(R):
    return R | CoralSet(float)


class TestCoralSet:

    def test_accepts_classes(self):
        assert CoralSet(int)
        assert CoralSet(float)

    def test_accepts_sets(self):
        assert CoralSet(set([1, 2, 3]))

    def test_accepts_discrete_sequences(self):
        assert CoralSet((1, 2, 3))
        assert CoralSet([1, 2, 3])
        assert CoralSet(range(3))
        assert CoralSet(set(range(3)))

    def test_has_element_integers(self, Z):
        assert 1 in Z
        assert 0 in Z
        assert -1 in Z

    def test_non_elements_integers(self, Z):
        assert 0.1 not in Z
        assert 0.0 not in Z # should this be true or false?
        assert -0.1 not in Z
        assert [1, 2, 3] not in Z

    def test_has_element_reals(self, R):
        assert -1.2 in R
        assert -1 in R
        assert -1.0 in R
        assert 0 in R
        assert 0.0 in R
        assert 1 in R
        assert 1.0 in R
        assert 1.2 in R

    def test_non_elements_reals(self, R):
        assert 1 + 2j not in R
        assert [1, 2, 3] not in R

    def test_has_element_discrete_set(self):
        discrete = CoralSet((1, 2, 3))
        assert 1 in discrete
        assert 2 in discrete
        assert 3 in discrete

    def test_non_elements_discrete_set(self):
        discrete = CoralSet((1, 2, 3))
        assert 12 not in discrete
        assert 12 + 13j not in discrete
        assert range(2) not in discrete

    def test_infinite_set_equality(self):
        assert CoralSet(float) == CoralSet(float)

    def test_finite_set_equality(self):
        assert CoralSet((1, 2, 3)) == CoralSet((1, 2, 3))
        assert CoralSet((1, 2, 3)) == CoralSet((3, 2, 1))
        assert CoralSet((1, 2, 3)) == CoralSet((3, 3, 2, 1))

        assert CoralSet(set([1, 2, 3])) == CoralSet((1, 2, 3))
        assert CoralSet([1, 2, 3]) == CoralSet((1, 2, 3))

    def test_allows_infinite_infinite_union(self):
        assert CoralSet(float) | CoralSet(int)

    def test_allows_infinite_finite_union(self):
        assert CoralSet(int) | CoralSet((0.1, 0.2, 0.3))
        assert CoralSet((0.1, 0.2, 0.3)) | CoralSet(int)

    def test_allow_finite_finite_union(self):
        assert CoralSet((1, 2)) | CoralSet((3, 4)) == CoralSet((1, 2, 3, 4))

    def test_same_same_union(self):
        assert CoralSet(float) | CoralSet(float) == CoralSet(float)
        assert CoralSet((1, 2, 3)) | CoralSet((1, 2, 3)) == CoralSet((1, 2, 3))

    def test_membership_via_in_keyword(self):
        assert 1 in CoralSet((1, 2))
        assert 1 + 2j in CoralSet((1 + 1j, 1 + 2j))

        assert 0 in CoralSet(int)
        assert 1j in CoralSet(complex)
        assert 0.01 in CoralSet(float)
