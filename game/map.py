from json import dumps, loads
from os.path import join
from typing import Self, Optional

from process.address import Address
from process.cs2 import CS2
from utils import Vec2, Vec3


class Map:
    map_name: str
    map_meta: dict


    @classmethod
    def update(cls) -> Self:
        cls.map_name = cls.get_map_name()
        cls.map_meta = cls.get_map_meta(cls.map_name)

        return cls

    @classmethod
    def world_2_map(cls, world_pos: Vec3) -> Vec2:
        #   o-------> x
        #   |
        #   |
        #   v
        #   y

        return Vec2(
            (world_pos.x - cls.map_meta.get("x")) / cls.map_meta.get("scale"),
            (cls.map_meta.get("y") - world_pos.y) / cls.map_meta.get("scale"),
        )

    @staticmethod
    def get_map_name() -> Optional[str]:
        global_var_address: Address = CS2.offset.signatures.client.dwGlobalVars.pointer()
        map_name_address = global_var_address.offset(0x1B8).pointer()

        map_name = map_name_address.str(50)
        return map_name

    @staticmethod
    def get_map_path(map_name: str) -> str:
        return join("maps", "%s.png" % map_name)

    @staticmethod
    def get_map_meta(map_name: Optional[str] = None) -> dict:
        with open(join("maps", "map_meta.json"), "r") as map_meta_file: map_meta = loads(map_meta_file.read())
        if map_name is None: return map_meta

        curr_map_meta: dict = map_meta.get(map_name, dict(x=None, y=None, scale=None))
        return curr_map_meta

