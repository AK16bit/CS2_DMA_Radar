from logging import error
from struct import unpack, error as struct_error
from typing import Optional, Any, List, Union, override, Sequence, Callable

from memprocfs import FLAG_NOCACHE
from memprocfs.vmmpyc import VmmProcess

from lib.pyMeow.pyMeow import r_int8, r_int16, r_int, r_int64, r_uint16, r_uint, r_uint64, r_float, r_bool, r_bytes, r_string, r_floats
from lib.pyMeow.structure import StructMeowProcess
from utils import Vec2


class MemoryReadMonitor:
    enable: bool = True
    force_read: bool = False
    memory_read_count: int = 0
    memory_read_bytes: int = 0

    @staticmethod
    def memory_read_monitor_decorator(byte_size: int | None, *args) -> Callable:
        def decorator(func: Callable) -> Callable:
            def wrapper(*func_args, **func_kwargs) -> Any:
                if MemoryReadMonitor.enable:
                    if isinstance(byte_size, int): read_byte_size = byte_size
                    elif len(args) == 1:
                        key = args[0]
                        if isinstance(key, int): read_byte_size = func_args[key]
                        elif isinstance(key, str): read_byte_size = func_kwargs[key]
                        else: raise ValueError
                    else: raise ValueError

                    MemoryReadMonitor.memory_read_count += 1
                    MemoryReadMonitor.memory_read_bytes += read_byte_size


                try: return func(*func_args, **func_kwargs)
                except Exception as error_reason:
                    if MemoryReadMonitor.force_read: return None
                    else: raise error_reason

            return wrapper
        return decorator


    @classmethod
    def reset(cls) -> None:
        cls.memory_read_count = 0
        cls.memory_read_bytes = 0


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
    @MemoryReadMonitor.memory_read_monitor_decorator(None, 2)
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
        return cls.unpack_byte(cls.read_memory(address, 4 * size), "%if" % size)

    @classmethod
    def read_str(cls, address: int, byte_size: int = 50) -> Optional[str]:
        byte = cls.read_memory(address, byte_size).split(b"\x00")[0].decode("utf-8")
        return byte



class MeowMemoryReadStruct(MemoryReadAbstract):
    _process: StructMeowProcess

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(None, 2)
    def read_memory(cls, address: int, byte_size: int) -> Optional[Any]:
        return r_bytes(cls._process, address, byte_size)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(1)
    def read_bool(cls, address: int) -> Optional[bool]:
        return r_bool(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(1)
    def read_i8(cls, address: int) -> Optional[int]:
        return r_int8(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(2)
    def read_u16(cls, address: int) -> Optional[int]:
        return r_uint16(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(2)
    def read_i16(cls, address: int) -> Optional[int]:
        return r_int16(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(4)
    def read_i32(cls, address: int) -> Optional[int]:
        return r_int(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(4)
    def read_u32(cls, address: int) -> Optional[int]:
        return r_uint(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(8)
    def read_i64(cls, address: int) -> Optional[int]:
        return r_int64(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(8)
    def read_u64(cls, address: int) -> Optional[int]:
        return r_uint64(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(4)
    def read_f32(cls, address: int) -> Optional[float]:
        return r_float(cls._process, address)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(None, 2)
    def read_vec(cls, address: int, size: int) -> Sequence[float]:
        return r_floats(cls._process, address, size)

    @classmethod
    @MemoryReadMonitor.memory_read_monitor_decorator(None, 2)
    def read_str(cls, address: int, byte_size: int = 50) -> Optional[str]:
        try: string = r_string(cls._process, address, byte_size)
        except Exception: return None
        if not isinstance(string, str): return None

        return string
