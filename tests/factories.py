# -*- coding: utf-8 -*-
"""
    tests.factories
    ~~~~~~~~~~~~~~~

    object factory for testing application data models
"""

from factory import Sequence
from factory.alchemy import SQLAlchemyModelFactory

from fbone.modules.user import User
from fbone.extensions import db


class BaseFactory(SQLAlchemyModelFactory):

    class Meta:
        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    name = Sequence(lambda n: "user{0}".format(n))
    email = Sequence(lambda n: "user{0}@example.com".format(n))
    fullname = Sequence(lambda n: "user{0}".format(n))

    class Meta:
        model = User