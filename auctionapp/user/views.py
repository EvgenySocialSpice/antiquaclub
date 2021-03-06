from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_user, logout_user
from auctionapp.user.forms import LoginForm, RegistrationForm
from auctionapp.db import db
from auctionapp.user.models import User
from auctionapp.utils import get_redirect_target
from auctionapp.site_func import get_categories_cache

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route('/login')
def login():
    title = 'Авторизация'
    login_form = LoginForm()
    categories = get_categories_cache()
    return render_template('user/login.html', page_title=title, form=login_form, categories=categories)


@blueprint.route('/process-login', methods=['POST'])
def process_login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash('Вы успешно вошли на сайт')
            return redirect(get_redirect_target())
    flash('Неправильные имя пользователя или пароль')
    return redirect(url_for('user.login'))


@blueprint.route('/logout')
def logout():
    logout_user()
    flash('Вы успешно разлогинились')
    return redirect(url_for('site.index'))


@blueprint.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('site.index'))
    title = "Регистрация"
    form = RegistrationForm()
    categories = get_categories_cache()
    return render_template('user/registration.html', page_title=title, categories=categories, form=form)


@blueprint.route('/process-reg', methods=['POST'])
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(name=form.name.data,
                        last_name=form.last_name.data,
                        nickname=form.nickname.data,
                        email=form.email.data,
                        phone=form.phone.data,
                        birth_date=form.birth_date.data,
                        reg_datetime=datetime.now(),
                        role_user='user',
                        phone_confirmed=True,
                        email_confirmed=True,
                        )
        new_user.set_password(form.password.data)
        # print(new_user)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
                print("Ошибка в поле {}: {}".format(getattr(form, field).label.text, error))
        return redirect(url_for('user.register'))
