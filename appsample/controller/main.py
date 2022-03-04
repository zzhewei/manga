from flask_login import login_required
from ..model import select, sqlOP, Permission
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for
from ..decorators import admin_required, permission_required

main = Blueprint('main', __name__)
SortType = 'asc'


# main page
@main.route("/")
def MainPage():
    rows = select("select * from manga order by mid " + SortType + ";")
    return render_template('main.html', rows=rows)


# query sort by button
@main.route("/sort")
def MainPageSort():
    global SortType
    if SortType == 'asc':
        SortType = 'desc'
    return redirect(url_for('main.MainPage'))


# query sort by button
@main.route("/data")
def dataTest():
    test1 = 'fffff'
    return test1
