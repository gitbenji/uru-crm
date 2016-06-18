# Manekineko

Manekineko is a fork of [Fbone](https://github.com/imwilsonxu/fbone), a [Flask](http://flask.pocoo.org) (Python microframework) boilerplate application with best practices, using a domain driven approach.

[![Build Status](http://ci.cuttlesoft.net/buildStatus/icon?job=manekineko)](http://ci.cuttlesoft.net/job/manekineko)

You can use it for:

- learning Flask
- kicking off your new project faster
- having a highly scalable and modular app structure


## FEATURES

### Frontend Framework

- [HTML5 Boilerplate](https://github.com/h5bp/html5-boilerplate)
- [jQuery](http://jquery.com/)
- [Bootstrap](https://getbootstrap.com)

### Flask Extensions

- Handle **orm** with [SQLAlchemy](http://www.sqlalchemy.org)
- Handle **migrations** with [Flask-Migrate](https://flask-migrate.readthedocs.org/en/latest/) and [Alembic](https://alembic.readthedocs.org/en/latest/)
- Handle **web forms** with [WTForms](http://wtforms.simplecodes.com/)
- Implement **user session management** with [Flask-Login](https://github.com/maxcountryman/flask-login)
- Implement **reset password via email** with [Flask-Mail](http://packages.python.org/Flask-Mail/)
- Implement **unit testing** with [Pytest](http://pytest.org)
- Implement **external script** with [Flask-Script](http://flask-script.readthedocs.org/en/latest/)
- Handle **i18n** with [Flask-Babel](http://packages.python.org/Flask-Babel/)

### Others

- Well designed structure for **large projects**
- Quick deploys via [fabric](flask.pocoo.org/docs/patterns/fabric/)
- Admin interface
- Homebaked logger

## USAGE

Pre-required:

- git
- pip
- sqlite

Suggested:

- virtualenv
- virtualenv wrapper
- MySQL/PostgreSQL

To get started, verify database settings in `fbone/config.py` then run:

```
$ python manage.py initdb
```

Then start the server with:

```
$ python manage.py runserver
```
Then open `http://127.0.0.1:5000`

**IMPORTANT**:

- Change `INSTANCE_FOLDER_PATH` in `fbone/utils.py` to suit yourself.
- Put `*.cfg` under `INSTANCE_FOLDER_PATH`.

```
## STRUCTURE

    ├── fbone
    │   ├── factory.py              (application factory)
    │   ├── config.py               (config module)
    │   ├── decorators.py           (route decorators)
    │   ├── extensions.py           (flask extensions)
    │   ├── modules                 (MVC modules)
    │   │   ├── admin               (admin module)
    │   │   ├── api                 (api module)
    │   │   ├── frontend            (frontend module)
    │   │   ├── settings            (settings module)
    │   │   └── user                (user module)
    │   │       ├── __init__.py
    │   │       ├── commands.py
    │   │       ├── constants.py
    │   │       ├── forms.py
    │   │       ├── models.py
    │   │       └── views.py
    │   ├── core                    (core app utilities)
    │   │   ├── email.py            (email methods)
    │   │   ├── flash.py            (flask.flash() wrapper)
    │   │   ├── helpers.py          (convenience functions and classes)
    │   │   └── oauth.py            (oauth settings and provider logic)
    │   ├── static
    │   │   ├── css
    │   │   ├── img
    │   │   └── js
    │   ├── templates
    │   ├── translations            (i18n)
    │   ├── utils.py
    ├── LICENSE
    ├── manage.py                   (manage via flask-script)
    ├── README.md
    └── tests                       (unit tests, run with pytest)
```

## LICENSE

[MIT LICENSE](http://www.tldrlegal.com/license/mit-license)

## ACKNOWLEDGEMENTS

Thanks to [Flask extension](http://flask.pocoo.org/extensions/) authors, various blogs, and the hard work of:
- [Matt Upstate](http://mattupstate.com/)
- [Miguel Grinberg](http://blog.miguelgrinberg.com/)
- [Armin Ronacher](http://lucumr.pocoo.org/)

Original work done by:
- [Wilson Xu](http://imwilsonxu.com), created Fbone
- [Muhammad Ahsan Ali](https://github.com/ahsanali), original Manekineko fork