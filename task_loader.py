import asyncio
from contextlib import contextmanager, suppress
import os
import tempfile

import aiohttp

from aoc.logger import LOG


class TaskLoader:
    _key: str
    _cache_path: str

    def __init__(self, cache_path: str | None = None) -> None:
        with suppress(FileExistsError):
            if not cache_path:
                self._cache_path = tempfile.gettempdir()
            else:
                self._cache_path = os.path.abspath(cache_path)

        self._key = os.environ["AOC"]

    def _get_from_cache(self, task_id):
        try:
            path = os.path.abspath(
                os.path.join(self._cache_path, f"aoc22_task_{task_id}")
            )
            with open(path, mode="r") as f:
                LOG.debug(f"reading data from cache at {path}")
                return f.read()
        except FileNotFoundError:
            return None

    def _put_to_cache(self, task_id: int, data: str):
        path = os.path.abspath(os.path.join(self._cache_path, f"aoc22_task_{task_id}"))
        with open(path, mode="w") as f:
            LOG.debug(f"writing data to cache file, at {path}")
            f.writelines(data)

    @contextmanager
    def get_input(self, task_id: int):
        task_input_url = f"https://adventofcode.com/2022/day/{task_id}/input"

        async def _req():
            async with aiohttp.ClientSession(cookies={"session": self._key}) as sess:
                LOG.debug(f"loading task #{task_id} input from {task_input_url}")
                async with sess.get(task_input_url) as resp:
                    LOG.debug(f"got {resp.status} from aoc site")
                    t = await resp.text()

                    LOG.debug(f"{len(t)} symbols in the input data")
                    self._put_to_cache(task_id, t)
                    return t

        try:
            res = self._get_from_cache(task_id)
            if res:
                yield res
            else:
                yield asyncio.run(_req())
        except (RuntimeError, Exception) as e:
            raise e
        finally:
            return None


LOADER = TaskLoader()
