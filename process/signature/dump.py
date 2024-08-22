from logging import info
from typing import Dict

from memprocfs import FLAG_NOCACHE

from error import SignatureDumpingError
from process.address import Address
from process.cs2 import CS2
from process.signature.client import *
from process.signature.engine2 import *


client_signatures_function = (
        dwEntityList,
        dwGameEntitySystem,
        dwGameEntitySystem_getHighestEntityIndex,
        dwGameRules,
        dwGlobalVars,
        dwGlowManager,
        dwLocalPlayerController,
        dwLocalPlayerPawn,
        dwPlantedC4,
        dwViewAngles,
        dwViewMatrix,
        dwViewRender,
        dwWeaponC4,
    )
def get_client_signatures() -> Dict[str, Address]:
    client_base = CS2.client.base
    client_buffer = CS2.memory.read_memory(CS2.client.base, CS2.client.size)

    client_signatures = {
        client_signature_function.__name__: client_signature_function(client_base, client_buffer).to_Address()
        for client_signature_function in client_signatures_function
    }

    return client_signatures


engine2_signatures_function = (
        dwBuildNumber,
        dwNetworkGameClient,
        dwNetworkGameClient_maxClients,
        dwNetworkGameClient_serverTickCount,
    )
def get_engine2_signatures() -> Dict[str, Address]:
    engine2_base = CS2.engine2.base
    engine2_buffer = CS2.memory.read_memory(CS2.engine2.base, CS2.engine2.size)

    engine2_signatures = {
        engine2_signature_function.__name__: engine2_signature_function(engine2_base, engine2_buffer).to_Address()
        for engine2_signature_function in engine2_signatures_function
    }

    return engine2_signatures


def dump_signatures() -> Dict[str, Dict[str, Address]]:
    try: client_signatures = get_client_signatures()
    except Exception: raise SignatureDumpingError
    else: info("Success Dump client.dll Signatures Offset (%02i/%02i)." % (len(client_signatures), len(client_signatures_function)))

    try: engine2_signatures = get_engine2_signatures()
    except Exception: raise SignatureDumpingError
    else: info("Success Dump engine2.dll Signatures Offset (%02i/%02i)." % (len(engine2_signatures), len(engine2_signatures_function)))

    return dict(
        client=client_signatures,
        engine2=engine2_signatures
    )