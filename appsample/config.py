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


class DevelopmentConfig(BaseConfig):
    DEBUG = False
    WTF_CSRF_CHECK_DEFAULT = True
    WTF_CSRF_SSL_STRICT = True
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/manga"
    #SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/manga"
    SQLALCHEMY_DATABASE_URI = "postgresql://hbnrxfyyharifc:40933115b93bc2ead4895c81c421c87033bb95175ae68bcce1f36ea568a167e8@ec2-34-194-158-176.compute-1.amazonaws.com:5432/d609ltha03al1l"
    # if use docker compose use this
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@mysql:3306/manga"


class TestingConfig(BaseConfig):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/mangatest"
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/mangatest"
    WTF_CSRF_ENABLED = False
    TESTING = True


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
}
