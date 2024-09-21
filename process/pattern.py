from logging import debug
from re import search
from struct import unpack
from typing import Self, Optional

from memprocfs import FLAG_NOCACHE

from error import PatternConvertError
from process.address import Address
from process.cs2 import CS2


class PatternVerA2X:
    def __init__(self, pattern: str, module_base: int, module_buffer: bytes):
        self.pattern = pattern

        self._module_base = module_base
        self._module_buffer = module_buffer

        self._pattern_offset: int

    @property
    def address(self) -> int:
        return self._module_base + self._pattern_offset

    def to_Address(self) -> Address:
        return Address(self._module_base + self._pattern_offset)

    @property
    def offset(self) -> int:
        return self._pattern_offset

    @staticmethod
    def pattern_str_to_regex_bytes(pattern: str) -> bytes:
        return rb"".join([
            rb"[\s\S]{1}" if "?" in hex_byte else rb"\x" + hex_byte.encode("utf-8")
            for hex_byte in pattern.split(" ")
        ])

    def aob_scan(self, auto_trans_2_regex: bool = True) -> Self:
        try:
            if auto_trans_2_regex: pattern_match_bytes = self.pattern_str_to_regex_bytes(self.pattern)
            else: pattern_match_bytes = self.pattern
            match_offset = search(pattern_match_bytes, self._module_buffer)

            if match_offset is None: raise PatternConvertError(self.pattern, pattern_match_bytes)
            self._pattern_offset = match_offset.start()
            return self

        except PatternConvertError as error: raise error
        except Exception as error_reason: raise PatternConvertError(self.pattern, error_reason)


    def pattern_bytes(self, offset: int, size: int) -> bytes:
        return self._module_buffer[self._pattern_offset + offset:self._pattern_offset + offset + size]


    def add(self, value: int) -> Self:
        self._pattern_offset += value
        return self

    def rip(self, offset: int = 3, length: int = 7) -> Self:
        self._pattern_offset = self._pattern_offset + CS2.memory.unpack_byte(self.pattern_bytes(offset, 4), "I") + length
        return self

    def slice(self, start: int, end: int) -> Self:
        byte = self.pattern_bytes(start, end - start)
        self._pattern_offset = int.from_bytes(byte, "little")

        return self


class PatternVerOsiris:
    def __init__(self, pattern: str, module_base: int, module_buffer: bytes) -> None:
        self.pattern = pattern
        self.module_base = module_base
        self.module_buffer = module_buffer

        self.pattern_offset = self.aob_scan()
        self.extra_offset = 0

        # print(self.module_base + self.pattern_offset)
        # print(self.pattern_bytes)
        # print(self.pattern_bytes, self.pattern_bytes[3:3 + 4], self.module_base + self.pattern_offset, self.module_base + self.pattern_offset + CS2.memory.unpack_byte(self.pattern_bytes[3:3 + 4], "i") + 7)


    @staticmethod
    def pattern_str_to_regex_bytes(pattern: str) -> bytes:
        return rb"".join([
            rb"[\s\S]{1}" if "?" in hex_byte else rb"\x" + hex_byte.encode("utf-8")
            for hex_byte in pattern.split(" ")
        ])

    def aob_scan(self) -> int:
        try:
            pattern_match_bytes = self.pattern_str_to_regex_bytes(self.pattern)
            match_offset = search(pattern_match_bytes, self.module_buffer)

            if match_offset is None: raise PatternConvertError(self.pattern, pattern_match_bytes)
            return match_offset.start()

        except PatternConvertError as error: raise error
        except Exception as error_reason: raise PatternConvertError(self.pattern, error_reason)

    @property
    def pattern_bytes(self) -> int:
        return self.module_buffer[self.pattern_offset:self.pattern_offset + self.extra_offset + 0x08]

    def add(self, value: int) -> Self:
        self.extra_offset += value
        return self

    def abs_read(self, next_offset_size: int = 4) -> Address:
        offset = CS2.memory.unpack_byte(self.pattern_bytes[self.extra_offset:self.extra_offset + next_offset_size], "I")
        return Address(self.module_base + self.pattern_offset + offset + self.extra_offset + next_offset_size)

    def ofs_read(self, size: int = 4) -> Address:
        if size not in (0x4, 0x8): raise ValueError
        return Address(CS2.memory.unpack_byte(self.pattern_bytes[self.extra_offset:self.extra_offset + size], "Q" if size == 0x08 else "I"))



    # def as(self) -> Address:
    #     return Address(self.module_base + self.pattern_offset + self.extra_offset)
