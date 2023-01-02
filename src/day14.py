

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
        self._sand_source: dict[int, dict[int, int]] = {}

    def __str__(self):
        result = ""
        min_ = self.min
        max_ = self.max
        for y in range(max_[1] + 1):  # y-minimum is always 0.
            for x in range(min_[0], max_[0] + 1):
                result += "#" if self.is_rock(x, y) else "+" if self.is_sand_source(x, y) else "."
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

    def add_sand_source(self, x: int, y:int):
        self._sand_source.setdefault(y, dict())[x] = 1

    def is_rock(self, x: int, y: int) -> bool:
        return y in self._rock and self._rock[y].get(x) == 1

    def is_sand_source(self, x: int, y: int) -> bool:
        return y in self._sand_source and self._sand_source[y].get(x) == 1

    def get_sand_sources(self) -> list[tuple[int, int]]:
        result: list[tuple[int, int]] = []
        min_ = self.min
        max_ = self.max
        for y in range(max_[1] + 1):  # y-minimum is always 0.
            for x in range(min_[0], max_[0] + 1):
                if self.is_sand_source(x, y):
                    result.append((x, y))
        return result


if __name__ == "__main__":
    cave = Cave.from_file("../input/day14sample.txt")
    cave.add_sand_source(500, 0)
    print(cave)
    print(cave.get_sand_sources())
