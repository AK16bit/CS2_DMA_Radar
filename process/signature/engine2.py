from process.pattern import PatternVerA2X


def dwBuildNumber(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("89 05 ?? ?? ?? ?? 48 8D 0D ?? ?? ?? ?? FF 15 ?? ?? ?? ?? 48 8B 0D", module_base, module_buffer)
        .aob_scan()
        .rip(2, 6)
    )

def dwNetworkGameClient(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("48 89 3D ?? ?? ?? ?? 48 8D 15", module_base, module_buffer)
        .aob_scan()
        .rip()
    )

def dwNetworkGameClient_maxClients(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 8B 81 ?? ?? ?? ?? FF C0", module_base, module_buffer)
        .aob_scan()
        .slice(2, 4)
    )

def dwNetworkGameClient_serverTickCount(module_base: int, module_buffer: bytes) -> PatternVerA2X:
    return (
        PatternVerA2X("8B 81 ?? ?? ?? ?? C3 CC CC CC CC CC CC CC CC CC 83 B9", module_base, module_buffer)
        .aob_scan()
        .slice(2, 4)
    )
