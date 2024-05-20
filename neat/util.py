import random
from typing import Sequence, Iterable, Iterator, TypeVar

T = TypeVar('T')

def random_bool():
    return bool(random.getrandbits(1))

class SparseList(Iterable[T]):
    def __init__(self):
        self.values = dict()

    def __setitem__(self, index: int, value):
        self.values[index] = value

    def __getitem__(self, index):
        if index in self.values:
            return self.values[index]
        return None

    def __len__(self):
        if self.values:
            return max(self.values.keys()) + 1
        else:
            return 0

    def __iter__(self)->Iterator[T]:
        return iter([self[i] for i in range(len(self))])

    def __repr__(self):
        return f"SpareList(len:{len(self)})"

    def __str__(self):
        return "[" + ", ".join([str(i) for i in self]) + "]"