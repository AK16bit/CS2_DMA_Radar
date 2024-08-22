from error import ProcessSetupError
from game.entity_list import EntityList
from game.player_entity import PlayerEntity
from process.address import Address
from process.cs2 import CS2

from logging import info

from process.memory import MemoryReadCounter
from utils import logger_setup



def runtime() -> None: ...
    # print(MemoryReadCounter.get_memory_read_count())
    # MemoryReadCounter.reset_memory_read_count()
    # Address.clear_address_cache()
    #
    # while True:
    #     local_player_entity = PlayerEntity(
    #         CS2.offset.signatures.client.dwLocalPlayerController.pointer(),
    #         CS2.offset.signatures.client.dwLocalPlayerPawn.pointer()
    #     )
    #     if local_player_entity.controller.address is None or local_player_entity.pawn.address is None: continue
    #
    #     for player_entity in EntityList.update().player_entities:
    #         if player_entity == local_player_entity: continue
    #
    #     # player_entity.health
    #
    #     Address.clear_address_cache()
    #     print(MemoryReadCounter.get_memory_read_count())
    #     MemoryReadCounter.reset_memory_read_count()
    #
    #     # break


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

    try: CS2.setup_pymeow().update_offsets()
    except Exception: raise ProcessSetupError

    runtime()


if __name__ == '__main__':
    main()