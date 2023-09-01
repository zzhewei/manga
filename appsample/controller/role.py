from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..decorators import admin_required
from ..model import Likes, Role, User, db, select
from .form import ChangePermissionForm, SearchForm

role = Blueprint("role", __name__)


# show user role data and update user role
@role.route("/UserRole", methods=["GET", "POST"])
@role.route("/UserRole/<int:page>", methods=["GET", "POST"])
@login_required
@admin_required
def UserRole(page=1):
    sel_str = ""
    form = ChangePermissionForm()
    form1 = SearchForm()
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
            Likes.query.filter_by(user_id=form.uid.data).delete()
            User.query.filter_by(id=form.uid.data).delete()
            db.session.commit()
            flash("Delete Success")
        # clear the form
        return redirect(url_for("role.UserRole"))

    if form1.validate_on_submit():
        sel_str = form1.data["search"]

    users = (
        User.query.filter(User.username.like("%" + sel_str + "%"))
        .join(Role)
        .add_columns(
            User.id,
            User.username,
            User.account,
            User.email,
            User.confirmed,
            Role.id.label("role_id"),
            Role.name.label("role_name"),
        )
        .paginate(page, 5, False)
    )
    print("change_form", form.errors)
    print("search_form", form1.errors)
    return render_template("role.html", form=form, form1=form1, users=users)
