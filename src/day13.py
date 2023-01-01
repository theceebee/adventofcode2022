import logging
from itertools import zip_longest

logger = logging.getLogger(__name__)


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


def parse_input(filename: str) -> list[tuple]:
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


def debug(filename: str):
    for i, pair in enumerate(parse_input(filename), start=1):
        print(f"{i}: {pair[0] < pair[1]}")


def puzzle1(filename: str) -> int:
    return sum([i for i, pair in enumerate(parse_input(filename), start=1) if pair[0] < pair[1]])


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    print(puzzle1("../input/day13.txt"))

