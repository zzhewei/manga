#################################
# reference:https://stackoverflow.com/questions/68288207/db-create-all-not-creating-tables-in-pytest-flask
#           https://dormousehole.readthedocs.io/en/latest/testing.html
#           https://iter01.com/578851.html
#           https://testdriven.io/blog/flask-pytest/
#################################
import pytest
from appsample import create_app
from appsample.model import User, db, Role


# function：每一個函式或方法都會呼叫
# class：每一個類呼叫一次
# module：每一個.py檔案呼叫一次
# session：是多個檔案呼叫一次

# autouse設定為True時，自動呼叫fixture功能。
@pytest.fixture(scope='session', autouse=True)
def test_client():
    blueprints = ['appsample.controller.main:main',
                  'appsample.controller.auth:auth',
                  'appsample.controller.role:role',
                  'appsample.controller.user:user']
    flask_app = create_app('testing', blueprints)

    with flask_app.test_client(use_cookies=True) as client:
        with flask_app.app_context():
            db.create_all()
            Role.insert_roles()
            user = User(role_id=1, email='test1234@gmail.com', username='test1', account='test1', password='test1', confirmed=False)
            db.session.add(user)
            db.session.commit()
            # 使用yield關鍵字可以實現setup/teardown的功能，在yield關鍵字之前的程式碼在case之前執行，yield之後的程式碼在case執行結束後執行
            yield client
            db.session.remove()
            db.drop_all()
