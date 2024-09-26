from logging import info, debug
from threading import Thread
from time import sleep

from error import ProcessSetupError
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

    # sleep(114514)


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

    run_loop_thread = RepeatThread(1 / 60, run_loop)
    run_loop_thread.start()

    map_update_thread = RepeatThread(30, map_update_loop)
    map_update_thread.start()

    clear_cache_thread = RepeatThread(5, clear_cache)
    clear_cache_thread.start()

    run_web_server(1090)


if __name__ == '__main__':
    main()