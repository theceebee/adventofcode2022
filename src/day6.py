
def parse_input(input_: str):
    with open(input_, "r") as fp:
        return fp.read()


def puzzle1(input_: str) -> int:
    for i in range(4, len(input_.rstrip()) + 1):
        if len(set(input_[i - 4:i])) == 4:
            return i


def puzzle2(input_: str) -> int:
    for i in range(14, len(input_.rstrip()) + 1):
        if len(set(input_[i - 14:i])) == 14:
            return i


if __name__ == "__main__":
    #print(puzzle1(parse_input("../input/day6.txt")))
    print(puzzle2(parse_input("../input/day6.txt")))
