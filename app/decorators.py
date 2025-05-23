from flask import abort, session, redirect, url_for
from flask_login import login_required, current_user, logout_user
from app.models import Role, User, Book, ModerationRequest
from functools import wraps
from . import database


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


def admin_required(func):
    @wraps(func)
    @login_required
    @check_actual_password
    def decorated_func(*args, **kwargs):
        if current_user.role == Role.ADMIN:
            return func(*args, **kwargs)
        else:
            abort(403)
    return decorated_func


def moderator_required(func):
    @wraps(func)
    @login_required
    @check_actual_password
    def decorated_func(*args, **kwargs):
        if current_user.role == Role.ADMIN or current_user.role == Role.MODERATOR:
            return func(*args, **kwargs)
        else:
            abort(403)
    return decorated_func


def book_passed_moderation(book: Book) -> bool:
    """Check if a user has permission to access to the book.
    Specifically, check if the book has not passed moderation, or if
    current_user is not a Moderator or an Admin.
    """
    if book is None:
        return False
    if book.moderation_request.status == ModerationRequest.STATUS_ACCEPTED:
        return True
    if (current_user.is_authenticated and
        (current_user.role == Role.MODERATOR or
         current_user.role == Role.ADMIN)):
        return True
    return False


