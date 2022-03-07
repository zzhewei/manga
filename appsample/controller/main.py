from flask_login import login_required
from ..model import select, sqlOP, Permission, db
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session
from ..decorators import admin_required, permission_required
from .form import ModifyForm
import json
import datetime

main = Blueprint('main', __name__)
SortType = 'asc'


# main page
@main.route("/", methods=['GET', 'POST'])
def MainPage():
    form = ModifyForm()
    if form.validate_on_submit():
        UpdateData = {"mid": form.mid.data, "url": form.url.data, "name": form.name.data, "page": form.pages.data, "author": form.author.data, "author_group": form.group.data, "update_time": datetime.datetime.now()}
        sqlOP("update manga set url = :url, name= :name, page= :page, author= :author, author_group= :author_group, update_time= :update_time where mid = :mid", UpdateData)
        print("Success")
    rows = select("select * from manga order by mid " + SortType + ";")
    return render_template('main.html', rows=rows, form=form)


# query sort by button
@main.route("/sort")
def MainPageSort():
    global SortType
    if SortType == 'asc':
        SortType = 'desc'
    return redirect(url_for('main.MainPage'))


# query sort by button
@main.route("/<string:mid>", methods=['GET'])
def ModifyGetData(mid):
    return_data = select("select * from manga where mid =:val", {"val": mid})
    return_data[0] = dict(return_data[0])
    return_data[0]['insert_time'] = return_data[0]['insert_time'].strftime('%Y-%m-%d %H:%M:%S')
    return_data[0]['update_time'] = return_data[0]['update_time'].strftime('%Y-%m-%d %H:%M:%S')
    data = {"code": 200, "success": True, "data": return_data}
    return jsonify(data)
