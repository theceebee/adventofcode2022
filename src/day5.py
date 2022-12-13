import re


def parse_stacks(data: list[str]) -> list[list[str]]:

    stack_numbers = data.pop()
    indices = [i for i in range(len(stack_numbers)) if stack_numbers[i] != " "]
    result = [[] for __ in indices]

    while True:
        try:
            line = data.pop()
            for i, j in enumerate(indices):
                if len(line) + 1 < j or line[j] == " ":
                    continue
                result[i].append(line[j])
        except IndexError:
            break

    return result


def parse_input(filename: str) -> tuple[list[list[str]], list[str]]:
    middle_index = 0
    data = []
    with open(filename, "r") as fp:
        for i, line in enumerate(fp):
            line_ = line.rstrip()
            data.append(line_)
            if line_:
                continue
            middle_index = i

    stacks_raw = data[:middle_index]
    moves = data[middle_index + 1:]

    stacks = parse_stacks(stacks_raw)
    return stacks, moves


def puzzle1(input_: str) -> str:
    stacks, moves = parse_input(input_)
    for line in moves:
        count, src, dst = [int(i.group()) for i in re.finditer("\d+", line)]
        for __ in range(count):
            stacks[dst - 1].append(stacks[src - 1].pop())
    return "".join([stack[-1] for stack in stacks])


def puzzle2(input_: str) -> str:
    stacks, moves = parse_input(input_)
    for line in moves:
        count, src, dst = [int(i.group()) for i in re.finditer("\d+", line)]
        buffer = []
        for __ in range(count):
            buffer.insert(0, stacks[src - 1].pop())
        stacks[dst - 1].extend(buffer)
    return "".join([stack[-1] for stack in stacks])


if __name__ == "__main__":
    print(puzzle1("../input/day5.txt"))
    print(puzzle2("../input/day5.txt"))
