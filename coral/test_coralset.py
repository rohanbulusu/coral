
from coralset import *


class TestCoralSet:

    def test_accepts_classes(self):
        assert CoralSet(int)
        assert CoralSet(float)

    def test_accepts_discrete_sequences(self):
        assert CoralSet((1, 2, 3))
        assert CoralSet([1, 2, 3])
        assert CoralSet(range(3))
        assert CoralSet(set(range(3)))

    def test_is_element_integers(self):
        integers = CoralSet(int)
        assert integers.is_element(1)
        assert integers.is_element(0)
        assert integers.is_element(-1)

    def test_non_elements_integers(self):
        integers = CoralSet(int)
        assert not integers.is_element(0.1)
        assert not integers.is_element(0.0)
        assert not integers.is_element(-0.1)
        assert not integers.is_element([1, 2, 3])

    def test_is_element_reals(self):
        reals = CoralSet(float) | CoralSet(int)
        assert reals.is_element(-1.2)
        assert reals.is_element(-1)
        assert reals.is_element(-1.0)
        assert reals.is_element(0)
        assert reals.is_element(0.0)
        assert reals.is_element(1)
        assert reals.is_element(1.0)
        assert reals.is_element(1.2)

    def test_non_elements_reals(self):
        reals = CoralSet(float)
        assert not reals.is_element(1 + 2j)
        assert not reals.is_element({'a': 1})

    def test_is_element_discrete_set(self):
        discrete = CoralSet((1, 2, 3))
        assert discrete.is_element(1)
        assert discrete.is_element(2)
        assert discrete.is_element(3)

    def test_non_elements_discrete_set(self):
        discrete = CoralSet((1, 2, 3))
        assert not discrete.is_element(12)
        assert not discrete.is_element(12 + 13j)
        assert not discrete.is_element(range(2))

    def test_infinite_set_equality(self):
        assert CoralSet(float) == CoralSet(float)

    def test_finite_set_equality(self):
        assert CoralSet((1, 2, 3)) == CoralSet((1, 2, 3))
        assert CoralSet((1, 2, 3)) == CoralSet((3, 2, 1))
        assert CoralSet((1, 2, 3)) == CoralSet((3, 3, 2, 1))

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


