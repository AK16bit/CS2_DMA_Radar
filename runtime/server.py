from logging import info

from flask import Flask, render_template
from flask_socketio import SocketIO
from psutil import net_connections

from error import PortOccupancyError
from runtime.run_loop import map_update_loop
from socket_manager import SocketManager


def run_web_server(port: int) -> None:
    if port <= 1024:
        raise ValueError
    if any((connection.status == "LISTEN" and connection.laddr.port == port) for connection in net_connections()):
        raise PortOccupancyError

    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config['SECRET_KEY'] = 'secret!'

    socketio = SocketIO(app)
    SocketManager.set_socket_io(socketio)

    @app.route('/')
    def index():
        return render_template('main.html')

    @socketio.on("connect")
    def connect():
        connected_client = [client for client in socketio.server.manager.rooms['/'].keys() if client is not None]
        info("Connected Clients (%i): %s" % (len(connected_client), ", ".join(connected_client)))

        map_update_loop()

# if 'Mobile' in request.headers.get('User-Agent'):
#     return render_template('mobile.html')
# else: return render_template('desktop.html')

    socketio.run(app, host='0.0.0.0', port=port, allow_unsafe_werkzeug=True, debug=True, use_reloader=False)



if __name__ == '__main__':
    run_web_server(1090)