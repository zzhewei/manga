from datetime import timedelta
import os


class BaseConfig:  # 基本配置
    SECRET_KEY = os.urandom(24)
    # 不設定的話Flask會使用緩存的js跟css不會更新
    SEND_FILE_MAX_AGE_DEFAULT = timedelta(seconds=1)
    # 中文設置
    JSON_AS_ASCII = False
    # SWAGGER設置  /apidocs
    SWAGGER = {
        "title": "Manga API",
        "description": "",
        "version": "1.0.0",
        "termsOfService": "",
        "hide_top_bar": True
    }
    LANGUAGES = ['zh', 'en', 'ja']
    BABEL_TRANSLATION_DIRECTORIES = '../translations'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = 'xxxx@gmail.com'
    MAIL_PASSWORD = 'test'
    MAIL_SENDER = 'Heaven Admin <xxxx@gmail.com>'
    MAIL_SUBJECT_PREFIX = '[Heaven]'
    FLASK_ANALYZE = False


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = True
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:cvbn78910@localhost:3306/manga"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@192.168.0.202:5432/manga"
    # heroku
    # SQLALCHEMY_DATABASE_URI = "postgresql://pugtefbvkqitvd:a978115eeffa95dd5b5c1d3ffad548c8ce44b0043ca573400c254fffe34cfa39@ec2-52-20-166-21.compute-1.amazonaws.com:5432/d4395tdnru2bdm"
    # render
    SQLALCHEMY_DATABASE_URI = "postgresql://manga_1h1z_user:6xR37NTVTVsXQ9nJrB551sEVhtpKKZ0c@dpg-ch5lg0orddl7albugqeg-a.singapore-postgres.render.com/manga"


class DockerDevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql:3306/manga"


class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/mangatest"
    # SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/mangatest"
    WTF_CSRF_ENABLED = False
    TESTING = True


class GitlabCIConfig(TestingConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql:3306/mangatest"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'gitlab_testing': GitlabCIConfig,
    'docker': DockerDevelopmentConfig,
}
