from dataclasses import dataclass
from logging import DEBUG, getLogger, StreamHandler, ERROR, WARNING, INFO, Formatter, Logger
from math import sqrt, degrees, atan2
from time import perf_counter
from typing import Dict, Optional, Union, Self, List, Sequence
from threading import Timer

from process.memory import MemoryReadMonitor


@dataclass
class Vec2:
    x: float = .0
    y: float = .0


    @classmethod
    def from_list(cls, input_value: Sequence[Optional[float]]) -> "Vec2":
        if not len(input_value) == 2: raise ValueError

        return Vec2(*input_value)

    @classmethod
    def from_dict(cls, input_value: Dict[str, Optional[float]]) -> "Vec2":
        return Vec2(
            input_value.get("x", .0),
            input_value.get("y", .0)
        )

    def to_list(self) -> list:
        return [self.x, self.y]

    def to_dict(self) -> dict:
        return dict(x=self.x, y=self.y)

    def __add__(self, other) -> "Vec2":
        if not isinstance(other, Vec2): return NotImplemented

        return Vec2(
            self.x + other.x,
            self.y + other.y
        )

    def __sub__(self, other) -> Self:
        if not isinstance(other, Vec2): return NotImplemented

        return Vec2(
            self.x - other.x,
            self.y - other.y
        )

    def distance(self, vec2: "Vec2") -> float:
        oppPos = self - vec2

        distance = sqrt(sum((
            oppPos.x ** 2,
            oppPos.y ** 2
        )))
        return distance

    def angle(self, vec2: "Vec2") -> float:
        oppPos = self - vec2

        angle = atan2(oppPos.y, oppPos.x)
        degree = degrees(angle)
        return degree


@dataclass
class Vec3:
    x: float = .0
    y: float = .0
    z: float = .0

    def __repr__(self):
        return "Vec3(%f, %f, %f)" % (self.x, self.y, self.z)

    def __getitem__(self, item: Union[str, int]) -> Optional[float]:
        return {
            0: self.x,
            1: self.y,
            2: self.z,
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }.get(item, None)

    @classmethod
    def from_list(cls, input_value: Sequence[Optional[float]]) -> "Vec3":
        if not len(input_value) == 3: raise ValueError

        return Vec3(*input_value)

    @classmethod
    def from_dict(cls, input_value: Dict[str, Optional[float]]) -> "Vec3":
        return Vec3(
            input_value.get("x", .0),
            input_value.get("y", .0),
            input_value.get("z", .0)
        )

    def to_list(self) -> list:
        return [self.x, self.y, self.z]

    def to_dict(self) -> dict:
        return dict(x=self.x, y=self.y, z=self.z)

    def __add__(self, other) -> "Vec3":
        if not isinstance(other, Vec3): return NotImplemented

        x = self.x + other.x
        y = self.y + other.y
        z = self.z + other.z
        return Vec3(x, y, z)

    def __sub__(self, other) -> "Vec3":
        if not isinstance(other, Vec3): return NotImplemented

        x = self.x - other.x
        y = self.y - other.y
        z = self.z - other.z
        return Vec3(x, y, z)

    def __truediv__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.x / other.x,
            self.y / other.y,
            self.z / other.z,
        )

    def __floordiv__(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        )

    def distance(self, vec3: "Vec3") -> float:
        oppPos = self - vec3

        distance = sqrt(sum((
            oppPos.x ** 2,
            oppPos.y ** 2,
            oppPos.z ** 2
        )))
        return distance

    def normalize(self) -> "Vec3":
        # length = linalg.norm((self.x, self.y, self.z))
        length = sqrt(sum((self.x ** 2, self.y ** 2, self.z ** 2)))
        # if length == 0: return copy(self)
        return Vec3(
            self.x / length,
            self.y / length,
            self.z / length
        )

    def cross(self, other: "Vec3") -> "Vec3":
        return Vec3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def dot(self, other: "Vec3") -> float:
        return sum((
            self.x * other.x,
            self.y * other.y,
            self.z * other.z,
        ))


def logger_setup() -> Logger:
    class ColoredFormatter(Formatter):
        def format(self, record):
            record.levelname = {
                DEBUG: f'\033[95m[{record.levelname}]\033[0m',
                INFO: f'\033[92m[{record.levelname}]\033[0m',
                WARNING: f'\033[93m[{record.levelname}]\033[0m',
                ERROR: f'\033[91m[{record.levelname}]\033[0m',
            }.get(record.levelno, record.levelname)

            return super().format(record)

    handler = StreamHandler()
    handler.setFormatter(ColoredFormatter(" ".join((
        "%(levelname)s",
        # "\033[1;32m[%(asctime)s]\033[0m",
        # "\033[1;35m[%(filename)s:%(lineno)s]\033[0m",
        # "\033[1;35m[%(filename)s]\033[0m",
        "\033[1;97m%(message)s\033[0m",
    ))))

    logger = getLogger()
    logger.addHandler(handler)
    logger.setLevel(DEBUG)
    return logger


def dict2class(a: dict):
    return type("", (), {
        **dict(__dict__=a),
        **{
            key: dict2class(item) if isinstance(item, dict) else item
            for key, item in a.items()
        }
    })()


class RepeatThread(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


class TimeUsedCounter:
    def __init__(self, time_list: Sequence = None) -> None:
        self.time_list = list() if time_list is None else time_list

    def __enter__(self) -> None:
        self.start_time = perf_counter()

    def __exit__(self, _, __, ___) -> None:
        time_used = perf_counter() - self.start_time
        self.time_list.append(time_used)

        print("time used: %s ms" % (time_used * 1000))


class RunningDebugger:
    max_index = 128
    time_used = list()
    memory_read_count = list()
    memory_read_bytes = list()

    @classmethod
    def update_time_used(cls) -> Self:
        if len(cls.time_used) > cls.max_index:
            cls.time_used = cls.time_used[slice(-cls.max_index, len(cls.time_used))]
        return cls

    @classmethod
    def update_memory_read(cls) -> Self:
        cls.memory_read_count.append(MemoryReadMonitor.memory_read_count)
        if len(cls.memory_read_count) > cls.max_index:
            cls.memory_read_count = cls.memory_read_count[slice(-cls.max_index, len(cls.memory_read_count))]

        cls.memory_read_bytes.append(MemoryReadMonitor.memory_read_bytes)
        if len(cls.memory_read_bytes) > cls.max_index:
            cls.memory_read_bytes = cls.memory_read_bytes[slice(-cls.max_index, len(cls.memory_read_bytes))]

        return cls


    @classmethod
    @property
    def time_used_mean(cls) -> float:
        if len(cls.time_used):
            return sum(cls.time_used) / len(cls.time_used)
        return 0

    @classmethod
    @property
    def memory_read_count_mean(cls) -> int:
        if len(cls.memory_read_count):
            return int(sum(cls.memory_read_count) / len(cls.memory_read_count))
        return 0

    @classmethod
    @property
    def memory_read_bytes_mean(cls) -> float:
        if len(cls.memory_read_bytes):
            return sum(cls.memory_read_bytes) / len(cls.memory_read_bytes)
        return 0
