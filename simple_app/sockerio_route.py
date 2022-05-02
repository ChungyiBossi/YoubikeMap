from flask_socketio import SocketIO

def create_sockio_client(app):
    socketio = SocketIO(app, logger=True, engineio_logger=True, cors_allowed_origins="*")
    socketio_route(socketio)
    return socketio


def socketio_route(sockioInstance):

    @sockioInstance.on('connect_event')
    def connected_msg(msg):
        print("Connected! ", msg)

    @sockioInstance.on("ping_from_client")
    def ping_from_client():
        print("Ping from client")