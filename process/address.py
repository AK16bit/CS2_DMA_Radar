from typing import Self, Any, Optional

from process.cs2 import CS2


class AddressMemoryRead:
    address: int

    def bool(self) -> Optional[int]: return CS2.memory.read_bool(self.address)
    def i8(self) -> Optional[int]: return CS2.memory.read_i8(self.address)
    def u8(self) -> Optional[int]: return CS2.memory.read_u8(self.address)
    def i16(self) -> Optional[int]: return CS2.memory.read_i16(self.address)
    def u16(self) -> Optional[int]: return CS2.memory.read_u16(self.address)
    def i32(self) -> Optional[int]: return CS2.memory.read_i32(self.address)
    def u32(self) -> Optional[int]: return CS2.memory.read_u32(self.address)
    def i64(self) -> Optional[int]: return CS2.memory.read_i64(self.address)
    def u64(self) -> Optional[int]: return CS2.memory.read_u64(self.address)
    def float(self) -> Optional[int]: return CS2.memory.read_f32(self.address)


class Address(AddressMemoryRead):
    def __init__(self, address: int):
        self.address = address

    def offset(self, value: int) -> Self:
        self.address += value
        return self


