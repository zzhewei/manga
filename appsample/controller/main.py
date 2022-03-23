from flask_login import login_required
from ..model import select, sqlOP, Permission, db, User
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session, request, flash
from ..decorators import admin_required, permission_required
from .form import ModifyForm
import json
import datetime

main = Blueprint('main', __name__)
SortType = "asc"


# index
@main.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# main page
@main.route("/main", methods=['GET', 'POST'])
def MainPage():
    form = ModifyForm()
    if form.validate_on_submit() and form.submit.data:
        if form.mid.data:
            UpdateData = {"mid": form.mid.data, "url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data, "update_time": datetime.datetime.now()}
            sqlOP("update manga set url = :url, name= :name, page= :page, author= :author, author_group= :author_group, update_time= :update_time where mid = :mid", UpdateData)
            flash('Modify Success')
        else:
            InsertData = {"url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data,
                          "status": 0, "insert_time": datetime.datetime.now(), "update_time": datetime.datetime.now(), "update_user": "Jason"}
            sqlOP("insert into manga(url, name, page, author, author_group, status, insert_time, update_time, update_user) \
                values(:url, :name, :page, :author, :author_group, :status, :insert_time, :update_time, :update_user)", InsertData)
            flash('Insert Success')
    rows = select("select * from manga order by mid "+SortType+";")
    rand = select("select * from manga order by rand() limit 5")
    return render_template('main.html', rows=rows, rand=rand, form=form, Permission=Permission)


# fuzzy search
@main.route("/fuzzy", methods=['GET', 'POST'])
def FuzzySearch():
    PostDict = request.get_json()
    if PostDict['input']:
        return_data = select("select * from manga where url like concat('%', :val, '%') or name like concat('%', :val, '%') or author like concat('%', :val, '%')\
                            or author_group like concat('%', :val, '%')", {'val': PostDict['input']})
    else:
        return_data = select("select * from manga order by mid " + SortType + ";")

    for i, item in enumerate(return_data):
        return_data[i] = dict(item)
        return_data[i]['insert_time'] = return_data[i]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        return_data[i]['update_time'] = return_data[i]['update_time'].strftime('%Y-%m-%d %H:%M:%S')

    # data = {"code": 200, "success": True, "data": return_data}
    # return jsonify(data)
    return render_template('url.html', rows=return_data, Permission=Permission)


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
    # data = {"code": 200, "success": True, "data": return_data}
    # return jsonify(data)
    return render_template('url.html', rows=return_data, Permission=Permission)


# Query single modify data
@main.route("/modify/<string:mid>", methods=['GET'])
@login_required
@permission_required(Permission.MODIFY)
def ModifyGetData(mid):
    return_data = select("select * from manga where mid =:val", {"val": mid})
    return_data[0] = dict(return_data[0])
    return_data[0]['insert_time'] = return_data[0]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
    return_data[0]['update_time'] = return_data[0]['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    data = {"code": 200, "success": True, "data": return_data}
    return jsonify(data)


# delete data
@main.route("/del/<string:mid>", methods=['GET'])
@login_required
@admin_required
def DelGetData(mid):
    sqlOP("delete from manga where mid =:val", {"val": mid})
    return_data = select("select * from manga order by mid " + SortType + ";")
    for i, item in enumerate(return_data):
        return_data[i] = dict(item)
        return_data[i]['insert_time'] = return_data[i]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
        return_data[i]['update_time'] = return_data[i]['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    return render_template('url.html', rows=return_data, Permission=Permission)
