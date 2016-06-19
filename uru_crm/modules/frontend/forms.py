# -*- coding: utf-8 -*-

from flask import Markup, current_app

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import (ValidationError, BooleanField, TextField, HiddenField, PasswordField,
    SubmitField, RadioField, SelectMultipleField)
from wtforms.validators import (Required, Length, EqualTo, Email)
from flask.ext.babel import lazy_gettext as _

from uru_crm.modules.user import User
from uru_crm.utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, PHONENUMBER_LENGTH)
from uru_crm.extensions import db


class LoginForm(Form):
    next = HiddenField()
    login = TextField(_('Username or email'), [Required()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)])
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Sign in'))


class SignupForm(Form):
    next = HiddenField()

    first_name = TextField(_('First Name'))

    last = TextField(_('Last Name'))

    email = EmailField(_('Email'), [Required(), Email()])

    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)], description=_('%(minChar)s characters or more! Be tricky.',
        minChar=PASSWORD_LEN_MIN))

    phone_number = TextField(_('Phone number'), [Required(), Length(PHONENUMBER_LENGTH)])

    address_1 = TextField(_('Street Address'))

    address_2 = TextField(_('City, State, ZIP'))

    delivery_preference = TextField(_('Delivery Preferences'), description=_("(ex. Leave box on the back porch)"))

    quantity = RadioField('Who are we feeding?', choices=[('value','just me!'),('value_two','me and wifey'),('three','the whole fam<3')])

    duration = RadioField('Duration?', choices=[('value','One week($50)'),('value_two','One Month($45)'),('three','Three Months($40)')], description=_("Any veggies you would like to avoid?"))

    avocados=_('avocados')
    cilantro = BooleanField(_('cilantro'))
    watermelon = BooleanField(_('watermelon'))
    peas = BooleanField(_('peas'))

    agree = BooleanField(_('Agree to the ') +
        Markup('<a target="blank" href="/terms">' + _('Terms of Service') + '</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This username is taken'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is taken'))

    def signup(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
        return user


class RecoverPasswordForm(Form):
    email = EmailField(_('Your email'), [Email()])
    submit = SubmitField(_('Send instructions'))


class ChangePasswordForm(Form):
    activation_key = HiddenField()
    password = PasswordField(_('Password'), [Required()])
    password_again = PasswordField(_('Password again'), [EqualTo('password',
        message="Passwords don't match")])
    submit = SubmitField(_('Save'))


class ReauthForm(Form):
    next = HiddenField()
    password = PasswordField(_('Password'), [Required(),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    submit = SubmitField(_('Reauthenticate'))


class OpenIDForm(Form):
    openid = TextField(_('Your OpenID'), [Required()])
    submit = SubmitField(_('Log in with OpenID'))

    def login(self, oid):
        openid = self.openid.data
        current_app.logger.debug('login with openid(%s)...' % openid)
        return oid.try_login(openid, ask_for=['email', 'fullname', 'nickname'])


class CreateProfileForm(Form):
    openid = HiddenField()
    name = TextField(_('Choose your username'), [Required(), Length(USERNAME_LEN_MIN,
        USERNAME_LEN_MAX)], description=_("Don't worry. you can change it later."))
    email = EmailField(_('Email'), [Required(), Email()],
        description=_("What's your email address?"))
    password = PasswordField(_('Password'), [Required(),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)],
        description=_('%(minChar)s characters or more! Be tricky.',
        minChar=PASSWORD_LEN_MIN))
    submit = SubmitField(_('Create Profile'))

    def validate_name(self, field):
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This username is taken.'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is taken.'))

    def create_profile(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()
