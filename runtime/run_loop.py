from logging import debug, error, info
from threading import Thread
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
from utils import TimeUsedCounter, RunningDebugger


def players_dot() -> None:
    players_dot_socket = SocketManager.SocketPlayersDot(
        time=time(),
        players=list(),
    )
    try:
        for player_entity in EntityList.player_entities:
            if not player_entity.health: continue

            pos = player_entity.pos
            if pos is None: continue

            map_pos = Map.world_2_map(pos)
            if map_pos is None: continue

            direction = player_entity.angle
            if direction is None: continue

            players_dot_socket.get("players").append(dict(
                x=map_pos.x,
                y=map_pos.y,
                d=direction.y,
                # team={2: "t", 3: "ct"}.get(player_entity.team_num),
                team="t" if player_entity.team_num == 2 else "ct" if player_entity.team_num == 3 else None,
                id=str(player_entity.steam_id)
            ))

        SocketManager.send_players_dot(players_dot_socket)
    except Exception as error_reason:
        error("Error at run_loop->players_dot: %s->%s" % (error_reason.__traceback__.tb_lineno, error_reason))


def players_status() -> None:
    try:
        for player_entity in EntityList.player_entities:
            if not player_entity.health: continue

            ...
    except Exception as error_reason: error("Error at run_loop->players_status: %s" % error_reason)


def bomb_status() -> None:
    bomb_socket: SocketManager.SocketBombStatus = dict(
        time=time(),
        planted=False,
        site="None",
        pos=dict(),
        time_left=0, time_max=40,
        defusing=False, defuse_time_left=0
    )
    try:
        game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
        is_c4_planted = game_rule_address.copy().offset(
            CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()

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
    except Exception as error_reason:
        error("Error at run_loop->bomb: %s" % error_reason)

def run_loop() -> None:
    # # players_pos
    # players_dot_socket: SocketManager.SocketPlayersDot = dict(
    #     time=time_now,
    #     t=list(),
    #     ct=list()
    # )
    # try:
    #     for player_entity in EntityList.update().player_entities:
    #         if not player_entity.health: continue
    #
    #         pos = player_entity.pos
    #         if pos is None: continue
    #
    #         map_pos = Map.world_2_map(pos)
    #         if map_pos is None: continue
    #
    #         direction = player_entity.angle
    #         if direction is None: continue
    #
    #         players_dot_socket.get({
    #             2: "t",
    #             3: "ct",
    #         }.get(player_entity.team_num), list()
    #         ).append(dict(
    #             x=map_pos.x,
    #             y=map_pos.y,
    #             d=direction.y,
    #             id=player_entity.steam_id
    #         ))
    #     SocketManager.send_players_dot(players_dot_socket)
    # except Exception as error_reason: error("Error at run_loop->players_pos: %s" % error_reason)

    # # players_status
    # try:
    #     for player_entity in EntityList.update().player_entities:
    #         if not player_entity.health: continue
    #
    #         ...
    # except Exception as error_reason: error("Error at run_loop->players_status: %s" % error_reason)

    # # bomb
    # bomb_socket: SocketManager.SocketBombStatus = dict(
    #     time=time_now,
    #     planted=False,
    #     site="None",
    #     pos=dict(),
    #     time_left=0, time_max=40,
    #     defusing=False, defuse_time_left=0
    # )
    # try:
    #     game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
    #     is_c4_planted = game_rule_address.copy().offset(CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()
    #
    #     bomb_socket["planted"] = is_c4_planted
    #     if is_c4_planted:
    #         planted_c4 = PlantedC4(CS2.offset.signatures.client.dwPlantedC4.pointer().pointer())
    #
    #         pos = planted_c4.pos
    #         if pos is None: ...
    #         map_pos = Map.world_2_map(pos)
    #         if map_pos is None: ...
    #         bomb_socket["pos"] = map_pos.to_dict()
    #
    #         bomb_socket.update(dict(
    #             site=planted_c4.site,
    #             pos=planted_c4.pos,
    #             time_left=planted_c4.explode_time_left,
    #             time_max=40,
    #             defusing=planted_c4.is_defusing,
    #             defuse_time_left=planted_c4.defuse_time_left if planted_c4.is_defusing else 0,
    #         ))
    #
    #         next_beep_game_time = planted_c4.next_beep_game_time
    #         if RuntimeCache.last_beep_game_time == -1 or RuntimeCache.last_beep_game_time != next_beep_game_time:
    #             RuntimeCache.last_beep_game_time, RuntimeCache.last_beep_time_length = next_beep_game_time, planted_c4.next_beep_time
    #
    #             bomb_beep_socket: SocketManager.SocketBombBeep = dict(
    #                 beep_span=planted_c4.next_beep_time
    #             )
    #             SocketManager.send_bomb_beep(bomb_beep_socket)
    #
    #
    #     SocketManager.send_bomb_status(bomb_socket)
    # except Exception as error_reason: error("Error at run_loop->bomb: %s" % error_reason)

    # (players_dot_thread := Thread(target=players_dot)).start()
    # (players_status_thread := Thread(target=players_status)).start()
    # (bomb_status_thread := Thread(target=bomb_status)).start()
    #
    # [thread.join() for thread in (
    #     players_dot_thread,
    #     players_status_thread,
    #     bomb_status_thread,
    # )]
    #
    # del players_dot_thread, players_status_thread, bomb_status_thread


    with TimeUsedCounter(time_list=RunningDebugger.time_used):
        (
            EntityList
            .update_entity_list_address()
            .update_player_entity()
            # .update_world_entity()
        )

        players_dot()
        players_status()
        bomb_status()

    RunningDebugger.update_time_used().update_memory_read()
    # print(RunningDebugger.time_used_mean, RunningDebugger.memory_read_count_mean, RunningDebugger.memory_read_bytes_mean)

    MemoryReadMonitor.reset()
    Address.clear_address_cache()


def map_update_loop() -> None:
    Map.update()
    SocketManager.send_map_sync(Map.map_name)
    debug("Updating Map: name->\"%s\"" % Map.map_name)

def clear_cache() -> None:
    debug("Clearing Cache: controller->%02i, pawn->%02i" % (len(EntityList._index_2_controller_cache), len(EntityList._controller_2_pawn_cache)))
    EntityList.clear_cache()