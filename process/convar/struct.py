from typing import Optional

from process.convar.offset import Offset
from process.cs2 import CS2


class StructConvar:
    def __init__(self, address: int):
        self.address = address

    def name(self) -> Optional[str]:
        if not (name_address := CS2.memory.read_u64(self.address + Offset.StructConvar.NAME)): return None
        return CS2.memory.read_str(name_address, 64)
    def description(self, byte: int) -> Optional[str]:
        if not (description_address := CS2.memory.read_u64(self.address + Offset.StructConvar.DESCRIPTION)): return None
        return CS2.memory.read_str(description_address, byte)
    def int(self) -> int: return CS2.memory.read_i32(self.address + Offset.StructConvar.VALUE)
    def float(self) -> float: return CS2.memory.read_f32(self.address + Offset.StructConvar.VALUE)


class StructConvarSystem:
    def __init__(self, convar_system_address):
        self.convar_system_address = convar_system_address
        self.convar_base_address = None

    def base_address(self) -> Optional[int]:
        if self.convar_base_address is None:
            self.convar_base_address = CS2.memory.read_u64(self.convar_system_address + Offset.StructConvarSystem.CONVAR_BASE)
        return self.convar_base_address

    def convar_count(self) -> Optional[int]:
        return CS2.memory.read_u16(self.convar_system_address + Offset.StructConvarSystem.CONVAR_COUNT)

    def convar_address(self, index: int) -> Optional[int]:
        return CS2.memory.read_u64(self.base_address() + index * Offset.StructConvarSystem.CONVAR_BASE_INDEX)