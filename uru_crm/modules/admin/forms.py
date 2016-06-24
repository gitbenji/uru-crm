# -*- coding: utf-8 -*-

from flask import Markup, current_app, Flask, render_template

from flask.ext.wtf import Form
from flask.ext.wtf.html5 import EmailField
from wtforms import (HiddenField, SubmitField, RadioField, FileField, DateField, TextField, DecimalField)
from wtforms.validators import AnyOf, Required, Email
from flask.ext.babel import lazy_gettext as _

from uru_crm.extensions import db
from uru_crm.modules.user import USER_ROLE, USER_STATUS, Box
from uru_crm.modules.farm import Farm


class UserForm(Form):
    next = HiddenField()
    role_code = RadioField(u"Role", [AnyOf([str(val) for val in USER_ROLE.keys()])],
            choices=[(str(val), label) for val, label in USER_ROLE.items()])
    status_code = RadioField(u"Status", [AnyOf([str(val) for val in USER_STATUS.keys()])],
            choices=[(str(val), label) for val, label in USER_STATUS.items()])
    # A demo of datepicker.
    created_time = DateField(u'Created time')
    submit = SubmitField(u'Save')

    def save(self, user):
        self.populate_obj(user)
        db.session.add(user)
        db.session.commit()


class NewBoxesForm(Form):
    next = HiddenField()
    date = DateField(_('Date'))
    veggies = TextField(_('Vegetable'))
    # quantity = DecimalField(_('Quantity'))
    add = SubmitField()
    submit = SubmitField(u'Create', [Required()])

    def add_set(self):
        pass

    def combine_veggies(self):
        print('combine_veggies')

    def save(self):
        box = Box()
        self.populate_obj(box)
        box.group = 1
        db.session.add(box)
        db.session.commit()
        return box


class NewFarmForm(Form):
    next = HiddenField()
    farm = TextField(_('Farm Name'))
    phone_num = TextField(_('Phone Number'))
    email = EmailField(_('Email'), [Required(), Email()])
    address = TextField(_('Address'))
    submit = SubmitField(u'Sign up')

    def save(self):
        farm = Farm()
        self.populate_obj(farm)
        db.session.add(farm)
        db.session.commit()
        return farm


class EditTranslationForm(Form):
    multipart = True
    file = FileField(u"Upload Translation File")
    language = HiddenField()
    submit = SubmitField(u'Save')


class UploadLogoForm(Form):
    multipart = True
    file = FileField(u"Upload Logo File")
    submit = SubmitField(u'Save')
