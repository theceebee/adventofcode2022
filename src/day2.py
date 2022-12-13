from __future__ import annotations

import abc
from functools import cache


class _RockPaperScissorsBase(metaclass=abc.ABCMeta):
    def __eq__(self, other) -> bool:
        return isinstance(other, self.__class__)

    @property
    @abc.abstractmethod
    def score(self) -> int:
        ...


class Rock(_RockPaperScissorsBase):

    score = 1

    def __gt__(self, other) -> bool:
        return isinstance(other, Scissors)

    def __lt__(self, other) -> bool:
        return isinstance(other, Paper)


class Paper(_RockPaperScissorsBase):

    score = 2

    def __gt__(self, other) -> bool:
        return isinstance(other, Rock)

    def __lt__(self, other) -> bool:
        return isinstance(other, Scissors)


class Scissors(_RockPaperScissorsBase):

    score = 3

    def __gt__(self, other) -> bool:
        return isinstance(other, Paper)

    def __lt__(self, other) -> bool:
        return isinstance(other, Rock)


class Game:

    @classmethod
    def parse_puzzle1(cls, string: str) -> Game:
        map_ = {
            "A": Rock,
            "B": Paper,
            "C": Scissors,
            "X": Rock,
            "Y": Paper,
            "Z": Scissors,
        }
        return cls(*(map_.get(token)() for token in string.split(sep=" ")))

    @classmethod
    def parse_puzzle2(cls, string: str) -> Game:
        map_ = {
            "A": Rock,
            "B": Paper,
            "C": Scissors,
        }
        a, b = string.split(sep=" ")
        a = map_.get(a)()
        choices = [Rock(), Paper(), Scissors()]

        if b == "X":  # Lose
            b = next(iter([c for c in choices if c < a]))
        elif b == "Y":  # Draw
            b = next(iter([c for c in choices if c == a]))
        else:  # b == "Z"  # Win
            b = next(iter([c for c in choices if c > a]))

        return cls(a, b)

    def __init__(self, a: _RockPaperScissorsBase, b: _RockPaperScissorsBase):
        self._a = a
        self._b = b

    @property
    @cache
    def score(self) -> int:
        result = self._b.score

        if self._b > self._a:  # You win.
            result += 6

        elif self._b == self._a:  # A draw.
            result += 3

        return result


def puzzle1() -> int:
    result = 0

    with open("../input/day2.txt", "r") as fp:
        for line in fp:
            result += Game.parse_puzzle1(line.rstrip()).score

    return result


def puzzle2() -> int:
    result = 0

    with open("../input/day2.txt", "r") as fp:
        for line in fp:
            result += Game.parse_puzzle2(line.rstrip()).score

    return result


if __name__ == "__main__":
    print(puzzle1())
    print(puzzle2())
