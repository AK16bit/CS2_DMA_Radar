from gc import collect
from logging import info
from sys import getsizeof
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
    module_base = CS2.client.base
    module_buffer = CS2.memory.read_memory(module_base, CS2.client.size)

    client_signatures = {
        signature_function.__name__: signature_function(module_base, module_buffer).to_Address()
        for signature_function in client_signatures_function
    }

    del module_buffer
    return client_signatures


engine2_signatures_function = (
        dwBuildNumber,
        dwNetworkGameClient,
        dwNetworkGameClient_maxClients,
        dwNetworkGameClient_serverTickCount,
    )
def get_engine2_signatures() -> Dict[str, Address]:
    module_base = CS2.engine2.base
    module_buffer = CS2.memory.read_memory(module_base, CS2.engine2.size)

    engine2_signatures = {
        signature_function.__name__: signature_function(module_base, module_buffer).to_Address()
        for signature_function in engine2_signatures_function
    }

    del module_buffer
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
        engine2=engine2_signatures,
    )