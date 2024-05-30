import random
from typing import Iterable, Iterator, TypeVar

T = TypeVar("T")


def random_bool():
    return bool(random.getrandbits(1))


class SparseList(Iterable[T]):
    def __init__(self) -> None:
        self.values: dict[int, T] = {}

    def iter_skip_nones(self) -> Iterator[T]:
        return iter(v for v in self if v)

    def __getitem__(self, index) -> T|None:
        if index in self.values:
            return self.values[index]
        return None

    def __setitem__(self, index: int, value: T):
        if not isinstance(index, int):
            raise TypeError(f"Spare list index must be of type [int]. Was {type(index)}")
        self.values[index] = value

    def __iter__(self) -> Iterator[T]:
        return iter([self[i] for i in range(len(self))])

    def __len__(self):
        if self.values:
            return max(self.values.keys()) + 1
        else:
            return 0

    def __repr__(self):
        return f"SpareList(len:{len(self)})"

    def __str__(self):
        return "[" + ", ".join([str(i) for i in self]) + "]"
