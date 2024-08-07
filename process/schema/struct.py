from typing import Optional

from process.cs2 import CS2
from process.schema.offset import Offset


class StructField:
    def __init__(self, field_address):
        self.field_address = field_address

    @property
    def name(self) -> Optional[str]:
        strAddr = CS2.memory.read_u64(self.field_address + Offset.StructField.NAME)
        return CS2.memory.read_str(strAddr, 128)

    @property
    def schema_type(self) -> Optional[int]:
        return CS2.memory.read_u64(self.field_address + Offset.StructField.SCHEMA_TYPE)

    @property
    def value(self) -> Optional[int]:
        return CS2.memory.read_i32(self.field_address + Offset.StructField.VALUE)


class StructClass:
    def __init__(self, class_address: int):
        self.class_address = class_address

    @property
    def name(self) -> Optional[str]:
        str_address = CS2.memory.read_u64(self.class_address + Offset.StructClass.NAME)
        return CS2.memory.read_str(str_address, 128)

    @property
    def module_name(self) -> Optional[str]:
        str_address = CS2.memory.read_u64(self.class_address + Offset.StructClass.MODULE_NAME)
        return CS2.memory.read_str(str_address, 128)


    @property
    def fields_count(self) -> Optional[int]:
        return CS2.memory.read_i16(self.class_address + Offset.StructClass.FIELDS_COUNT)

    @property
    def static_fields_count(self) -> Optional[int]:
        return CS2.memory.read_i16(self.class_address + Offset.StructClass.STATIC_FIELDS_COUNT)

    # @property
    # def static_metadata_count(self) -> Optional[int]:
    #     return CS2.memory.read_i16(self.class_address + Offset.StructClass.STATIC_METADATA_COUNT)

    @property
    def fields(self) -> Optional[int]:
        return CS2.memory.read_u64(self.class_address + Offset.StructClass.FIELDS)

    @property
    def static_fields(self) -> Optional[int]:
        return CS2.memory.read_u64(self.class_address + Offset.StructClass.STATIC_FIELDS)

    @property
    def has_base_class(self) -> Optional[bool]:
        return CS2.memory.read_bool(self.class_address + Offset.StructClass.HAS_BASE_CLASS)

    @property
    def base_class_address(self) -> Optional[int]:
        base_class_address = CS2.memory.read_u64(self.class_address + Offset.StructClass.BASE_ADDRESS)
        return CS2.memory.read_u64(base_class_address + Offset.StructClass.FIELDS_INDEX)



class StructAllocatedClassBase:
    def __init__(self, allocated_address: int):
        self.allocated_address = allocated_address

    @property
    def next(self) -> Optional[int]:
        return CS2.memory.read_u64(self.allocated_address + Offset.StructTSHash.StructHashBucket.StructAllocateClassBase.NEXT)

    @property
    def data(self) -> Optional[int]:
        return CS2.memory.read_u64(self.allocated_address + Offset.StructTSHash.StructHashBucket.StructAllocateClassBase.DATA)


class StructUnAllocatedClassBase:
    def __init__(self, unallocated_address):
        self.unallocated_address = unallocated_address

    @property
    def next(self) -> Optional[int]:
        return CS2.memory.read_u64(self.unallocated_address + Offset.StructTSHash.StructHashBucket.StructUnAllocateClassBase.NEXT)

    @property
    def data(self) -> Optional[int]:
        return CS2.memory.read_u64(self.unallocated_address + Offset.StructTSHash.StructHashBucket.StructUnAllocateClassBase.DATA)


class StructMemoryPool:
    def __init__(self, memory_pool_address: int):
        self.memory_pool_address = memory_pool_address

    @property
    def block_size(self) -> Optional[int]:
        return CS2.memory.read_i32(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.BLOCK_SIZE)

    @property
    def blocks_per_blob(self) -> Optional[int]:
        return CS2.memory.read_i32(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.BLOCKS_PER_BLOB)

    @property
    def grow_mode(self) -> Optional[int]:
        return CS2.memory.read_i32(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.GROW_MODE)

    @property
    def blocks_alloc(self) -> Optional[int]:
        return CS2.memory.read_i32(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.BLOCKS_ALLOC)

    @property
    def peak_alloc(self) -> Optional[int]:
        return CS2.memory.read_i32(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.PEAK_ALLOC)

    @property
    def blobs_count(self) -> Optional[int]:
        return CS2.memory.read_u16(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.BLOBS_COUNT)

    @property
    def free_list_tail(self) -> Optional[int]:
        return CS2.memory.read_u64(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.FREE_LIST_TAIL)

    @property
    def free_list_head(self) -> Optional[int]:
        return CS2.memory.read_u64(self.memory_pool_address + Offset.StructTSHash.StructMemoryPool.FREE_LIST_HEAD)




class StructHashBucket:
    def __init__(self, hash_bucket_address: int):
        self.hash_bucket_address = hash_bucket_address

    @property
    def first(self) -> Optional[int]:
        return CS2.memory.read_u64(self.hash_bucket_address + Offset.StructTSHash.StructHashBucket.FIRST)

    @property
    def first_uncomm(self) -> Optional[int]:
        return CS2.memory.read_u64(self.hash_bucket_address + Offset.StructTSHash.StructHashBucket.FIRST_UNCOMM)


class StructModule:
    def __init__(self, module_address: int):
        self.module_address = module_address

    @property
    def name(self) -> str:
        return CS2.memory.read_str(self.module_address + Offset.StructModule.NAME, 20)

    @property
    def class_bindings_address(self) -> int:
        return self.module_address + Offset.StructModule.CLASS_BINDINGS

    @property
    def enum_binding_address(self) -> int:
        return self.module_address + Offset.StructModule.ENUM_BINDINGS

    def memory_pool_address(self, binding_address: int) -> int:
        return binding_address + Offset.StructTSHash.MEMORY_POOL

    def hash_bucket_address(self, binding_address: int, index: int) -> int:
        return binding_address + Offset.StructTSHash.HASH_BUCKET + index * Offset.StructTSHash.HASH_BUCKET_INDEX


class StructSchemaSystem:
    def __init__(self, schema_system_address: int):
        self.schema_system_address = schema_system_address

    @property
    def base_address(self) -> Optional[int]:
        return CS2.memory.read_u64(self.schema_system_address + Offset.StructSchemaSystem.MODULE_BASE)

    @property
    def modules_count(self) -> Optional[int]:
        return CS2.memory.read_u32(self.schema_system_address + Offset.StructSchemaSystem.MODULES_COUNT)

    def module_address(self, index: int) -> Optional[int]:
        return CS2.memory.read_u64(self.base_address + index * Offset.StructSchemaSystem.MODULE_BASE_INDEX)