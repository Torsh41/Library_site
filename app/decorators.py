from flask import abort, session, redirect, url_for
from flask_login import login_required, current_user, logout_user
from app.models import Role, User
from functools import wraps


def admin_required(func):
    @wraps(func)
    @login_required
    def decorated_func(*args, **kwargs):
        if current_user.role == Role.ADMIN:
            return func(*args, **kwargs)
        else:
            abort(403)
    return decorated_func


def check_actual_password(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        user = User.query.filter_by(username=session.get('username')).first()
        if user:
            if user.password_hash != session.get('password_hash'):
                logout_user()
                session.pop('username', None)
                session.pop('password_hash', None)
                return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return decorated_func



        