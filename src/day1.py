from functools import cache
from typing import AnyStr


@cache
def get_calories_per_elf() -> list[int]:
    with open("../input/day1.txt", "r") as fp:
        data: AnyStr = fp.read()

    result = []
    for elf in data.split("\n\n"):
        result.append(sum([int(item) for item in elf.split("\n") if item]))

    return result


def puzzle_1() -> int:
    return max(get_calories_per_elf())


def puzzle_2() -> int:
    return sum(sorted(get_calories_per_elf())[-3:])


if __name__ == "__main__":
    print(puzzle_1())
    print(puzzle_2())
