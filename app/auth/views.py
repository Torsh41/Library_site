from flask import render_template, redirect, request, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..begin_to_app import database
from ..models import User
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, ConfirmEmailToChangePasswordForm
from app.email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)  # , form.remember_me.data)
            return redirect(url_for('personal.person', username=current_user.username))

        # неправильная почта или пароль
    return render_template('auth/authorization.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    # выход был осуществлен
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        database.session.delete(user)
        database.session.commit()
        logout_user()

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data.strip().replace("'", ""), email=form.email.data.strip().lower(),
                    password=form.password.data)
        user.default_ava()
        user.check_admin()
        database.session.add(user)
        database.session.commit()
        login_user(user)
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        # письмо с подтверждением было выслано на ваш аккаунт
        return redirect(url_for('main.index'))
    return render_template('auth/registraton.html', form=form)


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        database.session.commit()
        # вы подтвердили аккаунт
    # ссылка подтверждения не верна либо просрочена
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account',
               'auth/email/confirm', user=current_user, token=token)
    # новое письмо с подтверждением было выслано на ваш аккаунт
    return redirect(url_for('main.index'))


@auth.route('/password-change', methods=['GET', 'POST'])
def change_password_try():
    form = ConfirmEmailToChangePasswordForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user:
            token = user.generate_change_token()
            send_email(user.email, 'Change Your Password',
                       'auth/email/change_password',
                       user=user, token=token)
            return redirect(url_for('auth.login'))
    return render_template('auth/change_password_try.html', form=form)


@auth.route('/password-change/<token>', methods=['GET', 'POST'])
def change_password(token):
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if User.change_password(token, form.password.data):
            database.session.commit()
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/change_password.html', form=form)