# -*- coding: utf-8 -*-
"""
    tests.test_config
    ~~~~~~~~~~~~~~~~~

    test application configuration
"""

from uru_crm.factory import create_app
from uru_crm.config import TestConfig


def test_default_config():
    app = create_app()
    assert app.config['DEBUG'] is True
    assert app.config['TESTING'] is False


def test_test_config():
    app = create_app()
    app.config.from_object(TestConfig)
    assert app.config['TESTING'] is True
