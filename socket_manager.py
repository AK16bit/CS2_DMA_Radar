from flask_socketio import SocketIO
from typing import TypedDict, Any, Optional, List


class SocketManager:
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

    class SocketPlayersDot(TypedDict):
        class PlayerDot(TypedDict):
            x: float
            y: float
            r: float
            id: int
        time: float
        t: List[PlayerDot]
        ct: List[PlayerDot]
    @classmethod
    def send_players_dot(cls, players_dot: SocketPlayersDot) -> None:
        cls.send_socket("players_dot", players_dot)

    class SocketBombStatus(TypedDict):
        time: float
        planted: bool
        site: str
        pos: dict
        time_left: float
        time_max: float
        defusing: bool
        defuse_time_left: float
    class SocketBombBeep(TypedDict):
        beep_span: float
    @classmethod
    def send_bomb_status(cls, bomb_status: SocketBombStatus) -> None:
        cls.send_socket("bomb_status", bomb_status)
    @classmethod
    def send_bomb_beep(cls, bomb_beep: SocketBombBeep) -> None:
        cls.send_socket("bomb_beep", bomb_beep)


