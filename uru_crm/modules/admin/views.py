# -*- coding: utf-8 -*-

import os

from flask import (Blueprint, render_template, request, flash, current_app, send_from_directory,
    redirect, url_for)
from flask.ext.login import login_required
from flask.ext.babel import Babel
from wtforms import (HiddenField, SubmitField, RadioField, FileField, DateField, TextField, DecimalField)
from flask.ext.babel import lazy_gettext as _

from uru_crm.decorators import admin_required
from uru_crm.modules.farm import Farm
from uru_crm.modules.user import User, Box, WeeklyNumbers
from .forms import UserForm, EditTranslationForm, UploadLogoForm, NewFarmForm, NewBoxesForm

admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/')
@login_required
@admin_required
def index():
    users = User.query.all()
    logo_form = UploadLogoForm()
    return render_template('admin/index.html', users=users, active='index', logo_form=logo_form)

@admin.route('/boxes/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_boxes():
    form = NewBoxesForm(next=request.args.get('next'))
    print(dir(form))

    if form.validate_on_submit():
        form.combine_veggies()
        box = form.save()
        del NewBoxesForm.veggie2
        return redirect(form.next.data or url_for('admin.boxes'))

    # veggies = []
    # form is staying updated
    # try setting it back to normal at validate_on_submit()
    if form.is_submitted():
        # num_of_veggies += 1

        print(dir(form))
        setattr(NewBoxesForm, 'veggie2', TextField(_('Vector')))
        form = NewBoxesForm(next=request.args.get('next'))
        return render_template('admin/create_boxes.html', form=form)

    return render_template('admin/create_boxes.html', form=form)

@admin.route('/boxes')
@login_required
@admin_required
def boxes():
    users = User.query.all()
    boxes = Box.query.all()
    return render_template('admin/boxes.html', users=users, boxes=boxes, active='boxes')

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', users=users, active='users')

@admin.route('/farms')
@login_required
@admin_required
def farms():
    farms = Farm.query.all()
    return render_template('admin/farms.html', farms=farms, active='farms')

@admin.route('/numbers')
@login_required
@admin_required
def numbers():
    numbers = WeeklyNumbers.query.all()
    return render_template('admin/numbers.html', numbers=numbers, active='numbers')

@admin.route('/farms/signup', methods=['GET', 'POST'])
@login_required
@admin_required
def farm_signup():
    form = NewFarmForm(next=request.args.get('next'))

    if form.validate_on_submit():
        farm = form.save()

        return redirect(form.next.data or url_for('admin.farms'))

    return render_template('admin/farm_signup.html', form=form)

@admin.route('/user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def user(user_id):
    user = User.query.filter_by(id=user_id).first_or_404()
    form = UserForm(obj=user, next=request.args.get('next'))

    if form.validate_on_submit():
        form.save(user)

        flash('User updated.', 'success')

    return render_template('admin/user.html', user=user, form=form)


@admin.route('/translation/edit/<language>', methods=['POST', 'GET'])
@login_required
@admin_required
def edit_translation(language):
    form = EditTranslationForm(language=language)
    if form.validate_on_submit():
        file = request.files[form.file.name]
        if file:
            file.save(os.path.join(current_app.config['TRANSLATIONS_FOLDER'], language,
                current_app.config['TRANSLATIONS_PATH'], current_app.config['TRANSALTIONS_FILE']))
            os.system("pybabel compile -f -d uru_crm/translations")
            flash("Translation File has been uploaded")
            return redirect(url_for('admin.edit_translation', language=language))
    return render_template('admin/translation.html', form=form)


@admin.route('/translations', methods=['GET'])
@login_required
@admin_required
def translations():
    babel = Babel(current_app)
    languages = babel.list_translations()
    return render_template('admin/translations.html', languages=languages)


@admin.route('/translation/<language>', methods=['GET'])
@login_required
@admin_required
def existing_translation(language):
    return send_from_directory(os.path.join(current_app.config['TRANSLATIONS_FOLDER'], language,
        current_app.config['TRANSLATIONS_PATH']), current_app.config['TRANSALTIONS_FILE'])


@admin.route('/logo', methods=['POST'])
@login_required
@admin_required
def upload_logo():
    form = UploadLogoForm()
    if form.validate_on_submit():
        file = request.files[form.file.name]
        if file:
            file.save(current_app.config['LOGO_FILE'])
            flash("Logo File has been uploaded")
            return redirect(url_for('admin.index'))
