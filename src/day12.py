from __future__ import annotations
import string
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

        if not abs(self.x - x) == 1 and not abs(self.y - y) == 1:
            return False

        elif not abs(self.height - self.parent.coordinate(x, y).height) <= 1:
            return False

        return True

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
    def get_shortest_path_distance(self) -> int:
        start_index = self.start_coordinate.index
        distance = [float("inf") if i != start_index else 0 for i in range(len(self))]

        visited: set[_HeightMapCoordinate] = set()
        while self.end_coordinate not in visited:
            pass

        return len(distance)


class Graph:

    @classmethod
    def from_file(cls, filename):
        with open(filename, "r") as fp:
            lines = [line.strip() for line in fp]

        n = len(lines) * len(lines[0])
        print(n)
        return cls(n)

    def __init__(self, number_of_vertices: int):
        self._number_of_vertices = number_of_vertices
        self._adjacency_list: list[set[int]] = []

    @property
    def number_of_vertices(self) -> int:
        return self._number_of_vertices

    def add_edge(self, u: int, v: int):
        self._adjacency_list[v].add(u)


if __name__ == "__main__":

    # map_ = {"S": "a", "E": "z"}


    with open("../input/day12sample.txt", "r") as fp:
        height_map = HeightMap(lines=[line.strip() for line in fp])

    print(f"{height_map.width} x {height_map.height}")
    print(height_map.start_coordinate)
    print(height_map.end_coordinate)
    print(height_map.get_shortest_path_distance())
    print(height_map[0])
    print(height_map[21])
    print(height_map[39])

    # g = Graph(len(lines) * len(lines[0]))
    #
    # sentinel = 0
    # start = 0
    # end = 0
    # for v in range(1, len(lines)):
    #     for u in range(1, len(lines[0])):
    #         value = lines[v - 1][u - 1]
    #         if value == "S":
    #             start = sentinel
    #         elif value == "E":
    #             end = sentinel
    #         right = lines[v - 1][u]
    #         down = lines[v][u - 1]
    #
    #         if map_.get(right, right) - map_.get(value, value) <= 1:
    #             g.add_edge(u, v - 1)
    #
    #
    #
    #         sentinel += 1
    #
    #     # print("\n", end="")
