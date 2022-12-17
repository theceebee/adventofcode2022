from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Iterator, Union


class Direction(Enum):
    U = (0, 1)
    D = (0, -1)
    L = (-1, 0)
    R = (1, 0)


@dataclass()
class Vector:
    x: Union[int, float]
    y: Union[int, float]

    def __add__(self, other: Vector) -> Vector:
        return Vector(self.x + other.x, self.y + other.y)

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    @property
    @cache
    def magnitude(self) -> float:
        return (self.x ** 2 + self.y ** 2) ** .5

    @property
    def normal(self) -> Vector:
        return self.__class__(self.x / self.magnitude, self.y / self.magnitude)

    @classmethod
    def from_string(cls, value: str) -> Vector:
        direction, magnitude = value.rstrip().split()
        return cls(*(i * float(magnitude) for i in Direction[direction].value))

def parse_input(filename: str) -> Iterator[Vector]:
    with open(filename, "r") as fp:
        for line in fp:
            yield Vector.from_string(line)


class Simulation:

    def __init__(self):
        self.head = Vector(0, 0)
        self.tail = Vector(0, 0)

        self._tail_visited: set[Vector] = set()

    @property
    def tail_visited(self) -> list[Vector]:
        return list(self._tail_visited)

    def move_head(self, vector: Vector):
        for i in range(int(vector.magnitude)):
            self.head += vector.normal
            if abs(self.head.x - self.tail.x) > 1:
                self.tail += vector.normal
                if self.head.y != self.tail.y:
                    self.tail.y = self.head.y
            elif abs(self.head.y - self.tail.y) > 1:
                self.tail += vector.normal
                if self.head.x != self.tail.x:
                    self.tail.x = self.head.x
            self._tail_visited.add(self.tail)


def puzzle1(filename: str):
    sim = Simulation()
    for item in parse_input(filename):
        sim.move_head(item)
    print(len(sim.tail_visited))


if __name__ == "__main__":
    puzzle1("../input/day9.txt")

