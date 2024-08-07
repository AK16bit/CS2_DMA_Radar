from logging import error
from struct import unpack, error as struct_error
from typing import Optional, Any, List, Union, override, Sequence

from memprocfs import FLAG_NOCACHE
from memprocfs.vmmpyc import VmmProcess

from lib.pyMeow.pyMeow import r_int8, r_int16, r_int, r_int64, r_uint16, r_uint, r_uint64, r_float, r_bool, r_bytes, r_string, r_floats
from lib.pyMeow.structure import StructMeowProcess


class MemoryReadAbstract:
    _process: VmmProcess | StructMeowProcess

    @staticmethod
    def unpack_byte(byte: bytes, format_str: str) -> Optional[Any]:
        try:
            return unpack("<" + format_str, byte)[0]
        except Exception as error_reason:
            error("UnpackByteError: (byte: %s, format_str: %s, error: %s)" % (byte, "<" + format_str, error_reason))
            raise
        #     return None
        # except TypeError: return None
        # except Exception: raise "something is wrong..."

    @classmethod
    def read_memory(cls, address: int, byte_size: int) -> Optional[bytes]: ...

    @classmethod
    def read_bool(cls, address: int) -> Optional[bool]: ...

    @classmethod
    def read_i8(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_u16(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_i16(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_i32(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_u32(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_i64(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_u64(cls, address: int) -> Optional[int]: ...

    @classmethod
    def read_f32(cls, address: int) -> Optional[float]: ...

    @classmethod
    def read_vec(cls, address: int, vec_size: int) -> Optional[Sequence[float]]: ...

    @classmethod
    def read_str(cls, address: int, byte_size: int) -> Optional[str]: ...



class VmmMemoryReadStruct(MemoryReadAbstract):
    _process: VmmProcess

    @classmethod
    def read_memory(cls, address: int, byte_size: int) -> Optional[bytes]:
        byte = cls._process.memory.read(address, byte_size, FLAG_NOCACHE)
        if not byte:
            error("ReadMemoryError: (address: %s, byte_size:%s, read_value: %s)" % (address, byte_size, byte))
            # return None
        return byte

    @classmethod
    def read_bool(cls, address: int) -> Optional[bool]:
        return cls.unpack_byte(cls.read_memory(address, 1), "?")

    @classmethod
    def read_i8(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 2), "b")

    @classmethod
    def read_u8(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 2), "B")

    @classmethod
    def read_i16(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 2), "h")

    @classmethod
    def read_u16(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 2), "H")

    @classmethod
    def read_i32(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 4), "i")

    @classmethod
    def read_u32(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 4), "I")

    @classmethod
    def read_i64(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 8), "q")

    @classmethod
    def read_u64(cls, address: int) -> Optional[int]:
        return cls.unpack_byte(cls.read_memory(address, 8), "Q")

    @classmethod
    def read_f32(cls, address: int) -> Optional[float]:
        return cls.unpack_byte(cls.read_memory(address, 4), "f")

    @classmethod
    def read_vec(cls, address: int, size: int) -> Optional[Sequence[float]]:
        ...

    @classmethod
    def read_str(cls, address: int, byte_size: int = 50) -> Optional[str]:
        byte = cls.read_memory(address, byte_size).split(b"\x00")[0].decode("utf-8")
        return byte



class MeowMemoryReadStruct(MemoryReadAbstract):
    _process: StructMeowProcess

    @classmethod
    def read_memory(cls, address: int, size: int) -> Optional[Any]:
        return r_bytes(cls._process, address, size)

    @classmethod
    def read_bool(cls, address: int) -> Optional[bool]:
        return r_bool(cls._process, address)

    @classmethod
    def read_i8(cls, address: int) -> Optional[int]:
        return r_int8(cls._process, address)

    @classmethod
    def read_u16(cls, address: int) -> Optional[int]:
        return r_uint16(cls._process, address)

    @classmethod
    def read_i16(cls, address: int) -> Optional[int]:
        return r_int16(cls._process, address)

    @classmethod
    def read_i32(cls, address: int) -> Optional[int]:
        return r_int(cls._process, address)

    @classmethod
    def read_u32(cls, address: int) -> Optional[int]:
        return r_uint(cls._process, address)

    @classmethod
    def read_i64(cls, address: int) -> Optional[int]:
        return r_int64(cls._process, address)

    @classmethod
    def read_u64(cls, address: int) -> Optional[int]:
        return r_uint64(cls._process, address)

    @classmethod
    def read_f32(cls, address: int) -> Optional[float]:
        return r_float(cls._process, address)

    @classmethod
    def read_vec(cls, address: int, size: int) -> Sequence[float]:
        return r_floats(cls._process, address, size)

    @classmethod
    def read_str(cls, address: int, byte_size: int = 50) -> Optional[str]:
        try: string = r_string(cls._process, address, byte_size)
        except Exception: return None
        if not isinstance(string, str): return None

        return string
