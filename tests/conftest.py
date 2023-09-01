#################################
# reference:https://stackoverflow.com/questions/68288207/db-create-all-not-creating-tables-in-pytest-flask
#           https://dormousehole.readthedocs.io/en/latest/testing.html
#           https://iter01.com/578851.html
#           https://testdriven.io/blog/flask-pytest/
#################################
import os

import pytest
from appsample import create_app
from appsample.mail import send_email_celery
from appsample.model import Manga, Role, User, db
from pytest_mock import MockFixture

# function：每一個函式或方法都會呼叫
# class：每一個類呼叫一次
# module：每一個.py檔案呼叫一次
# session：是多個檔案呼叫一次


# autouse設定為True時，自動呼叫fixture功能。
@pytest.fixture(scope="session", autouse=True)
def test_client():
    blueprints = [
        "appsample.controller.main:main",
        "appsample.controller.auth:auth",
        "appsample.controller.role:role",
        "appsample.controller.user:user",
    ]
    flask_app = create_app(os.getenv("FLASK_CONFIG") or "testing", blueprints)

    with flask_app.test_client(use_cookies=True) as client:
        with flask_app.app_context():
            db.create_all()
            Role.insert_roles()
            r = Role.query.filter_by(name="Administrator").first()
            user = User(
                role_id=1,
                email="test1234@gmail.com",
                username="test1",
                account="test1",
                password="test1",
                confirmed=False,
                role=r,
            )
            manga = Manga(
                url="http://localhost:5000/openapi/swagger",
                name="x",
                page="1",
                author="test1",
                author_group="s",
                status=False,
                update_user=1,
                insert_user=1,
            )
            db.session.add(user)
            db.session.add(manga)
            db.session.commit()
            # 使用yield關鍵字可以實現setup/teardown的功能，在yield關鍵字之前的程式碼在case之前執行，yield之後的程式碼在case執行結束後執行
            yield client
            db.session.remove()
            db.drop_all()


@pytest.fixture()
def celery_mock(mocker: MockFixture):
    """
    定義celery.delay回傳的測試資料，以測試程式是否能註冊

    Args:
        mocker (pytest_mock.plugin.MockerFixture): 用來mock外部函式的物件。

    Returns:
        None

    Raises:
        None
    """
    mock_celery = mocker.patch.object(target=send_email_celery, attribute="delay")
    mock_celery.return_value = None
