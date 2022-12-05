import enum
from itertools import zip_longest
import re

from aoc.task_runner import Task


class CargoMoverVersion(enum.IntEnum):
    MOVER_9000 = enum.auto()
    MOVER_9001 = enum.auto()


class Instruction:
    move_from: int
    move_to: int
    amount: int
    __instruction_tpl_re: re.Pattern = re.compile(
        r"move (?P<amount>\d+) from (?P<from>\d+) to (?P<to>\d+)"
    )

    def __init__(self, instruction_line: str) -> None:
        match = self.__instruction_tpl_re.match(instruction_line)
        if match:
            self.move_from = int(match.group("from"))
            self.move_to = int(match.group("to"))
            self.amount = int(match.group("amount"))

    def __repr__(self) -> str:
        return f"<I {self.move_from}->{self.move_to} ={self.amount}>"


class CargoPile:
    _pile: dict[int, list[str]] = {}

    def __init__(self, cargo_lines: list[str]) -> None:
        for line in cargo_lines:
            label, cargo = int(line[:1]), list(line[1:])
            self._pile[label] = cargo

    def __repr__(self) -> str:
        return f"<P \n\t{self._pile}\n>"

    def move_cargo(
        self,
        instruction: Instruction,
        mover_version: CargoMoverVersion = CargoMoverVersion.MOVER_9000,
    ):
        if mover_version == CargoMoverVersion.MOVER_9000:
            lifted_cargo = reversed(
                self._pile[instruction.move_from][-instruction.amount :]
            )
        else:
            lifted_cargo = self._pile[instruction.move_from][-instruction.amount :]

        self._pile[instruction.move_to].extend(lifted_cargo)

        self._pile[instruction.move_from] = self._pile[instruction.move_from][
            : -instruction.amount
        ]

    def list_top(self):
        return "".join([x[-1] for x in self._pile.values()])


def group(l, n):
    return list(map(list, zip_longest(*[iter(l)] * n, fillvalue=" ")))


class Task5(Task):
    @staticmethod
    def parse(data: str):
        # split cargo from instructions
        r = data.split("\n\n")
        cargo_input, instruction_lines = (
            [
                list(
                    map(
                        lambda l: "".join(l).strip(" []"),
                        group(s, 4),
                    )
                )
                for s in r[0].splitlines()
            ],
            r[1].splitlines(),
        )
        T_cargo_input = ["".join(reversed(x)) for x in zip(*cargo_input)]

        return CargoPile(T_cargo_input), [
            Instruction(line) for line in instruction_lines
        ]

    @staticmethod
    def solution_1(data: str):
        pile, instructions = Task5.parse(data)

        # for every instruction in instructions list
        for i in instructions:
            # apply instruction to cargo lines
            pile.move_cargo(i, mover_version=CargoMoverVersion.MOVER_9000)

        return pile.list_top()

    @staticmethod
    def solution_2(data: str):
        pile, instructions = Task5.parse(data)

        # for every instruction in instructions list
        for i in instructions:
            # apply instruction to cargo lines
            pile.move_cargo(i, CargoMoverVersion.MOVER_9001)

        return pile.list_top()
