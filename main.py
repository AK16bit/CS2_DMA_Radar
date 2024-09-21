from logging import info, debug
from threading import Thread, Timer
from time import time
from typing import TypedDict

from error import ProcessSetupError
from game.entity_list import EntityList
from game.map import Map
from game.planted_c4 import PlantedC4
from game.player_entity import PlayerEntity
from process.address import Address
from process.cs2 import CS2
from process.memory import MemoryReadMonitor
from utils import logger_setup, RepeatThread

from flask import Flask, render_template, url_for, request
from flask_socketio import SocketIO


class SocketDataStruct(TypedDict):
    t: float
    local_player: dict
    teammate: list
    enemy: list

socket_data: SocketDataStruct = dict()

def run_loop() -> None:
    global socket_data
    Map.update()

    while True:
        socket_data_merging: SocketDataStruct = dict(
            t=time(),
            teammate=list(),
            enemy=list(),
        )

        local_player_entity = PlayerEntity(
            CS2.offset.signatures.client.dwLocalPlayerController.pointer(),
            CS2.offset.signatures.client.dwLocalPlayerPawn.pointer()
        )
        if local_player_entity.controller.address is None or local_player_entity.pawn.address is None: return

        # print(local_player_entity.pos, Map.world_2_map(local_player_entity.pos))
        Address.clear_address_cache()

        for player_entity in EntityList.update().player_entities:
            if not player_entity.health: continue

            pos = player_entity.pos
            map_pos = Map.world_2_map(pos)

            if player_entity == local_player_entity:
                socket_data_merging.update(dict(local_player=dict(
                    x=map_pos.x,
                    y=map_pos.y
                )))
                continue

            socket_data_merging.setdefault(
                ("teammate" if player_entity.team_num == local_player_entity.team_num else "enemy"), list()
            ).append(dict(
                x=map_pos.x,
                y=map_pos.y
            ))

            # print(pos, map_pos)

        debug("memory_read_run_once: %i" % MemoryReadMonitor.memory_read_count)

        # game_rule_address: Address = CS2.offset.signatures.client.dwGameRules.pointer()
        # is_c4_planted = game_rule_address.copy().offset(CS2.offset.schemas.client_dll.C_CSGameRules.m_bBombPlanted).bool()
        #
        # if is_c4_planted:
        #     game_time = CS2.offset.signatures.client.dwGlobalVars.pointer().offset(0x34).float()
        #
        #     planted_c4 = PlantedC4(CS2.offset.signatures.client.dwPlantedC4.pointer().pointer())



        Address.clear_address_cache()
        MemoryReadMonitor.reset()

        socket_data = socket_data_merging


def clear_cache() -> None:
    debug("Clearing Cache: controller->%02i, pawn->%02i" % (len(EntityList._controller_cache_map), len(EntityList._pawn_cache_map)))
    EntityList.clear_cache()


def run_web_server() -> None:
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    @app.route('/')
    def index():
        return render_template('main.html')

# if 'Mobile' in request.headers.get('User-Agent'):
#     return render_template('mobile.html')
# else: return render_template('desktop.html')

    def send_message():
        socketio.emit('message', socket_data)
        Timer(1 / 30, send_message).start()

    send_message()
    socketio.run(app, host='0.0.0.0', port=1090, allow_unsafe_werkzeug=True, debug=True)


def dev() -> None:
    ...


def setup() -> None:
    try: CS2.setup_pymeow().update_offsets()
    except Exception: raise ProcessSetupError

    debug("Memory Read: Count->%s, Byte->%s" % (MemoryReadMonitor.memory_read_count, MemoryReadMonitor.memory_read_bytes))
    MemoryReadMonitor.reset()
    Address.clear_address_cache()


def main() -> None:
    logger_setup()
    [info(line) for line in r"""  /$$$$$$  /$$   /$$  /$$$$$$   /$$$$$$  /$$$$$$$$ /$$$$$$  /$$$$$$$$
 /$$__  $$| $$  /$$/ /$$__  $$ /$$__  $$|_____ $$//$$__  $$|_____ $$/
| $$  \ $$| $$ /$$/ |__/  \ $$|__/  \ $$     /$$/| $$  \__/     /$$/ 
| $$$$$$$$| $$$$$/     /$$$$$/  /$$$$$$/    /$$/ | $$$$$$$     /$$/  
| $$__  $$| $$  $$    |___  $$ /$$____/    /$$/  | $$__  $$   /$$/   
| $$  | $$| $$\  $$  /$$  \ $$| $$        /$$/   | $$  \ $$  /$$/    
| $$  | $$| $$ \  $$|  $$$$$$/| $$$$$$$$ /$$/    |  $$$$$$/ /$$/     
|__/  |__/|__/  \__/ \______/ |________/|__/      \______/ |__/""".split("\n")]

    setup()

    run_loop_thread = Thread(target=run_loop)
    run_loop_thread.start()

    clear_cache_thread = RepeatThread(5, clear_cache)
    clear_cache_thread.start()

    # run_web_server()
    # dev()


if __name__ == '__main__':
    main()