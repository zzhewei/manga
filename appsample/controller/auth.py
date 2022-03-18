###########
# reference:https://github.com/testdrivenio/flask-spa-auth/blob/master/flask-spa-same-origin/backend/app.py
#           https://github.com/PrettyPrinted/building_user_login_system/blob/master/finish/app.py
#           https://github.com/miguelgrinberg/flasky/blob/master/app/models.py
#           https://hackmd.io/@shaoeChen/HJiZtEngG/https%3A%2F%2Fhackmd.io%2Fs%2Fryvr_ly8f
###########
from flask_login import login_required, login_user, logout_user, current_user
from .. import login_manager, csrf
from ..model import User, db
from .form import LoginForm, RegistrationForm
from flask import Blueprint, request, jsonify, flash, render_template, redirect, url_for
from flask_wtf.csrf import generate_csrf
auth = Blueprint('auth', __name__)


@login_manager.user_loader
def load_user(uid):
    return User.query.get(uid)


@auth.route("/GetCsrf", methods=["GET"])
def get_csrf():
    token = generate_csrf()
    response = jsonify({"Success": True})
    response.headers.set("csrf_token", token)
    return response


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data.lower(),
                    username=form.username.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth.route("/login", methods=['GET', 'POST'])
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
            user = User.query.filter_by(username=form.account.data).first()
            if user:
                if user.check_password(form.password.data):
                    login_user(user, form.remember_me.data)
                    # next(the url before login)
                    next = request.args.get('next')
                    if next is None or not next.startswith('/'):
                        return redirect(url_for('main.MainPage'))
                    return redirect(next)
            flash('Invalid account or password.')
        return render_template('login.html', form=form)
    return redirect(url_for('main.MainPage'))


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
    return redirect(url_for('auth.login'))


@auth.route('/session', methods=["POST"])
def get_session():
    if not current_user.is_authenticated:
        return jsonify({'status': 'error'}), 401
    return jsonify({'status': 'success', 'user': current_user.to_json()})
