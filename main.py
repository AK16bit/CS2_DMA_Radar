from gc import collect
from logging import info, debug
from threading import Thread
from time import sleep, time

from error import ProcessSetupError
from game.entity_list import EntityList
from game.projectile_entity import ProjectileEntity
from process.address import Address
from process.cs2 import CS2
from process.memory import MemoryReadMonitor
from runtime.run_loop import run_loop, clear_cache, map_update_loop
from runtime.server import run_web_server
from utils import logger_setup, RepeatThread


def setup() -> None:
    try: CS2.setup_pymeow().update_offsets()
    except Exception: raise ProcessSetupError

    debug("Setup Memory Read: Count->%s, Byte->%s" % (MemoryReadMonitor.memory_read_count, MemoryReadMonitor.memory_read_bytes))
    MemoryReadMonitor.reset()
    Address.clear_address_cache()
    collect()

    # sleep(114514)


def test_projectile() -> None:
    # entity_list_address = CS2.offset.signatures.client.dwEntityList.pointer().offset(0x10).pointer()
    entity_list_address = CS2.offset.signatures.client.dwEntityList.pointer()

    while True:
        for entity_index in range(64, 1024):
            # entity_address = entity_list_address.address + 0x78 * (entity_index)
            entity_address = EntityList.get_entity_from_list_entry(entity_list_address, entity_index)
            if not entity_address.address: continue

            try:
                class_name = entity_address.copy().pointer_chain(0x10, 0x20).str(32)
                if "projectile" in class_name:
                    entity = ProjectileEntity(entity_address)

                    print(
                        time(), entity_index, class_name, entity.detonate_time
                        # entity_base.offset(0x1120).float() - CS2.offset.signatures.client.dwGlobalVars.pointer().offset(0x34).float(),
                        # entity_base.offset(0x111A).bool()
                    )
            except Exception: ...

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

    # test_projectile()
    run_loop_thread = RepeatThread(1 / 128, run_loop)
    run_loop_thread.start()

    map_update_thread = RepeatThread(30, map_update_loop)
    map_update_thread.start()

    clear_cache_thread = RepeatThread(5, clear_cache)
    clear_cache_thread.start()

    run_web_server(1090)


if __name__ == '__main__':
    main()