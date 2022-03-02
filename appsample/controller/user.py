import json
from flask_login import login_required
from ..model import select, sqlOP, Permission
from flask import Blueprint, jsonify, current_app
from ..decorators import admin_required, permission_required
test = Blueprint('test', __name__)


# query user information contact
@test.route("/test1", methods=['GET', 'POST'])
@login_required
@admin_required
def test1():
    """
    測試用
    ---
    tags:
      - test
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    try:
        #p1 = Product('Isacc', 8888, 'https://picsum.photos/id/1047/1200/600', '', '', '')
        #p2 = Product('Dennis', 9999,'https://picsum.photos/id/1049/1200/600', '', '', '')
        #p3 = Product('Joey', 7777, 'https://picsum.photos/id/1033/1200/600', '', '', '')
        #p4 = Product('Fergus', 6666,'https://picsum.photos/id/1041/1200/600', '', '', '')
        #p5 = Product('Max', 5555, 'https://picsum.photos/id/1070/1200/600', '', '', '')
        #p6 = Product('Jerry', 4444, 'https://picsum.photos/id/1044/1200/600', '', '', '')
        #p = [p1, p2, p3, p4, p5, p6]

        #db.session.add_all(p)
        #db.session.commit()
        current_app.logger.warning("simple page info...")

        sqlOP("insert into  tttest.product values(8,'Jeadrry', 4444, 'https://picsum.photos/id/1048a/1200/600', '', '', '2021-12-03 15:16:07' ,'2021-12-03 15:16:07' ,'')")
        rows = select("select * from tttest.product where name like concat('%', :val, '%')", **{'val': 'J'})
        print(rows)

        data = {"code": 200, "success": "true", "data": "success"}
    except Exception as e:
        result = [{"errorResult": str(e)}]
        data = {"code": 400, "success": "false", "data": result}
    return jsonify(data)


# update data
@test.route("/test2", methods=['GET', 'POST'])
@login_required
@permission_required(Permission.MODIFY)
def test2():
    """
    測試用
    ---
    tags:
      - test
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    try:
        current_app.logger.warning("simple page info...")

        sqlOP("update tttest.product set description = 'modify success' where name = 'Jeadrry'")
        rows = select("select * from tttest.product where name like concat('%', :val, '%')", **{'val': 'J'})
        print(rows)

        data = {"code": 200, "success": "true", "data": "success"}
    except Exception as e:
        result = [{"errorResult": str(e)}]
        data = {"code": 400, "success": "false", "data": result}
    return jsonify(data)
