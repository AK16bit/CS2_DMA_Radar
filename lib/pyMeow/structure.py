from typing import TypedDict

__all__ = [
    "StructMeowProcess", "StructMeowModule"
]

class StructMeowProcess(TypedDict):
    name: str
    pid: int
    debug: bool
    handle: int
class StructMeowModule(TypedDict):
    name: str
    base: int
    end: int
    size: int
class StructMeowColor(TypedDict):
    r: int
    g: int
    b: int
    a: int
class StructMeowRectangle(TypedDict):
    x: float
    y: float
    width: float
    height: float
class StructMeowTexture(TypedDict):
    id: int
    width: int
    height: int
    mipmaps: int
    format: int