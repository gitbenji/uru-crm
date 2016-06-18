# -*- coding: utf-8 -*-
"""
    manage
    ~~~~~~

    Flask-Script Manager
"""

import os
import sqlalchemy

from flask.ext.script import Manager
from flask.ext.migrate import MigrateCommand

from fbone import create_app
from fbone.extensions import db
from fbone.utils import PROJECT_PATH, MALE
from fbone.modules.user import User, ADMIN, ACTIVE

from fbone.modules.user.commands import CreateUserCommand, DeleteUserCommand, ListUsersCommand


app = create_app()
manager = Manager(create_app)
manager.add_option('-c', '--config', dest='config', required=False)
manager.add_command('create_user', CreateUserCommand())
manager.add_command('delete_user', DeleteUserCommand())
manager.add_command('list_users', ListUsersCommand())
manager.add_command('db', MigrateCommand)


@manager.command
def initdb():
    """Init/reset database."""

    try:
        db.drop_all()
    except sqlalchemy.exc.OperationalError:
        URI = app.config['SQLALCHEMY_DATABASE_URI'][:app.config['SQLALCHEMY_DATABASE_URI'].rfind('/')]
        engine = sqlalchemy.create_engine(URI)
        engine.execute("CREATE DATABASE fbone")

    db.create_all()

    admin = User(
        name=u'admin',
        fullname=u'Agador Spartacus',
        email=u'admin@example.com',
        password=u'123456',
        role_code=ADMIN,
        status_code=ACTIVE,
        gender_code=MALE,
        bio=u'FSU Grad. Go Noles!')
    db.session.add(admin)
    db.session.commit()


@manager.command
def tests():
    """Run the tests."""
    import pytest
    cmd = pytest.main([os.path.join(PROJECT_PATH, 'tests'), '--verbose'])
    return cmd


if __name__ == "__main__":
    manager.run()
