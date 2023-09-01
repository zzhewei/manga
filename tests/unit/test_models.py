import time

from appsample.model import AnonymousUser, Permission, Role, User, db


class Test_user:
    def test_new_user(self):
        user = User(
            role_id=1, email="test12345@gmail.com", username="test2", account="test2", password="test2", confirmed=False
        )
        assert user.email == "test12345@gmail.com"
        assert user.password_hash != "test2"

    def test_password_setter(self):
        u = User(password="cat")
        assert u.password_hash is not None

    def test_password_salts_are_random(self):
        u = User(password="cat")
        u2 = User(password="cat")
        assert u.password_hash != u2.password_hash

    def test_valid_confirmation_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token()
        assert u.confirm(token)

    def test_invalid_confirmation_token(self):
        u1 = User(password="cat")
        u2 = User(password="dog")
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        token = u1.generate_confirmation_token()
        assert not u2.confirm(token)

    def test_expired_confirmation_token(self):
        u = User(password="cat")
        db.session.add(u)
        db.session.commit()
        token = u.generate_confirmation_token(1)
        time.sleep(2)
        assert not u.confirm(token)


class Test_role:
    def test_user_role(self):
        u = User(email="john@example.com", password="cat")
        assert u.can(Permission.READ)
        assert not u.can(Permission.WRITE)
        assert not u.can(Permission.MODIFY)
        assert not u.can(Permission.ADMIN)

    def test_moderator_role(self):
        r = Role.query.filter_by(name="Moderator").first()
        u = User(email="john1@example.com", password="cat1", role=r)
        assert u.can(Permission.READ)
        assert u.can(Permission.WRITE)
        assert u.can(Permission.MODIFY)
        assert not u.can(Permission.ADMIN)

    def test_administrator_role(self):
        r = Role.query.filter_by(name="Administrator").first()
        u = User(email="john2@example.com", password="cat2", role=r)
        assert u.can(Permission.READ)
        assert u.can(Permission.WRITE)
        assert u.can(Permission.MODIFY)
        assert u.can(Permission.ADMIN)

    def test_anonymous_user(self):
        u = AnonymousUser()
        assert not u.can(Permission.READ)
        assert not u.can(Permission.WRITE)
        assert not u.can(Permission.MODIFY)
        assert not u.can(Permission.ADMIN)
