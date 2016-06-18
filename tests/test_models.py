# -*- coding: utf-8 -*-
"""
    tests.test_models
    ~~~~~~~~~~~~~~~~~

    tests for application data models
"""

# import datetime as dt

import pytest

from fbone.modules.user import User, USER
from .factories import UserFactory


@pytest.mark.usefixtures('session')
class TestUser:

    def test_get_by_id(self):
        user = User(name='bar', email='bar@bar.com', fullname='bar')
        User().save(user)
        retrieved = User().get_by_id(user.id)
        assert retrieved == user

    # def test_created_at_defaults_to_datetime(self):
    #     user = User(name='qux', email='qux@bar.com')

    def test_password_is_nullable(self):
        user = User(name='zap', email='zap@bar.com')
        assert user.password is None

    def test_factory(self, db):
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.name)
        assert bool(user.email)
        assert user.is_admin() is False
        assert user.check_password('myprecious')

    # def test_check_password(self):
    #     user = User.create(username="foo", email="foo@bar.com",
    #                 password="foobarbaz123")
    #     assert user.check_password('foobarbaz123') is True
    #     assert user.check_password("barfoobaz") is False

    # def test_full_name(self):
    #     user = UserFactory(first_name="Foo", last_name="Bar")
    #     assert user.full_name == "Foo Bar"

    def test_roles(self):
        u = User(name='qux', email='qux@bar.com', fullname='qux')
        User().save(u)
        assert u.role_code == USER
