from functools import reduce


def puzzle1(input_: str):
    count = 0

    with open(input_, "r") as fp:
        for line in fp:
            ranges = []
            for range_ in line.rstrip().split(","):
                min_, max_ = [int(i) for i in range_.split("-")]
                ranges.append(set(range(min_, max_ + 1)))
            if reduce(set.intersection, ranges) in ranges:
                count += 1

    return count


def puzzle2(input_: str):
    count = 0

    with open(input_, "r") as fp:
        for line in fp:
            ranges = []
            for range_ in line.rstrip().split(","):
                min_, max_ = [int(i) for i in range_.split("-")]
                ranges.append(set(range(min_, max_ + 1)))
            if reduce(set.intersection, ranges):
                count += 1

    return count


if __name__ == "__main__":
    print(puzzle1("../input/day4.txt"))
    print(puzzle2("../input/day4.txt"))
