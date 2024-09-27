from logging import debug, error, info
from time import time

from game.entity_list import EntityList
from game.map import Map
from game.planted_c4 import PlantedC4
from game.player_entity import PlayerEntity
from process.address import Address
from process.cs2 import CS2
from process.memory import MemoryReadMonitor
from runtime.cache import RuntimeCache
from socket_manager import SocketManager


def run_loop() -> None:
    time_now = time()

    # players_pos
    players_pos_socket: SocketManager.SocketPlayersPos = dict(
        time=time_now,
        t=list(),
        ct=list()
    )
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
        SocketManager.send_players_pos(players_pos_socket)
    except Exception as error_reason: error("Error at run_loop->players_pos: %s" % error_reason)

    # players_status
    try:
        for player_entity in EntityList.update().player_entities:
            if not player_entity.health: continue

            ...
    except Exception as error_reason: error("Error at run_loop->players_status: %s" % error_reason)

    # bomb
    bomb_socket: SocketManager.SocketBombStatus = dict(
        time=time_now,
        planted=False,
        site="None",
        pos=dict(),
        time_left=0, time_max=40,
        defusing=False, defuse_time_left=0
    )
    try:
        game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
        is_c4_planted = game_rule_address.copy().offset(CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()

        bomb_socket["planted"] = is_c4_planted
        if is_c4_planted:
            planted_c4 = PlantedC4(CS2.offset.signatures.client.dwPlantedC4.pointer().pointer())

            pos = planted_c4.pos
            if pos is None: ...
            map_pos = Map.world_2_map(pos)
            if map_pos is None: ...
            bomb_socket["pos"] = map_pos.to_dict()

            bomb_socket.update(dict(
                site=planted_c4.site,
                pos=planted_c4.pos,
                time_left=planted_c4.explode_time_left,
                time_max=40,
                defusing=planted_c4.is_defusing,
                defuse_time_left=planted_c4.defuse_time_left if planted_c4.is_defusing else 0,
            ))

            next_beep_game_time = planted_c4.next_beep_game_time
            if RuntimeCache.last_beep_game_time == -1 or RuntimeCache.last_beep_game_time != next_beep_game_time:
                RuntimeCache.last_beep_game_time, RuntimeCache.last_beep_time_length = next_beep_game_time, planted_c4.next_beep_time

                bomb_beep_socket: SocketManager.SocketBombBeep = dict(
                    beep_span=planted_c4.next_beep_time
                )
                SocketManager.send_bomb_beep(bomb_beep_socket)


        SocketManager.send_bomb_status(bomb_socket)
    except Exception as error_reason: error("Error at run_loop->bomb: %s" % error_reason)

    Address.clear_address_cache()


def map_update_loop() -> None:
    Map.update()
    SocketManager.send_map_sync(Map.map_name)
    debug("Updating Map: name->\"%s\"" % Map.map_name)

def clear_cache() -> None:
    debug("Clearing Cache: controller->%02i, pawn->%02i" % (len(EntityList._index_2_controller_cache), len(EntityList._controller_2_pawn_cache)))
    EntityList.clear_cache()