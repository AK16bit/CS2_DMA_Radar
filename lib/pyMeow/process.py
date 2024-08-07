# from BasaGanniDarr.Util.debug import Debugger
from error import ProcessNotFoundError
from utils import Vec2, Vec3
from lib.pyMeow.pyMeow import r_ctype, process_running, enum_modules, open_process, process_exists, pid_exists, r_bytes, \
    r_string, r_floats

from typing import Union, Generator, Any, Optional, Callable, Sequence

from lib.pyMeow.module import MeowModule


class MeowProcess:
    def __init__(self, process: str):
        self._process = open_process(process)

    def __getitem__(self, item: str) -> Any: return self._process.get(item, None)
    def __repr__(self) -> str: return str(self._process)

    @property
    def name(self) -> str: return self._process.get("name")

    @property
    def pid(self) -> int: return self._process.get("pid")

    @property
    def handle(self) -> int: return self._process.get("handle")

    def modules(self) -> Generator[MeowModule, None, None]:
        modules = enum_modules(self._process)
        for module_struct in modules: yield MeowModule(self._process, module_struct)
