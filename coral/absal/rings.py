
from utils import typename
from coralset import CoralSet
from maps import BinaryOperation

class Ring:

    def __init__(self, cset, operation):
        if not isinstance(cset, CoralSet):
            raise TypeError(f'Expected CoralSet, not {typename(cset)}')
        if not BinaryOperation.is_binary_operation(operation):
            raise TypeError(f'Expected a binary operation, not {typename(operation)}')
        self.cset = cset
        self.operation = operation
