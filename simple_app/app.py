import os
from flask import Flask
from flask_socketio import SocketIO
from .blueprint import simple_route
from .postgreSQL.session import create_engine
from .postgreSQL.tables import LineUser
from .google_map_api import GooogleMapClient

def create_flask_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)  # load relative configure
    app.config.from_mapping(
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    app.config.from_pyfile('config.py', silent=True)
    # envirenment vars check
    if not (app.config.get('GOOGLE_API_KEY') and app.config.get('LINE_CHANNEL_ACCESS_TOKEN')):
        app.logger.warn("Setup Your GOOGLE API Key and Line Channel ACT as envirenment variable correctly")

    # register blueprint
    app.register_blueprint(simple_route)
    # create db
    app.db_engine = create_engine(url=app.config.get('POSTGRESQL_DB_URL'))
    app.google_client = GooogleMapClient(api_key=app.config.get('GOOGLE_API_KEY'))

    # socket io
    # (?) 是不是創建socketio instance的時候，偷做了什麼事，因為只要創建後，就能透過gunicorn開啟
    socketio = SocketIO(app, logger=True)
    @socketio.on('connect_event')
    def connected_msg(msg):
        print("Connected! ", msg)

    @socketio.on("ping_from_client")
    def ping_from_client():
        print("Ping from client")
    return app