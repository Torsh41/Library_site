from flask import abort
from flask_login import login_required, current_user
from app.models import Role
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



        