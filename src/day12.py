from __future__ import annotations
from operator import itemgetter
import string
import sys
from functools import cache


class _HeightMapCoordinate:

    _value_remap = {"S": "a", "E": "z"}

    def __init__(self, x: int, y: int, parent: HeightMap):
        self.x = x
        self.y = y
        self.parent = parent

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f"index: {self.index}, x: {self.x}, y: {self.y}, height: {self.height}"

    @property
    @cache
    def height(self) -> int:
        char = self.parent._lines[self.y][self.x]
        return string.ascii_lowercase.index(self._value_remap.get(char, char))

    @property
    @cache
    def index(self) -> int:
        return self.y * len(self.parent._lines[self.y]) + self.x

    @cache
    def is_adjacent(self, x: int, y: int) -> bool:

        x_offset = abs(self.x - x)
        y_offset = abs(self.y - y)

        if not (x_offset != 1 or y_offset != 1) or x_offset + y_offset != 1:
            return False

        elif self.parent.coordinate(x, y).height - self.height > 1:
            return False

        return True

    @property
    @cache
    def adjacent(self) -> list[_HeightMapCoordinate]:
        result = []

        # left
        if self.x > 0 and self.is_adjacent(self.x - 1, self.y):
            result.append(self.parent.coordinate(self.x - 1, self.y))

        # right
        if self.x < self.parent.width - 1 and self.is_adjacent(self.x + 1, self.y):
            result.append(self.parent.coordinate(self.x + 1, self.y))

        # up
        if self.y > 0 and self.is_adjacent(self.x, self.y - 1):
            result.append(self.parent.coordinate(self.x, self.y - 1))

        # down
        if self.y < self.parent.height - 1 and self.is_adjacent(self.x, self.y + 1):
            result.append(self.parent.coordinate(self.x, self.y + 1))

        return result


class HeightMap:

    def __init__(self, lines: list[str]):
        self._lines = lines

    def __getitem__(self, item: int) -> _HeightMapCoordinate:
        line_length = len(self._lines[0])
        x = item % line_length
        y = item // line_length
        return self.coordinate(x, y)

    def __len__(self) -> int:
        return len(self._lines) * len(self._lines[0])

    @property
    @cache
    def width(self) -> int:

        if not self._lines:
            return 0

        return len(self._lines[0].strip())

    @property
    @cache
    def height(self) -> int:

        if not self._lines:
            return 0

        return len(self._lines)

    @property
    @cache
    def start_coordinate(self) -> _HeightMapCoordinate:
        for y, line in enumerate(self._lines):
            for x, char in enumerate(line):
                if char != "S":
                    continue
                return _HeightMapCoordinate(x, y, self)

    @property
    @cache
    def end_coordinate(self):
        for y, line in enumerate(self._lines):
            for x, char in enumerate(line):
                if char != "E":
                    continue
                return _HeightMapCoordinate(x, y, self)

    @cache
    def coordinate(self, x: int, y: int) -> _HeightMapCoordinate:
        return _HeightMapCoordinate(x, y, self)

    @cache
    def dijkstra(self, src: _HeightMapCoordinate) -> list[int]:

        visited: list[int] = []
        cost: list[int] = []
        prev: list[int] = []

        for __ in range(len(self)):
            visited.append(0)
            cost.append(sys.maxsize)
            prev.append(-1)

        cost[src.index] = 0

        for i in range(len(self)):
            min_cost = sorted([(i, c, v) for i, (c, v) in enumerate(zip(cost, visited)) if not v], key=itemgetter(1))[0][0]

            if cost[min_cost] == sys.maxsize:
                break

            for adjacent in self[min_cost].adjacent:
                new_cost = cost[min_cost] + 1
                if new_cost < cost[adjacent.index]:
                    cost[adjacent.index] = new_cost
                    prev[adjacent.index] = min_cost

            visited[min_cost] = 1

        return cost


def puzzle1(height_map_: HeightMap) -> int:
    distance = height_map_.dijkstra(height_map_.start_coordinate)
    return distance[height_map_.end_coordinate.index]


def puzzle2(height_map_: HeightMap) -> int:
    result = sys.maxsize

    for i in range(len(height_map_)):
        if height_map_[i].height > 0:
            continue

        distances = height_map_.dijkstra(height_map_[i])
        new_distance = distances[height_map_.end_coordinate.index]
        if new_distance < result:
            result = new_distance

    return result


if __name__ == "__main__":
    with open("../input/day12.txt", "r") as fp:
        height_map = HeightMap(lines=[line.strip() for line in fp])

    print(puzzle1(height_map))
    print(puzzle2(height_map))
