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
        self.execution_cycles = 2
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

    @classmethod
    def from_file(cls, filename: str) -> ExecutionState:
        result = cls()

        with open(filename, "r") as fp:
            for line in fp:
                result.queue_instruction(parse_instruction(line.rstrip()))

        return result

    def __init__(self):
        self._cycle_count: int = 0
        self._cpu = CPU()
        self._instruction_queue: list[IT] = []

    def __next__(self) -> ExecutionState:
        if not self._instruction_queue:
            raise StopIteration

        self._cycle_count += 1
        self._instruction_queue[0].execution_cycles -= 1

        if not self._instruction_queue[0].execution_cycles:
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


def puzzle1(filename: str) -> int:
    result = 0
    execution_state = ExecutionState.from_file(filename)

    while True:
        register_value = execution_state.cpu.x

        try:
            execution_state = next(execution_state)
        except StopIteration:
            break

        if execution_state.cycle_count in [20, 60, 100, 140, 180, 220]:
            signal_strength = execution_state.cycle_count * register_value
            result += signal_strength

    return result


def puzzle2(filename: str):

    def _draw_pixel(cycle: int, value: int) -> bool:
        values = list(range(value, value + 3))
        return cycle in values

    execution_state = ExecutionState.from_file(filename)

    while True:
        register = execution_state.cpu.x

        try:
            execution_state = next(execution_state)
        except StopIteration:
            break

        cycle = execution_state.cycle_count % 40
        print(
            "#" if _draw_pixel(cycle, register) else ".",
            end="\n" if not cycle else ""
        )


if __name__ == "__main__":
    input_ = "../input/day10.txt"
    print(puzzle1(input_))
    puzzle2(input_)
