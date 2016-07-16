# -*- coding: utf-8 -*-

from flask import Markup, current_app, Flask, render_template

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
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
    next = HiddenField()
    login = TextField(_('Username or email'), [Required()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)])
    remember = BooleanField(_('Remember me'))
    submit = SubmitField(_('Sign in'))


class StripeForm(Form):
    next = HiddenField()

    first_name = TextField(_('First Name'), default='Fly')
    last_name = TextField(_('Last Name'), default='Robyn')
    email = EmailField(_('Email'), [Required(), Email()], default='email@gmail.com')
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)], description=_('%(minChar)s characters or more! Be tricky.',
        minChar=PASSWORD_LEN_MIN), default='asdfasdf')

    phone_num = TextField(_('Phone number'), [Required(), Length(PHONENUMBER_LENGTH)], default='1234567890')
    address = TextField(_('Address'), [Required()], default='123 High Rd')
    address_2 = TextField(_('City, State, ZIP'), default='Tallahassee')

    box_size = RadioField('Who are we feeding?', choices=[('single','Just me!'),('couple','Me and bae'),('family','The whole fam<3')], default='couple')

    card_number = TextField(_('Card Number'), [Required()], default='4242424242424242')
    exp_month = IntegerField(_('Expiration Date'), [Required()], default=12)
    exp_year = IntegerField(_(''), [Required()], default=17)
    cvc_number = IntegerField(_('CVC'), [Required()], default=123)

    agree = BooleanField(_('Agree to the ') +
        Markup('<a target="blank" href="/terms">' + _('Terms of Service') + '</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_email(self, field):
        pass
        # if User.query.filter_by(email=field.data).first() is not None:
        #     raise ValidationError(_('This email is taken'))

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
        User().save(user)
        return user


class SignupForm(Form):
    next = HiddenField()

    first_name = TextField(_('First Name'))
    last_name = TextField(_('Last Name'))
    email = EmailField(_('Email'), [Required(), Email()])
    password = PasswordField(_('Password'), [Required(), Length(PASSWORD_LEN_MIN,
        PASSWORD_LEN_MAX)], description=_('%(minChar)s characters or more! Be tricky.',
        minChar=PASSWORD_LEN_MIN))

    phone_num = TextField(_('Phone number'), [Required(), Length(PHONENUMBER_LENGTH)])
    address = TextField(_('Address'))
    # address_2 = TextField(_('City, State, ZIP'))

    delivery_instructs = TextField(_('Delivery Preferences'), description=_("(ex. Leave box on the back porch)"))
    box_size = RadioField('Who are we feeding?', choices=[('just me!','just me!'),('me and wifey','me and wifey'),('the whole fam<3','the whole fam<3')])
    duration = RadioField('Duration?', choices=[('One week($50)','One week($50)'),('One Month($45)','One Month($45)'),('Three Months($40)','Three Months($40)')], description=_("Any veggies you would like to avoid?"))

    list_of_veggies = ['avocados', 'cilantro', 'watermelon', 'peas']
    veggies = [(x, x) for x in list_of_veggies]
    bad_veggies = MultiCheckboxField('Label', choices=veggies)

    agree = BooleanField(_('Agree to the ') +
        Markup('<a target="blank" href="/terms">' + _('Terms of Service') + '</a>'), [Required()])
    submit = SubmitField('Sign up')

    def validate_name(self, field):
        # this never runs
        if User.query.filter_by(name=field.data).first() is not None:
            raise ValidationError(_('This username is taken'))

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None:
            raise ValidationError(_('This email is taken'))

    def signup(self):
        user = User()
        self.populate_obj(user)
        db.session.add(user)
        # try:
        db.session.commit()
        return user
        # # ???????????
        # except IntegrityError:
        #     db.session.rollback()
        #     raise Exception


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
