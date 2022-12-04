from aoc.task_runner import Task


class RoomRange:
    _range_start: int
    _range_end: int

    def __init__(self, start: int, end: int) -> None:
        self._range_start = int(start)
        self._range_end = int(end)

    def __repr__(self) -> str:
        return f"<RoomRange start={self._range_start} end={self._range_end}>"

    def contains(self, other_range: "RoomRange"):
        return (
            self._range_start <= other_range._range_start
            and self._range_end >= other_range._range_end
        )

    def overlaps(self, other_range: "RoomRange"):
        return (
            self._range_start <= other_range._range_start <= self._range_end
            or self._range_start <= other_range._range_end <= self._range_end
        )


class RoomRangeParser:
    @staticmethod
    def data_to_rooms(data: str):
        for line in data.splitlines():
            yield RoomRangeParser.from_task_line(line)

    @staticmethod
    def from_task_line(line):
        return [RoomRangeParser.parse(rrange) for rrange in line.split(",")]

    @staticmethod
    def parse(single_range):
        return RoomRange(*single_range.split("-"))


class Task4(Task):
    @staticmethod
    def solution_1(data):
        return sum(
            first.contains(second) or second.contains(first)
            for (first, second) in RoomRangeParser.data_to_rooms(data)
        )

    @staticmethod
    def solution_2(data):
        return sum(
            first.overlaps(second) or second.overlaps(first)
            for (first, second) in RoomRangeParser.data_to_rooms(data)
        )
