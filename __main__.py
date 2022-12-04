import argparse
import logging

from aoc.logger import LOG
from aoc.task_runner import TaskRunner

parser = argparse.ArgumentParser(
    prog="aoc22",
    description="This helper program runs a task from AoC 2022",
    epilog="Good luck this year!",
)

parser.add_argument(
    "task_id",
    help="This is the day of the task you wish to run",
    type=int,
)

parser.add_argument(
    "--debug", action="store_true", help="Show debug information during task run"
)
parser.add_argument(
    "--solutions",
    dest="solutions_path",
    help="Path of the solutions folder",
    type=str,
    required=True,
)
parser.add_argument(
    "--cache",
    dest="cache_path",
    help="Path for the cache folder instead of system /tmp folder",
    type=str,
)

if __name__ == "__main__":
    try:
        args = parser.parse_args()
        if args.debug:
            LOG.setLevel(logging.DEBUG)
        LOG.debug(f"Args parsed: {args}")
        TaskRunner(
            args.task_id,
            args.solutions_path,
            args.cache_path,
        ).run()
    except Exception:
        raise
