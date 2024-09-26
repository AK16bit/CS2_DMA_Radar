from flask_socketio import SocketIO
from typing import TypedDict, Any, Optional, List


class SocketData:
    _socket_io: Optional[SocketIO] = None

    @classmethod
    def set_socket_io(cls, socket_io: SocketIO) -> None:
        cls._socket_io = socket_io

    @classmethod
    def send_socket(cls, event: str, data: Any) -> bool:
        if cls._socket_io is None: return False

        try: cls._socket_io.emit(event, data)
        except Exception: return False
        return True

    @classmethod
    def send_map_sync(cls, map_name: str) -> None:
        cls.send_socket("map_sync", "static/no_map.png" if map_name is None or map_name == "<empty>" else "static/maps/%s.png" % map_name)

    class SocketPlayersPos(TypedDict):
        time: float
        t: List[dict]
        ct: List[dict]

    @classmethod
    def send_players_pos(cls, players_pos: SocketPlayersPos) -> None:
        cls.send_socket("players_pos", players_pos)