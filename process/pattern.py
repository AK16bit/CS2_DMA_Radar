from logging import debug
from re import search
from struct import unpack
from typing import Self, Optional

from memprocfs import FLAG_NOCACHE

from error import PatternConvertError
from process.address import Address
from process.cs2 import CS2
from process.memory import VmmMemoryReadStruct


class Pattern:
    def __init__(self, pattern: str):
        self.pattern = pattern
        self._address: Optional[int] = None

    @property
    def address(self) -> int:
        return self._address

    def to_Address(self) -> Address:
        return Address(self._address)

    @staticmethod
    def pattern_str_to_regex_bytes(pattern: str) -> bytes:
        return rb"".join([
            rb"[\s\S]{1}" if "?" in hex_byte else rb"\x" + hex_byte.encode("utf-8")
            for hex_byte in pattern.split(" ")
        ])

    def search(self, module_base: int, module_buffer: bytes) -> Self:
        try:
            pattern_bytes = self.pattern_str_to_regex_bytes(self.pattern)
            match_offset = search(pattern_bytes, module_buffer)

            if match_offset is None: raise PatternConvertError(self.pattern, pattern_bytes)
            self._address = module_base + match_offset.start()
        except PatternConvertError as error: raise error
        except Exception as error_reason: raise PatternConvertError(self.pattern, error_reason)

        return self

    def add(self, value: int) -> Self:
        self._address += value
        return self

    def rip(self, offset: int = 3, length: int = 7) -> Self:
        self._address = self._address + CS2.memory.read_i32(self._address + offset) + length
        return self

    def slice(self, start: int, end: int) -> Self:
        byte = CS2.memory.read_memory(self._address + start, end - start)
        self._address = int.from_bytes(byte, "little")

        return self