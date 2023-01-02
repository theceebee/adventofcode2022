from functools import lru_cache
from typing import Optional


class Cave:

    @classmethod
    def from_file(cls, filename):
        result = cls()

        with open(filename, "r") as fp:
            for line in fp:
                tokens: list[tuple[int, int]] = [tuple(int(t) for t in token.split(",")) for token in line.strip().split(" -> ")]
                for i in range(1, len(tokens)):
                    result.add_rock_path(tokens[i - 1], tokens[i])

        return result

    def __init__(self):
        self._rock: dict[int, dict[int, int]] = {}
        self._sand_source: tuple[int, int] = (500, 0)
        self._resting_sand: dict[int, dict[int, int]] = {}

    def __str__(self):
        result = ""
        min_ = self.min
        max_ = self.max
        for y in range(max_[1] + 1):  # y-minimum is always 0.
            for x in range(min_[0], max_[0] + 1):
                result += (
                    "#" if self.is_rock(x, y)
                    else "o" if self.is_resting_sand(x, y)
                    else "+" if self.is_sand_source(x, y)
                    else "."
                )
            if y != max_[1]:
                result += "\n"
        return result

    @property
    def min(self) -> tuple[int, int]:
        min_x_values = [min(v) for v in self._rock.values()]
        return min(min_x_values), 0

    @property
    def max(self) -> tuple[int, int]:
        max_x_values = [max(v) for v in self._rock.values()]
        return max(max_x_values), max(self._rock)

    @property
    def resting_sand_count(self) -> int:
        result = 0
        min_ = self.min
        max_ = self.max
        for y in range(max_[1] + 1):  # y-minimum is always 0.
            for x in range(min_[0], max_[0] + 1):
                result += self.is_resting_sand(x, y)
        return result

    @property
    def sand_source(self) -> tuple[int, int]:
        return self._sand_source

    def add_rock(self, x: int, y: int):
        self._rock.setdefault(y, dict())[x] = 1

    def add_rock_path(self, start: tuple[int, int], end: tuple[int, int]):

        def _add_horizontal_rock_path(start_: tuple[int, int], end_: tuple[int, int]):
            for i in range(start_[0], end_[0] + 1):
                self._rock.setdefault(start_[1], dict())[i] = 1

        def _add_vertical_rock_path(start_: tuple[int, int], end_: tuple[int, int]):
            for i in range(start_[1], end_[1] + 1):
                self._rock.setdefault(i, dict())[start_[0]] = 1

        if start[0] != end[0]:  # horizontal path
            _add_horizontal_rock_path(*sorted((start, end)))

        elif start[1] != end[1]:  # vertical path
            _add_vertical_rock_path(*sorted((start, end)))

        else:  # just in case, add a single coordinate of rock.
            self.add_rock(*end)

    def add_resting_sand(self, x: int, y: int):
        self._resting_sand.setdefault(y, dict())[x] = 1

    def is_rock(self, x: int, y: int) -> bool:
        return y in self._rock and self._rock[y].get(x) == 1

    def is_resting_sand(self, x: int, y: int) -> bool:
        return y in self._resting_sand and self._resting_sand[y].get(x) == 1

    def is_sand_source(self, x: int, y: int) -> bool:
        return (x, y) == self._sand_source

    # def get_sand_sources(self) -> list[tuple[int, int]]:
    #     result: list[tuple[int, int]] = []
    #     min_ = self.min
    #     max_ = self.max
    #     for y in range(max_[1] + 1):  # y-minimum is always 0.
    #         for x in range(min_[0], max_[0] + 1):
    #             if self.is_sand_source(x, y):
    #                 result.append((x, y))
    #     return result


class CaveSim:

    def __init__(self, cave: Cave):
        self.cave = cave
        self.active_sand: Optional[tuple[int, int]] = None

    @lru_cache()
    def is_in_cave(self, x: int, y: int) -> bool:
        return y <= self.cave.max[1]

    def tick(self):
        if not self.active_sand:
            self.active_sand = self.cave.sand_source
            return

        next_position = self.active_sand
        for offset in [(0, 1), (-1, 0), (2, 0)]:
            next_position = tuple(next_position[i] + offset[i] for i in range(2))

            if not self.is_in_cave(*next_position):
                break

            if not (self.cave.is_rock(*next_position) or self.cave.is_resting_sand(*next_position)):
                self.active_sand = next_position
                return

        # If we've made it this far then either the sand can't go anywhere else, or it's run out of the cave and cannot come to rest.
        if self.is_in_cave(*next_position):
            self.cave.add_resting_sand(*self.active_sand)

        self.active_sand = None

    def tick_until_next_spawn(self):
        if not self.active_sand:
            self.tick()

        while self.active_sand is not None:
            self.tick()

    def tick_until_sand_cannot_rest(self):

        if not self.active_sand:
            self.tick()

        count = self.cave.resting_sand_count

        while True:
            if self.active_sand is None:
                if self.cave.resting_sand_count == count:
                    break

                count = self.cave.resting_sand_count

            self.tick()


if __name__ == "__main__":
    sim = CaveSim(Cave.from_file("../input/day14.txt"))
    sim.tick_until_sand_cannot_rest()
    print(sim.cave.resting_sand_count)
