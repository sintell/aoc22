from abc import ABC, abstractstaticmethod
import importlib.util
import os

from aoc.logger import LOG
from aoc.task_loader import TaskLoader


class colors:
    reset = "\033[0m"
    bold = "\033[01m"

    class fg:
        red = "\033[31m"
        green = "\033[32m"


class Task(ABC):
    @staticmethod
    @abstractstaticmethod
    def solution_1(data: str) -> str | int:
        ...

    @staticmethod
    @abstractstaticmethod
    def solution_2(data: str) -> str | int:
        ...


class TaskRunner:
    task_class: Task
    task_id: int
    cache_path: str | None
    solutions_path: str

    def __init__(
        self, task_id: int, solutions_path: str, cache_path: str | None = None
    ) -> None:
        self.task_id = task_id
        if not os.path.exists(solutions_path):
            raise FileNotFoundError(
                f"solutions dirrectory {solutions_path} does not exists or is not accessible by current user"
            )

        if cache_path and not os.path.exists(os.path.abspath(cache_path)):
            raise FileNotFoundError(
                f"cache dirrectory: {cache_path} does not exists or is not accessible by current user"
            )
        self.solutions_path = os.path.abspath(solutions_path)
        self.cache_path = cache_path

        LOG.info(f"starting problem: task_id={task_id}")
        module_name = "aoc22.task_{task_id}"
        spec = importlib.util.spec_from_file_location(
            module_name,
            os.path.abspath(
                os.path.join(
                    self.solutions_path,
                    f"task_{task_id}.py",
                )
            ),
        )
        if not (spec and spec.loader):
            raise FileNotFoundError(
                f"no solution for task: task_id={task_id} at {self.solutions_path}"
            )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if not hasattr(module, f"Task{task_id}"):
            raise TypeError(
                f"file 'task_{task_id}.py must have class Task with solution_1 and solution_2 methods"
            )
        self.task_class: Task = getattr(module, f"Task{task_id}")

    def run(self):
        with TaskLoader(cache_path=self.cache_path).get_input(
            task_id=self.task_id
        ) as data:
            try:
                LOG.debug(f"running solution_1")
                result_1 = self.task_class.solution_1(data)
                if result_1:
                    LOG.info(
                        f"successefull run, {colors.bold}solution_1{colors.reset}: {colors.bold}{colors.fg.green}{result_1}{colors.reset}"
                    )
                else:
                    LOG.debug("no result for solution_1")

                LOG.debug(f"running solution_2")
                result_2 = self.task_class.solution_2(data)
                if result_2:
                    LOG.info(
                        f"successefull run, {colors.bold}solution_2{colors.reset}: {colors.bold}{colors.fg.green}{result_2}{colors.reset}"
                    )
                else:
                    LOG.debug("no result for solution_2")
            except (Exception, RuntimeError) as e:
                LOG.error(
                    f"got an exception while running solutions, probably something wrong with the code:\n\t{colors.fg.red}{e}{colors.reset}"
                )
                raise
