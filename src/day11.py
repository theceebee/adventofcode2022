from __future__ import annotations
import re
from dataclasses import dataclass
from operator import mul
from typing import Callable


@dataclass
class Monkey:
    index: int
    items: list[int]
    op: Callable
    test_divisor: int
    true: int
    false: int
    parent: list[Monkey]
    inspection_count: int = 0


def parse_input(filename: str) -> list[Monkey]:
    result = []

    with open(filename, "r") as fp:
        kwargs = None

        for i, line in enumerate(fp, start=1):
            mod = i % 7
            if not mod:
                result.append(Monkey(**kwargs))
            if mod == 1:
                kwargs = {"parent": result}
                kwargs.update({k: int(v) for k, v in re.match(r"^Monkey (?P<index>\d):\s*$", line).groupdict().items()})
            elif mod == 2:
                kwargs.update({"items": [int(i) for i in line.strip().split(":")[-1].split(", ")]})
            elif mod == 3:
                kwargs.update({"op": eval(line.split(":")[-1].strip().replace("new =", "lambda x:").replace("old", "x"))})
            elif mod == 4:
                kwargs.update({k: int(v) for k, v in re.match(r"^\D+(?P<test_divisor>\d+)", line.strip()).groupdict().items()})
            elif mod == 5:
                kwargs.update({k: int(v) for k, v in re.match(r"^\D+(?P<true>\d+)", line.strip()).groupdict().items()})
            elif mod == 6:
                kwargs.update({k: int(v) for k, v in re.match(r"^\D+(?P<false>\d+)", line.strip()).groupdict().items()})

        result.append(Monkey(**kwargs))

    return result


def puzzle1(filename: str) -> int:

    monkeys = parse_input(filename)

    for i in range(20):
        for monkey in monkeys:
            items = monkey.items[:]
            monkey.items = []
            for item in items:
                monkey.inspection_count += 1
                item = monkey.op(item)
                item = item // 3
                monkeys[monkey.false if item % monkey.test_divisor else monkey.true].items.append(item)

    return mul(*sorted([monkey.inspection_count for monkey in monkeys], reverse=True)[:2])


def puzzle2(filename: str) -> int:

    monkeys = parse_input(filename)

    for i in range(20):
        for monkey in monkeys:
            items = monkey.items[:]
            monkey.items = []
            for item in items:
                monkey.inspection_count += 1
                item = monkey.op(item)
                test = not item % monkey.test_divisor
                if test:
                    monkeys[monkey.true].items.append(item)
                else:
                    monkeys[monkey.false].items.append(item)

    inspection_counts = [monkey.inspection_count for monkey in monkeys]
    print(inspection_counts)
    return mul(*(sorted(inspection_counts, reverse=True)[:2]))


if __name__ == "__main__":
    print(puzzle1("../input/day11.txt"))
    print(puzzle2("../input/day11sample.txt"))
