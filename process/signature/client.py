from process.pattern import PatternVerA2X




def dwEntityList(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 35 ?? ?? ?? ?? 48 85 F6", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwGameEntitySystem(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8B 1D ?? ?? ?? ?? 48 89 1D", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwGameEntitySystem_getHighestEntityIndex(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("8B 81 ?? ?? ?? ?? 89 02 48 8B C2 C3 CC CC CC CC 48 89 5C 24 ?? 48 89 6C 24", module_base, module_buffer)
        .aob_scan()
        .slice(2, 4)
    )

def dwGameRules(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 1D ?? ?? ?? ?? FF 15 ?? ?? ?? ?? 84 C0", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwGlobalVars(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 15 ?? ?? ?? ?? 48 89 42", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwGlowManager(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8B 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 8B 41", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwLocalPlayerController(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 05 ?? ?? ?? ?? 8B 9E", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwLocalPlayerPawn(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D", module_base, module_buffer)
        .aob_scan()
        .rip()
        .add(352)
    )

def dwPlantedC4(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8B 15 ?? ?? ?? ?? 41 FF C0", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwViewAngles(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? 48 8D 05", module_base, module_buffer)
        .aob_scan()
        .rip()
        .add(23936)
    )

def dwViewMatrix(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8D 0D ?? ?? ?? ?? 48 C1 E0 06", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwViewRender(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 05 ?? ?? ?? ?? 48 8B C8 48 85 C0", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwWeaponC4(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 8B 15 ?? ?? ?? ?? 48 8B 5C 24 ?? FF C0 89 05 ?? ?? ?? ?? 48 8B C6 48 89 34 EA 48 8B 6C 24 ?? C6 86 ?? ?? ?? ?? ?? 80 BE", module_base, module_buffer)
        .aob_scan()
        .rip()
    )