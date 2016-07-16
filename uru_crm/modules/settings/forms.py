# -*- coding: utf-8 -*-

import os
import hashlib
from datetime import datetime

from flask import current_app
from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import (ValidationError, TextField, HiddenField, PasswordField, SubmitField,
    TextAreaField, IntegerField, RadioField, FileField)
from wtforms.validators import (Required, Length, EqualTo, Email, AnyOf, Optional)
from flask.ext.babel import lazy_gettext as _
from flask.ext.login import current_user

from uru_crm.utils import (PASSWORD_LEN_MIN, PASSWORD_LEN_MAX,
        USERNAME_LEN_MIN, USERNAME_LEN_MAX, PHONENUMBER_LENGTH, CARDNUMBER_LENGTH, CVCNUMBER_LENGTH)
from uru_crm.utils import allowed_file, ALLOWED_AVATAR_EXTENSIONS, make_dir
from uru_crm.utils import GENDER_TYPE
from uru_crm.extensions import db
from uru_crm.modules.user import User
import uru_crm.modules.mixins.stripe_mix as stripe_conts


class ProfileForm(Form):
    multipart = True
    next = HiddenField()
    first_name = TextField(_('First Name'))
    last_name = TextField(_('Last Name'))
    email = EmailField(_('Email'), [Required(), Email()])
    phone_num = TextField(_('Phone number'), [Required(), Length(PHONENUMBER_LENGTH)])
    address = TextField(_('Address'), [Required()])

    box_size = RadioField('Who are we feeding?', choices=[('single', 'Just me!'), ('couple', 'Me and bae'), ('family', 'The whole fam<3')])
    submit = SubmitField(_('Save'))

    def create_profile(self, request, user):

        self.populate_obj(user)

        db.session.add(user)
        db.session.commit()

        stripe_conts.update_subscription(user, user.box_size)


class PasswordForm(Form):
    next = HiddenField()
    password = PasswordField(_('Current password'), [Required()])
    new_password = PasswordField(_('New password'), [Required(),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX)])
    password_again = PasswordField(_('Password again'), [Required(),
        Length(PASSWORD_LEN_MIN, PASSWORD_LEN_MAX), EqualTo('new_password')])
    submit = SubmitField(_('Save'))

    def validate_password(form, field):
        user = User.get_by_id(current_user.id)
        if not user.check_password(field.data):
            raise ValidationError(_("Password is wrong."))

    def update_password(self, user):
        self.populate_obj(user)
        user.password = self.new_password.data

        db.session.add(user)
        db.session.commit()
