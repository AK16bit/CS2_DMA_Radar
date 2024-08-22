from dataclasses import dataclass
from logging import DEBUG, getLogger, StreamHandler, ERROR, WARNING, INFO, Formatter, Logger
from math import sqrt, degrees, atan2
from typing import Dict, Optional, Union, Self


@dataclass
class Vec2:
    x: float = .0
    y: float = .0

    @classmethod
    def fromDict(cls, dict: Dict[str, Optional[float]]) -> "Vec2":
        x: float = dict.get("x", None)
        y: float = dict.get("y", None)
        if None in (x, y): raise ValueError()

        return Vec2(x, y)

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
    def fromDict(cls, dict: Dict[str, Optional[float]]) -> "Vec3":
        x: float = dict.get("x", None)
        y: float = dict.get("y", None)
        z: float = dict.get("z", None)
        if None in (x, y, z): raise ValueError()

        return Vec3(x, y, z)

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