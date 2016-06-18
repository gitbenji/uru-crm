# -*- coding: utf-8 -*-
"""
    tests.conftest
    ~~~~~~~~~~~~~~

    configuriation for pytests
"""

import os
import pytest

# from alembic.command import upgrade
# from alembic.config import Config

from fbone.factory import create_app
from fbone.config import TestConfig
from fbone.extensions import db as _db
from fbone.utils import INSTANCE_FOLDER_PATH


@pytest.fixture(scope='session')
def app(request):
    """Session-wide test `Flask` application."""
    app = create_app()
    app.config.from_object(TestConfig)

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


def apply_migrations(app):
    """Applies all alembic migrations."""
    # ALEMBIC_CONFIG = os.path.join(app.config['PROJECT_ROOT'], 'migrations/alembic.ini')
    # config = Config(ALEMBIC_CONFIG)
    # upgrade(config, 'head')
    pass


@pytest.fixture(scope='session')
def db(app, request):
    """Session-wide test database."""
    if os.path.exists(os.path.join(INSTANCE_FOLDER_PATH, 'test.sqlite')):
        os.unlink(os.path.join(INSTANCE_FOLDER_PATH, 'test.sqlite'))

    def teardown():
        _db.drop_all()
        os.unlink(os.path.join(INSTANCE_FOLDER_PATH, 'test.sqlite'))

    _db.app = app
    apply_migrations(app)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(db, request):
    """Creates a new database session for a test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    session = db.create_scoped_session()

    db.create_all()
    db.session = session

    def teardown():
        transaction.rollback()
        connection.close()
        session.remove()

    request.addfinalizer(teardown)
    return session
