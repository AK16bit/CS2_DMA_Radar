from logging import debug
from typing import Optional, Generator, Dict

from process.convar.offset import Offset
from process.convar.struct import StructConvarSystem, StructConvar
from process.cs2 import CS2
from process.pattern import PatternVerA2X


def dump_convar() -> Dict[str, StructConvar]:
    convar_system_address = read_convar_system_address()
    convar_system_struct = StructConvarSystem(convar_system_address)

    convars_count = convar_system_struct.convar_count()
    convars_address: Generator[int, None, None] = (convar_system_struct.convar_address(index) for index in range(convars_count))

    convars = dict()
    for convar_index, convar_address in enumerate(convars_address):
        convar_struct = StructConvar(convar_address)

        try:
            convar_name = convar_struct.name()
            convars.update({convar_name: convar_struct})
        except Exception: continue

    return convars



def read_convar_system_address():
    tier0_buffer = CS2.memory.read_memory(CS2.tier0.base, CS2.tier0.size)

    convar_system = PatternVerA2X(
        Offset.StructConvarSystem.CONVAR_SYSTEM_PATTERN, CS2.tier0.base, tier0_buffer
    ).aob_scan().rip(
        Offset.StructConvarSystem.CONVAR_SYSTEM_PATTERN_RIP_OFFSET,
        Offset.StructConvarSystem.CONVAR_SYSTEM_PATTERN_RIP_LENGTH
    ).address

    return convar_system
