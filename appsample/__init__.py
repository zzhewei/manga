#################################
# __init__ 把當前目錄當作package 在其中做初始化動作
#################################
from flask import Flask, jsonify
from flasgger import Swagger
from .config import config
from flask_cors import CORS
from werkzeug.utils import import_string
from .model import db, migrate, Role
import logging
from logging.handlers import TimedRotatingFileHandler
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager


csrf = CSRFProtect()
login_manager = LoginManager()


##########
# 工廠模式
# 初始化 Flask對象可以是package或檔案 __name__是系統變數，該變數指的是該py檔的名稱
##########
def create_app(config_name, blueprints):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    Swagger(app)
    for i in blueprints:
        import_name = import_string(i)
        app.register_blueprint(import_name)
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)

    formatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
    handler = TimedRotatingFileHandler("./log/event.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=True, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    @app.route("/init")
    def init():
        Role.insert_roles()
        return jsonify({"Success": True})

    '''
    @app.after_request
    def inject_csrf_token(response):
        response.set_cookie("csrf_token", generate_csrf())
        return response


    @app.before_request
    def check_csrf():
        # BEGIN workaround until https://github.com/lepture/flask-wtf/pull/419 is merged
        if request.blueprint in csrf._exempt_blueprints:
            return

        view = app.view_functions.get(request.endpoint)
        dest = f'{view.__module__}.{view.__name__}'

        if dest in csrf._exempt_views:
            return
        # END workaround
    '''
    # with app.app_context():
    #    db.create_all()
    return app


'''
flask app.route how to run
refer:https://www.cnblogs.com/sddai/p/13426277.html

class FlaskBother:
    def __init__(self):
        self.routes = {}

    def route(self, route_str):
        def decorator(f):
            self.routes[route_str] = f
            return f

        return decorator

    def server(self, path):
        view_function = self.routes.get(path)
        if view_function:
            return view_function()
        else:
            raise ValueError('Route "{}" has not been registered'.format(path))

app = FlaskBother()

@app.route("/")
def hello():
    return "Hello World"

print(app.server("/"))
'''