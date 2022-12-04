from task_loader import TaskLoader
from operator import itemgetter

data = TaskLoader().get_input(2)


def solution_1():
    lookup_table = {
        "A X": 4,
        "B X": 1,
        "C X": 7,
        "A Y": 8,
        "B Y": 5,
        "C Y": 2,
        "A Z": 3,
        "B Z": 9,
        "C Z": 6,
    }
    return sum(
        f(lookup_table) for f in (itemgetter(line) for line in data.splitlines())
    )


def solution_2():
    lookup_table = {
        "A X": 3,
        "B X": 1,
        "C X": 2,
        "A Y": 4,
        "B Y": 5,
        "C Y": 6,
        "A Z": 8,
        "B Z": 9,
        "C Z": 7,
    }
    return sum(
        f(lookup_table) for f in (itemgetter(line) for line in data.splitlines())
    )


print(solution_2())
