from flask_login import login_required
from ..model import select, sqlOP, Permission, db, User
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session, request, flash
from ..decorators import admin_required, permission_required
from .form import ModifyForm
import json
import datetime

permission = Blueprint('permission', __name__)


# delete data
@permission.route("/UserPermission", methods=['GET'])
def UserPermission():
    users = select("SELECT id, username, email, confirmed, role_id FROM user;")
    return render_template('permission.html', users=users)
