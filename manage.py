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

from uru_crm import create_app
from uru_crm.extensions import db
from uru_crm.utils import PROJECT_PATH, MALE
from uru_crm.modules.user import User, ADMIN, ACTIVE, Farm, Available_Veggie

from uru_crm.modules.user.commands import CreateUserCommand, DeleteUserCommand, ListUsersCommand


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
        engine = sqlalchemy.create_engine(URI, isolation_level='AUTOCOMMIT')
        engine.execute("CREATE DATABASE uru_crm")

    db.create_all()

    admin = User(
        first_name=u'Benji',
        last_name=u'Shankwitz',
        email=u'bshankwitz@gmail.com',
        phone_num='5617231122',
        address=u'211 Westridge Dr, Tallahassee, FL., 32304',
        password=u'bianca',
        box_size=u'single',
        duration=u'forever',
        role_code=ADMIN,
        status_code=ACTIVE)
    db.session.add(admin)

    farm = Farm(
        farm=u'Pita Queen, LLC',
        phone_num=u'1234567890',
        email=u'pita@gmail.com',
        address=u'123 Main Street'
    )
    db.session.add(farm)

    veggie = Available_Veggie(
        veggie=u'Potato',
        farm=u'Pita Queen, LLC',
        quantity=u'50lbs'
    )
    db.session.add(veggie)

    db.session.commit()


@manager.command
def tests():
    """Run the tests."""
    import pytest
    cmd = pytest.main([os.path.join(PROJECT_PATH, 'tests'), '--verbose'])
    return cmd


if __name__ == "__main__":
    manager.run()
