# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, flash
from flask.ext.login import login_required, current_user

from uru_crm.modules.user import User
from .forms import ProfileForm, PasswordForm


settings = Blueprint('settings', __name__, url_prefix='/settings')


@settings.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    form = ProfileForm(first_name=current_user.first_name,
            last_name=current_user.last_name,
            email=current_user.email,
            phone_num=current_user.phone_num,
            address=current_user.address,
            box_size=current_user.box_size,
            delivery_instructs=current_user.delivery_instructs,
            bad_veggies=current_user.bad_veggies,
            next=request.args.get('next'))

    if form.validate_on_submit():

        form.create_profile(request, user)

        flash('Public profile updated.', 'success')

    return render_template('settings/profile.html', user=user,
            active="profile", form=form)


@settings.route('/password', methods=['GET', 'POST'])
@login_required
def password():
    user = User.query.filter_by(name=current_user.name).first_or_404()
    form = PasswordForm(next=request.args.get('next'))

    if form.validate_on_submit():
        form.update_password(user)

        flash('Password updated.', 'success')

    return render_template('settings/password.html', user=user,
            active="password", form=form)
