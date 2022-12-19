from __future__ import annotations
import abc
from dataclasses import dataclass
from typing import TypeVar

class AbstractInstruction(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def execute(self, cpu: CPU) -> None:
        ...

class NoOpInstruction(AbstractInstruction):

    def __init__(self):
        self.execution_cycles = 1

    def execute(self, cpu: CPU):
        ...


class AddXInstruction(AbstractInstruction):

    def __init__(self, value: int):
        self.execution_cycles = 1
        self.value = value

    def execute(self, cpu: CPU):
        cpu.x += self.value


IT = TypeVar("IT", NoOpInstruction, AddXInstruction)


def parse_instruction(string_: str) -> IT:
    if string_.startswith("noop"):
        return NoOpInstruction()
    elif string_.startswith("addx"):
        return AddXInstruction(value=int(string_.rsplit(" ", 1)[-1]))


@dataclass
class CPU:
    x: int = 1


class ExecutionState:

    def __init__(self):
        self._cycle_count: int = 0
        self._cpu = CPU()
        self._instruction_queue: list[IT] = []

    def __next__(self) -> ExecutionState:
        if not self._instruction_queue:
            raise StopIteration

        self._cycle_count += 1

        if self._instruction_queue[0].execution_cycles > 0:
            self._instruction_queue[0].execution_cycles -= 1

        else:
            self._instruction_queue.pop(0).execute(self._cpu)

        return self

    @property
    def cpu(self) -> CPU:
        return self._cpu

    @property
    def cycle_count(self) -> int:
        return self._cycle_count

    @property
    def signal_strength(self) -> int:
        return self._cycle_count * self._cpu.x

    def queue_instruction(self, instruction: IT):
        self._instruction_queue.append(instruction)


def puzzle1(execution_state: ExecutionState) -> int:
    result = 0

    while True:
        try:
            execution_state = next(execution_state)
        except StopIteration:
            break

        print(execution_state.cycle_count, execution_state.cpu.x)

        if execution_state.cycle_count in [20, 60, 100, 140, 180, 220]:
            print("Signal:", execution_state.signal_strength)
            result += execution_state.signal_strength

    return result


if __name__ == "__main__":
    state = ExecutionState()

    with open("../input/day10sample.txt", "r") as fp:
        for line in fp:
            state.queue_instruction(parse_instruction(line.rstrip()))

    print(puzzle1(state))
