from process.cs2 import CS2
from process.schema.dump import dump_schemas
from process.signature.dump import dump_signatures

from logging import Logger, info

from utils import logger_setup


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


    CS2.setup_pymeow()
    dump_signatures()
    dump_schemas()


if __name__ == '__main__':
    main()