# -*- coding: utf-8 -*-

from flask import Markup, current_app, Flask, render_template

from flask.ext.wtf import Form
from wtforms import (ValidationError, BooleanField, TextField, HiddenField, IntegerField, PasswordField, SubmitField, RadioField, SelectMultipleField, widgets)
from wtforms.validators import (Required, Length, EqualTo, Email)
from flask.ext.babel import lazy_gettext as _

from uru_crm.modules.user import User
from uru_crm.utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, PHONENUMBER_LENGTH, CARDNUMBER_LENGTH, CVCNUMBER_LENGTH)
from uru_crm.extensions import db

import uru_crm.modules.mixins.stripe_mix as stripe_conts


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class LoginForm(Form):
    id = 'login'
    next = HiddenField()
    login = TextField(_('Username or email'), [Required()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)])
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Sign in'))


class StripeForm(Form):
    next = HiddenField()

    first_name = TextField((''), [Required()], description='First Name')
    last_name = TextField((''), [Required()], description='Last Name')
    email = TextField((''), [Required(), Email()], description='Email Address')
    password = PasswordField((''), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)], description='Password')
    # password_verification
    retype_password = PasswordField((''), description='Retype Password')

    phone_num = TextField((''), [Length(PHONENUMBER_LENGTH)], description='Phone Number')
    address = TextField((''), [Required()], description='Street Address')
    address_2 = TextField((''), description='Apt/Bldg No')
    city = TextField((''), [Required()], default='Tallahassee', description='City')
    state = TextField((''), [Required()], default='FL', description='State')
    postal_zip = TextField((''), [Required()], description='Postal Code')

    box_size = RadioField('What size box is needed?', [Required()], choices=[('single', 'Enough for 1 person ($25)'),
            ('couple', 'Enough for 2 persons ($45)'),
            ('family', 'Enough for 4 persons ($75)')])

    # box_size = HiddenField()

    card_number = TextField((''), [Required()], description='Card Number')
    exp_month = IntegerField((''), [Required()], description='Expiration (mm)')
    exp_year = IntegerField((''), [Required()], description='Expiration (yy)')
    cvc_number = IntegerField((''), [Required()], description='CVC')

    agree = BooleanField(_('Agree to the ') +
        Markup('<a target="blank" href="/terms">' + _('Terms of Service') + '</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is taken'))

    def validate_retype_password(self, field):
        if field.data != self.password.data:
            raise ValidationError(_('Passwords do not match'))

    def validate_card_number(self, field):
        pass

    # def validate_last_name(self, field):
    #     if User.query.filter_by(last_name=field.data).first() is not None:
    #         raise ValidationError(_('This last name is taken'))

    def signup(self):
        card_vals = {
          'number': self.card_number.data,
          'cvc': self.cvc_number.data,
          'exp_month': self.exp_month.data,
          'exp_year': self.exp_year.data
        }
        cid = stripe_conts.create_customer(card_vals, self.email.data)
        user = User()
        self.populate_obj(user)
        user.customer_id = cid
        self.address = self.address.data + ', ' + \
            self.address_2.data + ', ' + \
            self.city.data + ', ' + \
            self.state.data + ' ' + \
            self.postal_zip.data
        User().save(user)
        return user


class RecoverPasswordForm(Form):
    email = TextField(_('Your email'), [Email()])
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
    email = TextField(_('Email'), [Required(), Email()],
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
