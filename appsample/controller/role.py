from flask_login import login_required, current_user
from ..model import select, sqlOP, Permission, db, User, Role
from flask import Blueprint, jsonify, current_app, render_template, redirect, url_for, session, request, flash
from ..decorators import admin_required, permission_required
from .form import ChangePermissionForm

role = Blueprint('role', __name__)


# show user role data and update user role
@role.route("/UserRole", methods=['GET', 'POST'])
@role.route("/UserRole/<int:page>", methods=['GET', 'POST'])
def UserRole(page=1):
    form = ChangePermissionForm()
    # 一定要寫在validate_on_submit前面 不然會抓不到choice 導致Not a valid choice.
    form.userrole.choices = [(i.id, i.name) for i in select("SELECT id, name FROM roles;")]
    if form.validate_on_submit():
        if form.submit.data:
            user = User.query.filter_by(id=form.uid.data).first()
            user.username = form.username.data
            user.role_id = form.userrole.data
            db.session.commit()
            flash("Update Success")
        else:
            User.query.filter_by(id=form.uid.data).delete()
            db.session.commit()
            flash("Delete Success")
        # clear the form
        return redirect(url_for('role.UserRole'))

    users = User.query.join(Role).add_columns(User.id, User.username, User.account, User.email, User.confirmed, Role.id.label("role_id"), Role.name.label("role_name")).paginate(page, 5, False)
    print(form.errors)
    return render_template('role.html', form=form, users=users)
