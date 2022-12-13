from __future__ import annotations

from enum import auto
from enum import IntEnum
from typing import Optional


class Tree:

    class Direction(IntEnum):
        left = auto()
        right = auto()
        up = auto()
        down = auto()

    def __init__(self, x: int, y: int, height: int, grid: Grid):
        self.x = x
        self.y = y
        self.height = height
        self.grid = grid

    @property
    def left(self) -> Optional[Tree]:
        if self.x:
            return self.grid[self.y][self.x - 1]

    @property
    def right(self) -> Optional[Tree]:
        if self.x < self.grid.width - 1:
            return self.grid[self.y][self.x + 1]

    @property
    def up(self) -> Optional[Tree]:
        if self.y:
            return self.grid[self.y - 1][self.x]

    @property
    def down(self) -> Optional[Tree]:
        if self.y < self.grid.height - 1:
            return self.grid[self.y + 1][self.x]

    def is_visible_from(self, direction: Direction) -> bool:
        next_ = getattr(self, direction.name)
        if next_:
            return next_.height < self.height and next_.is_visible_from(direction)
        return True

    @property
    def is_visible(self) -> bool:
        result = False

        if all([self.grid[self.y][x].height < self.height for x in range(self.x)]):
            result = True

        if all([self.grid[self.y][x].height < self.height for x in range(self.x + 1, self.grid.width)]):
            result = True

        if all([self.grid[y][self.x].height < self.height for y in range(self.y)]):
            result = True

        if all([self.grid[y][self.x].height < self.height for y in range(self.y + 1, self.grid.height)]):
            result = True

        return result

    @property
    def scenic_score(self) -> int:

        trees_left = 0
        for x in range(self.x - 1, -1, -1):
            trees_left += 1
            if self.grid[self.y][x].height >= self.height:
                break

        trees_right = 0
        for x in range(self.x + 1, self.grid.width):
            trees_right += 1
            if self.grid[self.y][x].height >= self.height:
                break

        trees_up = 0
        for y in range(self.y - 1, -1, -1):
            trees_up += 1
            if self.grid[y][self.x].height >= self.height:
                break

        trees_down = 0
        for y in range(self.y + 1, self.grid.height):
            trees_down += 1
            if self.grid[y][self.x].height >= self.height:
                break

        return trees_left * trees_right * trees_up * trees_down


class Grid(list):

    @property
    def width(self) -> int:
        return len(self[0])

    @property
    def height(self) -> int:
        return len(self)

    def __iter__(self) -> Tree:
        for i in range(len(self)):
            for j in range(len(self[i])):
                yield self[i][j]


def parse_input(input_: str) -> Grid:
    result = Grid()
    with open(input_, "r") as fp:
        for i, line in enumerate(fp):
            result.append([])
            for j, height in enumerate(line.rstrip()):
                result[i].append(Tree(j, i, int(height), result))
    return result


def puzzle1(grid: Grid) -> int:
    return sum([int(tree.is_visible) for tree in grid])


def puzzle2(grid: Grid) -> int:
    highest_scenic_score = grid[0][0]
    for tree in grid:
        if tree.scenic_score > highest_scenic_score.scenic_score:
            highest_scenic_score = tree
    return highest_scenic_score.scenic_score


if __name__ == "__main__":
    grid_ = parse_input("../input/day8.txt")
    print(puzzle1(grid_))
    print(puzzle2(grid_))
