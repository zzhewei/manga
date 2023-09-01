###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
###########
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from .. import login_manager
from ..mail import send_email_celery
from ..model import User, db
from .form import ChangePasswordForm, LoginForm, RegistrationForm

auth = Blueprint("auth", __name__)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            email=form.email.data.lower(),
            username=form.username.data,
            account=form.account.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()

        token = user.generate_confirmation_token()
        url = url_for("auth.confirm", token=token, _external=True)
        send_email_celery.delay(user.email, "Confirm Your Account", "mail_confirm", username=user.username, url=url)
        flash("A confirmation email has been sent to you by email.")
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route("/confirm/<token>")
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for("main.MainPage"))
    if current_user.confirm(token):
        db.session.commit()
        flash("You have confirmed your account. Thanks!")
    else:
        flash("The confirmation link is invalid or has expired.")
    return redirect(url_for("main.MainPage"))


@auth.route("/login", methods=["GET", "POST"])
# @csrf.exempt
def login():
    """
    登入
    ---
    tags:
      - test
    parameters:
      - name: body
        in: body
        required: true
        schema:
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    produces: application/json
    responses:
      404:
        description: Page Not Fond
      500:
        description: Internal Server Error
      200:
        description: OK
    """
    if not current_user.is_authenticated:
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter((User.email == form.account.data) | (User.account == form.account.data)).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    # next(the url before login)
                    url_next = request.args.get("next")
                    if url_next is None or not url_next.startswith("/"):
                        return redirect(url_for("main.MainPage"))
                    return redirect(url_next)
            flash("Invalid account or password.")
        return render_template("login.html", form=form)
    return redirect(url_for("main.MainPage"))


@auth.route("/logout")
@login_required
def logout():
    """
    登出
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
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash("Your password has been updated.")
            return redirect(url_for("main.MainPage"))
        else:
            flash("Invalid password.")
    return render_template("change_password.html", form=form)
