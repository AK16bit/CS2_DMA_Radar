from typing import Any

from process.address import Address


# It juz 4 type tint, ez 2 coding :P
class _SignaturesClient:
    dwEntityList: Address
    dwGameEntitySystem: Address
    dwGameEntitySystem_getHighestEntityIndex: Address
    dwGameRules: Address
    dwGlobalVars: Address
    dwGlowManager: Address
    dwLocalPlayerController: Address
    dwLocalPlayerPawn: Address
    dwPlantedC4: Address
    dwViewAngles: Address
    dwViewMatrix: Address
    dwViewRender: Address
    dwWeaponC4: Address

# It juz 4 type tint, ez 2 coding :P
class _SignaturesEngine2:
    dwBuildNumber: Address
    dwNetworkGameClient: Address
    dwNetworkGameClient_maxClients: Address
    dwNetworkGameClient_serverTickCount: Address

# It juz 4 type tint, ez 2 coding :P
class _Signatures:
    client: _SignaturesClient
    engine2: _SignaturesEngine2


class Offset:
    signatures: _Signatures
    schemas: Any

