from process.pattern import Pattern


def dwCSGOInput(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? 48 8D 05")
        .search(module_base, module_buffer)
        .rip()
    )

def dwEntityList(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 35 ?? ?? ?? ?? 48 85 F6")
        .search(module_base, module_buffer)
        .rip()
    )

def dwGameEntitySystem(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8B 1D ?? ?? ?? ?? 48 89 1D")
        .search(module_base, module_buffer)
        .rip()
    )

def dwGameEntitySystem_getHighestEntityIndex(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("8B 81 ?? ?? ?? ?? 89 02 48 8B C2 C3 CC CC CC CC 48 89 5C 24 ?? 48 89 6C 24")
        .search(module_base, module_buffer)
        .slice(2, 4)
    )

def dwGameRules(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 1D ?? ?? ?? ?? FF 15 ?? ?? ?? ?? 84 C0")
        .search(module_base, module_buffer)
        .rip()
    )

def dwGlobalVars(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 0D ?? ?? ?? ?? 48 89 41")
        .search(module_base, module_buffer)
        .rip()
    )

def dwGlowManager(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8B 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 8B 41")
        .search(module_base, module_buffer)
        .rip()
    )

def dwLocalPlayerController(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 05 ?? ?? ?? ?? 8B 9E")
        .search(module_base, module_buffer)
        .rip()
    )

def dwLocalPlayerPawn(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D")
        .search(module_base, module_buffer)
        .rip()
        .add(328)
    )

def dwPlantedC4(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8B 15 ?? ?? ?? ?? 41 FF C0")
        .search(module_base, module_buffer)
        .rip()
    )

def dwPrediction(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8D 05 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC 48 83 EC ?? 8B 0D")
        .search(module_base, module_buffer)
        .rip()
    )

def dwSensitivity(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8B 05 ?? ?? ?? ?? 48 8B 40 ?? F3 41 0F 59 F4")
        .search(module_base, module_buffer)
        .rip()
    )

def dwSensitivity_sensitivity(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("FF 50 ?? 4C 8B C6 48 8D 55 ?? 48 8B CF E8 ?? ?? ?? ?? 84 C0 0F 85 ?? ?? ?? ?? 4C 8D 45 ?? 8B D3 48 8B CF E8 ?? ?? ?? ?? E9 ?? ?? ?? ?? F3 0F 10 06")
        .search(module_base, module_buffer)
        .slice(2, 3)
    )

def dwViewAngles(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8D 0D ?? ?? ?? ?? E8 ?? ?? ?? ?? 48 8D 05 ?? ?? ?? ?? 48 C7 05 ?? ?? ?? ?? ?? ?? ?? ?? 48 89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? 48 8D 05")
        .search(module_base, module_buffer)
        .rip()
        .add(21528)
    )

def dwViewMatrix(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8D 0D ?? ?? ?? ?? 48 C1 E0 06")
        .search(module_base, module_buffer)
        .rip()
    )

def dwViewRender(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 05 ?? ?? ?? ?? 48 8B C8 48 85 C0")
        .search(module_base, module_buffer)
        .rip()
    )

def dwWeaponC4(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 8B 15 ?? ?? ?? ?? FF C0 89 05 ?? ?? ?? ?? 48 8B C6 48 89 34 EA 48 8B 6C 24 ?? C6 86 ?? ?? ?? ?? ?? 80 BE")
        .search(module_base, module_buffer)
        .rip()
    )