from memprocfs.vmmpyc import VmmModule
from lib.pyMeow import MeowModule


class ModuleAbstract:
    _module: VmmModule | MeowModule

    @property
    def name(self) -> str: ...

    @property
    def base(self) -> int: ...

    @property
    def size(self) -> int: ...



class VmmModuleStruct(ModuleAbstract):
    def __init__(self, module: VmmModule):
        self._module: VmmModule = module

    @property
    def name(self) -> str: return self._module.name

    @property
    def base(self) -> int: return self._module.base

    @property
    def size(self) -> int: return self._module.image_size


class MeowModuleStruct(ModuleAbstract):
    def __init__(self, module: MeowModule):
        self._module: MeowModule = module

    @property
    def name(self) -> str: return self._module.name

    @property
    def base(self) -> int: return self._module.base

    @property
    def size(self) -> int: return self._module.size