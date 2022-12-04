from task_loader import TaskLoader

input = TaskLoader().get_input(1)


def solution_1():
    max = 0
    for chunk in input.split("\n\n"):
        total = sum(map(int, chunk.strip().splitlines()))
        if total > max:
            max = total

    return max


def solution_2():
    top = sorted(
        (sum(map(int, chunk.splitlines())) for chunk in input.split("\n\n")),
        reverse=True,
    )[:3]
    return sum(top)


print(solution_2())
