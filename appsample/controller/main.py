from flask_login import login_required
from ..model import select, sqlOP, Permission, db
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session, request
from ..decorators import admin_required, permission_required
from .form import ModifyForm
import json
import datetime

main = Blueprint('main', __name__)
SortType = "asc"


# main page
@main.route("/", methods=['GET', 'POST'])
def MainPage():
    form = ModifyForm()
    if form.validate_on_submit() and form.submit.data:
        if form.mid.data:
            UpdateData = {"mid": form.mid.data, "url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data, "update_time": datetime.datetime.now()}
            sqlOP("update manga set url = :url, name= :name, page= :page, author= :author, author_group= :author_group, update_time= :update_time where mid = :mid", UpdateData)
            print("Success")
        else:
            print("insert")
            InsertData = {"url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data,
                          "status": 0, "insert_time": datetime.datetime.now(), "update_time": datetime.datetime.now(), "update_user": "Jason"}
            sqlOP("insert into manga(url, name, page, author, author_group, status, insert_time, update_time, update_user) \
                values(:url, :name, :page, :author, :author_group, :status, :insert_time, :update_time, :update_user)", InsertData)
    rows = select("select * from manga order by mid "+SortType+";")
    rand = select("select * from manga order by rand() limit 5")
    return render_template('main.html', rows=rows, rand=rand, form=form)


# fuzzy search
@main.route("/fuzzy", methods=['GET', 'POST'])
def FuzzySearch():
    PostDict = request.get_json()
    return_data = ""
    if PostDict['input']:
        return_data = select("select * from manga where url like concat('%', :val, '%') or name like concat('%', :val, '%') or author like concat('%', :val, '%')\
                            or author_group like concat('%', :val, '%')", {'val': PostDict['input']})
    else:
        return_data = select("select * from manga order by mid " + SortType + ";")

    for i, item in enumerate(return_data):
        return_data[i] = dict(item)
        return_data[i]['insert_time'] = return_data[i]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        return_data[i]['update_time'] = return_data[i]['update_time'].strftime('%Y-%m-%d %H:%M:%S')

    data = {"code": 200, "success": True, "data": return_data}
    return jsonify(data)


# query sort by button
@main.route("/sort")
def MainPageSort():
    global SortType
    if SortType == "asc":
        SortType = "desc"
    else:
        SortType = "asc"
    return_data = select("select * from manga order by mid "+SortType+";")
    for i, item in enumerate(return_data):
        return_data[i] = dict(item)
        return_data[i]['insert_time'] = return_data[i]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        return_data[i]['update_time'] = return_data[i]['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    data = {"code": 200, "success": True, "data": return_data}
    return jsonify(data)


# modify data
@main.route("/modify/<string:mid>", methods=['GET'])
def ModifyGetData(mid):
    return_data = select("select * from manga where mid =:val", {"val": mid})
    return_data[0] = dict(return_data[0])
    return_data[0]['insert_time'] = return_data[0]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
    return_data[0]['update_time'] = return_data[0]['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    data = {"code": 200, "success": True, "data": return_data}
    return jsonify(data)


# delete data
@main.route("/del/<string:mid>", methods=['GET'])
def DelGetData(mid):
    sqlOP("delete from manga where mid =:val", {"val": mid})
    data = {"code": 200, "success": True, "data": "del success"}
    return jsonify(data)
