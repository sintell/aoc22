# aoc2022 bootstrapper

Python module to simplify AoC challenge

## Usage
```shell
python -m aoc --solutions=. <task_id>
```
, where `task_id` is a number of the day you solving the task for

## What's inside
- Automagically loads task input, using your AoC session token
- Input is cached inside /tmp
- Supports `--debug` to show additional info
- Supports `--cache` to specify custom location for cache files
- Supports `--solutions` to specify location with the solutions, solutions must be importable as python modules

## Solution file
Each solution file must follow naming convention: `task_<task_id>.py`
Inside each solution file must be defined a class named `Task<task_id>` with the following *static* methods
```py
class Task4(Task):
    @staticmethod
    def solution_1(data: str) -> str|int:
        ...

    @staticmethod
    def solution_2(data: str) -> str|int:
        ...
```

