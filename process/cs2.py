from logging import info
from operator import itemgetter
from typing import Iterable, Optional, Type, Generator

from memprocfs import Vmm
from memprocfs.vmmpyc import VmmProcess, VmmModule

import lib.pyMeow as meow
from error import DeviceNotFoundError, ProcessNotFoundError, ProcessModuleNotFoundError
from lib.pyMeow import MeowProcess, MeowModule
from lib.pyMeow.pyMeow import process_exists
from process.memory import VmmMemoryReadStruct, MeowMemoryReadStruct, MemoryReadAbstract
from process.module import VmmModuleStruct, MeowModuleStruct, ModuleAbstract
from utils import dict2class, TimeUseCounter


class CS2:
    process: Optional[VmmProcess | MeowProcess] = None
    memory: Type[MemoryReadAbstract]

    client: ModuleAbstract
    engine2: ModuleAbstract
    schemasystem: ModuleAbstract

    offset: Type["offset.Offset"]

    @classmethod
    def setup_memprocfs(cls) -> Type["CS2"]:
        # get device
        try:
            vmm: Vmm = Vmm([
                '-device', 'fpga',
                '-disable-python', '-disable-symbols', '-disable-symbolserver', '-disable-yara',
                '-disable-yara-builtin',
                '-debug-pte-quality-threshold', '64'
            ])
        except Exception: raise DeviceNotFoundError
        else: info("Success Found Vmm Device.")

        # get cs2.exe process
        try: cls.process: VmmProcess = vmm.process('cs2.exe')
        except Exception: raise ProcessNotFoundError
        else: info("Success Found cs2.exe Process: pid->%s" % cls.process.pid)

        # get modules
        try:
            modules: Iterable[VmmModule] = cls.process.module_list()
            CS2.client, CS2.engine2, CS2.schemasystem = itemgetter(
                "client.dll",
                "engine2.dll",
                "schemasystem.dll",
            )({
                module.name: VmmModuleStruct(module)
                for module in modules
            })
        except Exception: raise ProcessModuleNotFoundError
        else: info("Success Found Modules: " + ", ".join([
            "%s->%s" % (module.name, module.base)
            for module in (
                cls.client,
                cls.engine2,
                cls.schemasystem
            )]))

        # setup memory read
        VmmMemoryReadStruct._process = cls.process
        cls.memory = VmmMemoryReadStruct

        return cls


    @classmethod
    def setup_pymeow(cls) -> Type["CS2"]:
        # get cs2.exe process
        if not process_exists("cs2.exe"):  raise ProcessNotFoundError
        try: cls.process: MeowProcess = meow.MeowProcess("cs2.exe")
        except Exception: raise ProcessNotFoundError
        else: info("Success Found cs2.exe Process: pid->%s" % cls.process.pid)

        # get modules
        try:
            modules: Generator[MeowModule, None, None] = cls.process.modules()
            CS2.client, CS2.engine2, CS2.schemasystem = itemgetter(
                "client.dll",
                "engine2.dll",
                "schemasystem.dll",
            )({
                module.name: MeowModuleStruct(module)
                for module in modules
            })
        except Exception: raise ProcessModuleNotFoundError
        else: info("Success Found Modules: " + ", ".join([
            "%s->%s" % (module.name, module.base)
            for module in (
                cls.client,
                cls.engine2,
                cls.schemasystem
            )]))

        # setup memory read
        MeowMemoryReadStruct._process = cls.process._process
        cls.memory = MeowMemoryReadStruct

        return cls

    @classmethod
    def update_offsets(cls) -> Type["CS2"]:
        from process.signature.dump import dump_signatures
        from process.schema.dump import dump_schemas
        from process.offset import Offset

        signatures = dump_signatures()
        schemas = dump_schemas()

        Offset.signatures = dict2class(signatures)
        Offset.schemas = dict2class(schemas)
        cls.offset: Type[Offset] = Offset

        return cls