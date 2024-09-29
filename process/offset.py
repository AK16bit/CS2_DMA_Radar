from typing import Any
import process


# It juz 4 type tint, ez 2 coding :P


class Offset:
    class _Signatures:
        class _SignaturesClient:
            dwEntityList: "process.address.Address"
            dwGameEntitySystem: "process.address.Address"
            dwGameEntitySystem_getHighestEntityIndex: "process.address.Address"
            dwGameRules: "process.address.Address"
            dwGlobalVars: "process.address.Address"
            dwGlowManager: "process.address.Address"
            dwLocalPlayerController: "process.address.Address"
            dwLocalPlayerPawn: "process.address.Address"
            dwPlantedC4: "process.address.Address"
            dwViewAngles: "process.address.Address"
            dwViewMatrix: "process.address.Address"
            dwViewRender: "process.address.Address"
            dwWeaponC4: "process.address.Address"

        class _SignaturesEngine2:
            dwBuildNumber: "process.address.Address"
            dwNetworkGameClient: "process.address.Address"
            dwNetworkGameClient_maxClients: "process.address.Address"
            dwNetworkGameClient_serverTickCount: "process.address.Address"

        client: _SignaturesClient
        engine2: _SignaturesEngine2

    class _Schemas:
        client_dll: Any

    class _Convars:
        mp_c4timer: "process.convar.struct.StructConvar"


    signatures: _Signatures
    schemas: _Schemas
    convars: _Convars

