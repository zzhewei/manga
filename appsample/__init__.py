#################################
# __init__ 把當前目錄當作package 在其中做初始化動作
#################################
import logging
from logging.handlers import TimedRotatingFileHandler

from celery import Celery, Task
from flasgger import Swagger
from flask import Flask, g, jsonify, request
from flask_babel import Babel
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import upgrade
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import import_string

from .config import config
from .model import AnonymousUser, Role, User, db, migrate

csrf = CSRFProtect()
login_manager = LoginManager()
bootstrap = Bootstrap()
babel = Babel()
email = Mail()


##########
# 工廠模式
# 初始化 Flask對象可以是package或檔案 __name__是系統變數，該變數指的是該py檔的名稱
##########
def create_app(config_name, blueprints):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    celery_init_app(app, config_name)
    Swagger(app)
    for i in blueprints:
        import_name = import_string(i)
        app.register_blueprint(import_name, url_prefix='/<lan>')
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)
    login_manager.init_app(app)
    bootstrap.init_app(app)
    babel.init_app(app)
    email.init_app(app)
    login_manager.anonymous_user = AnonymousUser

    formatter = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)d][%(levelname)s] - %(message)s")
    handler = TimedRotatingFileHandler("./log/event.log", when="D", interval=1, backupCount=15, encoding="UTF-8", delay=True, utc=True)
    app.logger.addHandler(handler)
    handler.setFormatter(formatter)

    @app.cli.command('init')
    @app.route("/init")
    def init():
        # 直接更新最新版
        upgrade()
        Role.insert_roles()
        r = Role.query.filter_by(name='Administrator').first()
        u = User(email='admin@example.com', username='admin', account='admin', password='admin', role=r, confirmed=True)
        db.session.add(u)
        db.session.commit()
        return jsonify({"Success": True})

    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, post-check=0, pre-check=0"
        return response

    ##########
    # reference:https://hackmd.io/@shaoeChen/SyX5xZWz7
    #           https://www.maxlist.xyz/2020/10/24/flask-i18n/
    #           https://flask.palletsprojects.com/en/2.0.x/patterns/urlprocessors/
    #           https://www.cnblogs.com/iamluoli/p/11202234.html
    ##########
    # 1 set g lan value
    @app.url_value_preprocessor
    def get_lan(endpoint, values):
        # print(endpoint, values)
        if values is not None:
            g.lan = values.pop('lan', 'zh')

    # 2 Check lan is in config
    @app.before_request
    def check_lan():
        lan = g.get('lan', None)
        if lan and lan not in app.config['LANGUAGES']:
            g.lan = request.accept_languages.best_match(app.config['LANGUAGES'])

    # 3 set lan type
    @babel.localeselector
    def get_locale():
        return g.get('lan')

    # 4 checks if the lan is in the dictionary
    @app.url_defaults
    def set_lan(endpoint, values):
        if 'lan' in values or not g.lan:
            return
        # URL map can be used to figure out if it would make sense to provide a lan for the given endpoint.
        if app.url_map.is_endpoint_expecting(endpoint, 'lan'):
            values['lan'] = g.lan
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

    if app.config["FLASK_ANALYZE"]:
        from werkzeug.middleware.profiler import ProfilerMiddleware
        app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="pstat_files")
    return app

def celery_init_app(app: Flask, config_name) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(app.name, task_cls=FlaskTask)
    celery_app.config_from_object(config[config_name])
    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

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