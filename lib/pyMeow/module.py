from typing import Union, Any, Optional, List

from lib.pyMeow.pyMeow import open_process, module_exists, get_module, aob_scan_module, r_bytes
from lib.pyMeow.structure import StructMeowProcess, StructMeowModule


class MeowModule:
    def __init__(self, process: Union[str, int, StructMeowProcess], module: Union[str, StructMeowModule]):
        if isinstance(process, str) or isinstance(process, int):
            self.process = open_process(process)
        else:
            self.process = process

        if isinstance(module, str):
            if not module_exists(self.process, module): raise
            self.module = get_module(self.process, module)
        else:
            self.module = module

    def __getitem__(self, item: str) -> Any: return self.module.get(item, None)
    def __repr__(self) -> str: return str(self.module)

    @property
    def name(self) -> str: return self.module.get("name")

    @property
    def base(self) -> int: return self.module.get("base")

    @property
    def end(self) -> int: return self.module.get("end")

    @property
    def size(self) -> int: return self.module.get("size")

    @property
    def buffer(self) -> bytes: return r_bytes(self.process, self.base, self.size)
