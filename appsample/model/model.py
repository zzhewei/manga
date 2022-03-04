###########
# reference:https://www.maxlist.xyz/2019/10/30/flask-sqlalchemy/
#           https://blog.csdn.net/weixin_42677653/article/details/106154452
###########
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()
migrate = Migrate()


class Permission:
    READ = 1
    WRITE = 2
    MODIFY = 4
    ADMIN = 8


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    @staticmethod
    def insert_roles():
        roles = {
            'User': [Permission.READ],
            'Moderator': [Permission.READ, Permission.WRITE, Permission.MODIFY],
            'Administrator': [Permission.READ, Permission.WRITE, Permission.MODIFY, Permission.ADMIN],
        }
        default_role = 'User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default = (role.name == default_role)
            db.session.add(role)
        db.session.commit()

    def add_permission(self, perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self, perm):
        if self.has_permission(perm):
            self.permissions -= perm

    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self, perm):
        return self.permissions & perm == perm

    def __repr__(self):
        return '<Role %r>' % self.name


class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(200))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    # property set method only read
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):
        return {'id': self.id, 'username': self.username}

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)


class Manga(db.Model):
    __tablename__ = 'manga'
    mid = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(500), nullable=False)
    name = db.Column(db.Text, nullable=False)
    page = db.Column(db.Text, nullable=True)
    author = db.Column(db.String(100), nullable=False)
    author_group = db.Column(db.String(100))
    status = db.Column(db.Boolean, nullable=False, default=False)
    insert_time = db.Column(db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    update_user = db.Column(db.String(50), nullable=False)

    def __init__(self, url, name, page, author, author_group, status, insert_time, update_time, update_user):
        self.url = url
        self.name = name
        self.page = page
        self.author = author
        self.author_group = author_group
        self.status = status
        self.insert_time = insert_time
        self.update_time = update_time
        self.update_user = update_user


def select(SqlContent, **args):
    data = db.session.execute(SqlContent, args)
    db.session.commit()
    return data.mappings().all()


def sqlOP(SqlContent, **args):
    try:
        db.session.execute(SqlContent, args)
        db.session.commit()
    except:
        db.session.rollback()
