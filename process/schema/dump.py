from logging import info
from typing import Optional, Generator, List, Dict, Union


from error import PatternConvertError, SchemaModuleDumpError, SchemaClassDumpError
from process.schema.offset import Offset
from process.schema.struct import StructSchemaSystem, StructModule, StructMemoryPool, StructAllocatedClassBase, \
    StructHashBucket, StructUnAllocatedClassBase, StructClass, StructField
from process.pattern import Pattern
from process.cs2 import CS2


def dump_schemas() -> Dict[str, Dict[str, Dict[str, int]]]:
    try:
        schema_system_address = read_schema_system_address()
        schema_system_struct = StructSchemaSystem(schema_system_address)
    except Exception: raise PatternConvertError

    modules_count = schema_system_struct.modules_count
    modules_address: Generator[int, None, None] = (schema_system_struct.module_address(index) for index in range(modules_count))

    schema = dict()
    for module_address in modules_address:
        try: module_data = read_module(module_address)
        except Exception: raise SchemaModuleDumpError

        module_name = module_data.get("module_struct").name
        if module_name not in ("client.dll", "engine2.dll"): continue
        # print(module_name)

        try:
            classes_list = [read_class(class_address) for class_address in module_data.get("classes_address")]
            classes = {
                class_name: class_fields
                for class_offset in classes_list
                for class_name, class_fields in class_offset.items()
            }
        except Exception: raise SchemaClassDumpError

        info("Success Dump %s Schemas Offset: Classes->%s, Fields->%s" % (
            module_name,
            len(classes),
            len([field for cls in classes.values() for field in cls])
        ))
        schema.update({module_name.replace(".", "_"): classes})
    return schema




def read_schema_system_address() -> Optional[int]:
    try:
        schemasystem_base = CS2.schemasystem.base
        schemasystem_buffer = CS2.memory.read_memory(CS2.schemasystem.base, CS2.schemasystem.size)

        schema_system_address = (
            Pattern(Offset.StructSchemaSystem.SCHEMA_SYSTEM_PATTERN)
            .search(schemasystem_base, schemasystem_buffer)
            .rip(
                Offset.StructSchemaSystem.SCHEMA_SYSTEM_PATTERN_RIP_OFFSET,
                Offset.StructSchemaSystem.SCHEMA_SYSTEM_PATTERN_RIP_LENGTH
            )
            .address
        )
    except Exception: return None

    return schema_system_address


def read_module(module_address: int) -> Dict[str, Union[List[int], StructModule]]:
    module_struct = StructModule(module_address)

    class_bindings_address = module_struct.class_bindings_address
    allocated_classes_address = read_allocated_address_list(module_struct, class_bindings_address)
    unallocated_classes_address = read_unallocated_address_list(module_struct, class_bindings_address)

    current_classes_address = allocated_classes_address if len(allocated_classes_address) > len(unallocated_classes_address) else unallocated_classes_address
    return dict(module_struct=module_struct, classes_address=current_classes_address)


def read_allocated_address_list(module_struct: StructModule, binding_address: int) -> List[int]:
    allocated_address_list: List[int] = list()

    memory_pool_struct = StructMemoryPool(module_struct.memory_pool_address(binding_address))
    allocated_address = memory_pool_struct.free_list_head

    while allocated_address:
        alloc_address_struct = StructAllocatedClassBase(allocated_address)
        if alloc_address_struct.data:
            allocated_address_list.append(alloc_address_struct.data)

        allocated_address = alloc_address_struct.next
        if len(allocated_address_list) >= memory_pool_struct.peak_alloc: break

    return allocated_address_list


def read_unallocated_address_list(module_struct: StructModule, binding_address: int) -> List[int]:
    unallocated_address_list: List[int] = list()

    memory_pool_struct = StructMemoryPool(module_struct.memory_pool_address(binding_address))
    hash_bucket_structs: Generator[StructHashBucket, None, None] = (
        StructHashBucket(module_struct.hash_bucket_address(binding_address, index))
        for index in range(Offset.StructTSHash.HASH_BUCKET_SIZE)
    )

    for hash_bucket_struct in hash_bucket_structs:
        try: unallocated_address = hash_bucket_struct.first_uncomm
        except Exception: continue

        while unallocated_address:
            unallocated_address_struct = StructUnAllocatedClassBase(unallocated_address)
            if unallocated_address_struct.data:
                unallocated_address_list.append(unallocated_address_struct.data)

            unallocated_address = unallocated_address_struct.next
            if len(unallocated_address_list) >= memory_pool_struct.blocks_alloc: break
        if len(unallocated_address_list) >= memory_pool_struct.blocks_alloc: break

    return unallocated_address_list


def read_class(class_address: int) -> Dict[str, Dict[str, int]]:
    class_struct = StructClass(class_address)
    class_name = class_struct.name

    fields = read_field(class_struct.fields, class_struct.fields_count)
    return {class_name: fields}


def read_field(fields_base_address: int, fields_count: int) -> Dict[str, int]:
    fields = dict()

    for index in range(fields_count):
        field_address = fields_base_address + index * Offset.StructClass.FIELDS_INDEX
        field_struct = StructField(field_address)

        if field_struct.name is None: break
        fields.update({field_struct.name: field_struct.value})
    return fields