from process.pattern import Pattern


def dwBuildNumber(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? FF 15 ?? ?? ?? ??")
        .search(module_base, module_buffer)
        .rip(2, 6)
    )

def dwNetworkGameClient(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("48 89 3D ?? ?? ?? ?? 48 8D 15")
        .search(module_base, module_buffer)
        .rip()
    )

def dwNetworkGameClient_maxClients(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 8B 81 ?? ?? ?? ?? FF C0")
        .search(module_base, module_buffer)
        .slice(2, 4)
    )

def dwNetworkGameClient_serverTickCount(module_base: int, module_buffer: bytes) -> Pattern:
    return (
        Pattern("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 83 B9")
        .search(module_base, module_buffer)
        .slice(2, 4)
    )
