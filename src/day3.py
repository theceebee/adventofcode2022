import string
from collections import Counter
from functools import reduce


def puzzle1(input_: str) -> int:
    result = 0

    with open(input_, "r") as fp:
        for line in fp:
            length = len(line)
            mid = length // 2
            first, second = Counter(line[:mid]), Counter(line[mid:])
            common = list(set(first).intersection(set(second)))[0]
            result += string.ascii_letters.index(common) + 1

    return result


def puzzle2(input_: str) -> int:
    result = 0

    with open(input_, "r") as fp:
        group = []
        for i, line in enumerate(fp, start=1):
            group.append(set(line.rstrip()))
            if i % 3:
                continue
            common = list(reduce(set.intersection, group))[0]
            result += string.ascii_letters.index(common) + 1
            group = []

    return result


if __name__ == "__main__":
    # print(puzzle1("../input/day3.txt"))
    print(puzzle2("../input/day3.txt"))
