# -*- coding: utf-8 -*-

import os

from flask import Flask, request, render_template
from flask.ext.babel import Babel

from uru_crm import assets
from uru_crm.config import HerokuConfig
from uru_crm.modules.user import User, user
from uru_crm.modules.settings import settings
from uru_crm.modules.frontend import frontend
from uru_crm.modules.api import api
from uru_crm.modules.admin import admin
from uru_crm.extensions import db, migrate, mail, cache, login_manager
from uru_crm.utils import PROJECT_PATH, INSTANCE_FOLDER_PATH


# For import *
__all__ = ['create_app']

DEFAULT_BLUEPRINTS = (
    frontend,
    user,
    settings,
    api,
    admin,
)


def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""

    if app_name is None:
        app_name = HerokuConfig.PROJECT
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(app_name, instance_path=INSTANCE_FOLDER_PATH, instance_relative_config=True)

    # Init assets
    assets.init_app(app)

    configure_app(app, config)
    configure_hook(app)
    configure_blueprints(app, blueprints)
    configure_extensions(app)
    configure_logging(app)
    configure_template_filters(app)
    configure_error_handlers(app)

    return app


def configure_app(app, config=None):
    # http://flask.pocoo.org/docs/api/#configuration
    # inherit the base config object
    app.config.from_object(HerokuConfig)

    # If config is None, try to load config file from environment variable
    if config is None and 'uru_crm_CFG' in os.environ:
        # Use instance folder instead of env variables to make deployment easier.
        config = os.environ['uru_crm_CFG']

    # check for config last time in case it was stored as ENV variable
    if config:
        # pass configuration file in with application manager
        config_file = os.path.join(PROJECT_PATH, config)
        app.config.from_pyfile(config_file, silent=False)

    @app.context_processor
    def utility_processor():
        def parse_list(list_string):
            # string_length = len(list_string)
            list_string = list_string[1:-1]
            return list_string.split(',')
        return dict(parse_list=parse_list)


def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)

    # flask-migrate
    migrate.init_app(app, db)

    # flask-mail
    mail.init_app(app)

    # flask-cache
    cache.init_app(app)

    # flask-babel
    babel = Babel(app)

    @babel.localeselector
    def get_locale():
        return request.accept_languages.best_match(HerokuConfig.LANGUAGES)

    # flask-login
    login_manager.login_view = 'frontend.login'
    login_manager.refresh_view = 'frontend.reauth'

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(id)
    login_manager.setup_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views."""

    for blueprint in blueprints:
        app.register_blueprint(blueprint)


def configure_template_filters(app):

    @app.template_filter()
    def pretty_date(value):
        return pretty_date(value)

    @app.template_filter()
    def format_date(value, format='%Y-%m-%d'):
        return value.strftime(format)


def configure_logging(app):
    """Configure file(info) and email(error) logging."""

    if app.debug or app.testing:
        # Skip debug and test mode. Just check standard output.
        return

    import logging
    from logging.handlers import SMTPHandler

    # Set info level on logger, which might be overwritten by handers.
    # Suppress DEBUG messages.
    app.logger.setLevel(logging.INFO)

    info_log = os.path.join(app.config['LOG_FOLDER'], 'uru_crm.log')
    info_file_handler = logging.handlers.RotatingFileHandler(info_log, maxBytes=100000,
        backupCount=10)
    info_file_handler.setLevel(logging.INFO)
    info_file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(info_file_handler)

    # Testing
    # app.logger.info("testing info.")
    # app.logger.warn("testing warn.")
    # app.logger.error("testing error.")

    mail_handler = SMTPHandler(app.config['MAIL_SERVER'],
                               app.config['MAIL_USERNAME'],
                               app.config['ADMINS'],
                               'O_ops... %s failed!' % app.config['PROJECT'],
                               (app.config['MAIL_USERNAME'],
                                app.config['MAIL_PASSWORD']))
    mail_handler.setLevel(logging.ERROR)
    mail_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]')
    )
    app.logger.addHandler(mail_handler)


def configure_hook(app):
    @app.before_request
    def before_request():
        pass

    # @app.context_processor
    # def ctx_processor():
    #     pass


def configure_error_handlers(app):

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template("errors/forbidden_page.html"), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("errors/page_not_found.html"), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template("errors/server_error.html"), 500
