import os
from flask import Flask
from .blueprint import simple_route

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

    return app