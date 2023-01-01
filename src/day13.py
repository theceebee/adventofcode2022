from itertools import zip_longest
from operator import mul


class PacketList(list):

    def __init__(self, initlist=None):
        super().__init__([PacketList(item) if isinstance(item, list) else item for item in initlist or []])

    def __gt__(self, other):
        for self_, other_ in zip_longest(self, other):

            if self_ is None:
                break

            elif other_ is None:
                return True

            else:
                self_is_list = isinstance(self_, PacketList)
                other_is_list = isinstance(other_, PacketList)

                if self_is_list and other_is_list:
                    if self_ > other_:
                        return True

                    elif self_ < other:
                        break

                elif self_is_list:
                    if self_ > PacketList([other_]):
                        return True

                    elif self_ < PacketList([other_]):
                        break

                elif other_is_list:
                    if PacketList([self_]) > other_:
                        return True

                    elif PacketList([self_]) < other_:
                        break

                else:  # int vs int comparison
                    if self_ > other_:
                        return True

                    elif self_ < other_:
                        break

        return False

    def __lt__(self, other):
        for self_, other_ in zip_longest(self, other):

            if self_ is None:
                return True

            elif other_ is None:
                break

            else:
                self_is_list = isinstance(self_, PacketList)
                other_is_list = isinstance(other_, PacketList)

                if self_is_list and other_is_list:
                    if self_ < other_:
                        return True

                    elif self_ > other_:
                        break

                elif self_is_list:
                    if self_ < PacketList([other_]):
                        return True

                    elif self_ > PacketList([other_]):
                        break

                elif other_is_list:
                    if PacketList([self_]) < other_:
                        return True

                    elif PacketList([self_]) > other_:
                        break

                else:  # int vs int comparison
                    if self_ < other_:
                        return True

                    elif self_ > other_:
                        break

        return False


def parse_input_pairs(filename: str) -> list[tuple]:
    result: list[tuple] = []
    with open(filename, "r") as fp:
        pair = ()
        for i, line in enumerate(fp):
            j = i % 3
            if j < 2:
                pair += (PacketList(eval(line)),)
            elif j == 2:
                result.append(pair)
                pair = ()
        result.append(pair)
    return result


def parse_input_list(filename: str) -> list[PacketList]:
    with open(filename, "r") as fp:
        return [PacketList(eval(line)) for i, line in enumerate(fp, start=1) if i % 3]


def puzzle1(filename: str) -> int:
    return sum([i for i, pair in enumerate(parse_input_pairs(filename), start=1) if pair[0] < pair[1]])


def puzzle2(filename: str) -> int:
    divider_packets: list[PacketList] = [PacketList([[2]]), PacketList([[6]])]
    input_packets: list[PacketList] = parse_input_list(filename)
    indices = [i for i, packet in enumerate(sorted(divider_packets + input_packets), start=1) if packet in divider_packets]
    return mul(*indices)


if __name__ == "__main__":
    print(puzzle1("../input/day13.txt"))
    print(puzzle2("../input/day13.txt"))
