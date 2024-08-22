from functools import wraps
from logging import warning
from typing import Self, Optional, Dict, Any, Callable

from process.cs2 import CS2



class AddressMemoryRead:
    address: int
    _cache: Dict[int, Dict[str, Any]] = dict()

    @staticmethod
    def _address_caching_decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(address_object: "AddressMemoryRead", *args, **kwargs) -> Any:
            try:
                memory_type = func.__name__

                # from BasaGanniDarr
                value: Optional[Any] = None
                if AddressMemoryRead._cache.get(address_object.address, None) is not None:
                    value = AddressMemoryRead._cache.get(address_object.address).get(memory_type, None)
                    # print("read cache: %s, %s" % (memory_type, address_object.address))

                if value is None:
                    value = func(address_object, *args, **kwargs)
                    AddressMemoryRead._cache.update({address_object.address: {memory_type: value}})
                    # print("wrote cache: %s, %s" % (memory_type, address_object.address))
            except Exception:
                value = func(address_object, *args, **kwargs)
                # warning("Can't Cache Address: %s" % address_object.address)

            return value
        return wrapper

    @classmethod
    def clear_address_cache(cls, target_address: Optional[int] = None) -> None:
        if target_address is None: cls._cache.clear()
        else: cls._cache.pop(target_address)

    @_address_caching_decorator
    def bool(self) -> Optional[bool]: return CS2.memory.read_bool(self.address)

    @_address_caching_decorator
    def i8(self) -> Optional[int]: return CS2.memory.read_i8(self.address)

    @_address_caching_decorator
    def u8(self) -> Optional[int]: return CS2.memory.read_u8(self.address)

    @_address_caching_decorator
    def i16(self) -> Optional[int]: return CS2.memory.read_i16(self.address)

    @_address_caching_decorator
    def u16(self) -> Optional[int]: return CS2.memory.read_u16(self.address)

    @_address_caching_decorator
    def i32(self) -> Optional[int]: return CS2.memory.read_i32(self.address)

    @_address_caching_decorator
    def u32(self) -> Optional[int]: return CS2.memory.read_u32(self.address)

    @_address_caching_decorator
    def i64(self) -> Optional[int]: return CS2.memory.read_i64(self.address)

    @_address_caching_decorator
    def u64(self) -> Optional[int]: return CS2.memory.read_u64(self.address)

    @_address_caching_decorator
    def float(self) -> Optional[float]: return CS2.memory.read_f32(self.address)


class Address(AddressMemoryRead):
    def __init__(self, address: int):
        self.address = address

    def __repr__(self) -> str:
        return "Address(%s / %s)" % (self.address, hex(self.address))

    def __eq__(self, other: int | Self) -> bool:
        if isinstance(other, int): return self.address == other
        if isinstance(other, Address): return self.address == other.address
        return False

    def offset(self, value: int) -> Self:
        self.address += value
        return self

    def pointer(self) -> "Address":
        return Address(self.u64())

    def copy(self) -> "Address":
        return Address(self.address)



