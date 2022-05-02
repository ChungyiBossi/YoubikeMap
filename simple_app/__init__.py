
# from simple_app.app import create_flask_app
# from simple_app.route import create_route

# https://kknews.cc/zh-tw/code/bjx6qeo.html   import turtorial
from simple_app.app import create_flask_app

def create_app():
    app = create_flask_app()
    print("Start!!!")
    return app
