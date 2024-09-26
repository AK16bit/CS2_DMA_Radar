from logging import debug, error
from time import time

from game.entity_list import EntityList
from game.map import Map
from game.planted_c4 import PlantedC4
from game.player_entity import PlayerEntity
from process.address import Address
from process.cs2 import CS2
from process.memory import MemoryReadMonitor
from socket_data import SocketData


def run_loop() -> None:
    players_pos_socket: SocketData.SocketPlayersPos = dict(
        time=time(),
        t=list(),
        ct=list()
    )

    # players_pos
    try:
        for player_entity in EntityList.update().player_entities:
            if not player_entity.health: continue

            pos = player_entity.pos
            if pos is None: continue

            map_pos = Map.world_2_map(pos)
            if map_pos is None: continue

            players_pos_socket.get({
                2: "t",
                3: "ct",
            }.get(player_entity.team_num), list()
            ).append(dict(
                x=map_pos.x,
                y=map_pos.y
            ))
        SocketData.send_players_pos(players_pos_socket)
    except Exception as error_reason: error("Error in run_loop->players_pos: %s" % error_reason)

    # players_status
    try:
        for player_entity in EntityList.update().player_entities:
            if not player_entity.health: continue

            ...
    except Exception as error_reason: error("Error at run_loop->players_status: %s" % error_reason)

    # bomb
    try:
        game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
        is_c4_planted = game_rule_address.copy().offset(CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()

        if is_c4_planted:
            planted_c4 = PlantedC4(CS2.offset.signatures.client.dwPlantedC4.pointer().pointer())
            # planted_c4.test()
    except Exception as error_reason: error("Error in run_loop->bomb: %s" % error_reason)

    Address.clear_address_cache()




def map_update_loop() -> None:
    Map.update()
    SocketData.send_map_sync(Map.map_name)
    debug("Updating Map: name->\"%s\"" % Map.map_name)

def clear_cache() -> None:
    debug("Clearing Cache: controller->%02i, pawn->%02i" % (len(EntityList._index_2_controller_cache), len(EntityList._controller_2_pawn_cache)))
    EntityList.clear_cache()