from itertools import zip_longest
from string import ascii_letters

from aoc.task_runner import Task


class Ruksack:
    comp_1: set
    comp_2: set

    def __init__(self, contents: str) -> None:
        half_size = len(contents) // 2
        self.comp_1, self.comp_2 = set(contents[:half_size]), set(contents[half_size:])

    def find_common_item(self):
        return ascii_letters.find(self.comp_1.intersection(self.comp_2).pop()) + 1


def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=None)


class Task3(Task):
    @staticmethod
    def solution_1(data):
        return sum((Ruksack(line).find_common_item()) for line in data.splitlines())

    @staticmethod
    def solution_2(data: str):
        return sum(
            ascii_letters.find(
                set(g[0]).intersection(set(g[1])).intersection(set(g[2])).pop()
            )
            + 1
            for g in grouper(data.splitlines(), 3)
        )
