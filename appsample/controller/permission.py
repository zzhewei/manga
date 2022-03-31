from flask_login import login_required
from ..model import select, sqlOP, Permission, db, User
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session, request, flash
from ..decorators import admin_required, permission_required
from .form import ModifyForm
import json
import datetime

permission = Blueprint('permission', __name__)


# show user permission data
@permission.route("/UserPermission", methods=['GET'])
def UserPermission():
    users = select("SELECT user.id, username, email, confirmed, roles.name as permission_name FROM user left join roles on user.role_id = roles.id;")
    permissions = select("SELECT id, name FROM roles;")
    return render_template('permission.html', users=users, permissions=permissions)
