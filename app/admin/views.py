from . import admin
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request
from ..begin_to_app import database
from app.models import User, Cataloge, Book, Item, Category
from app.decorators import admin_required


RESULT_COUNT = 5
def result_without_admin(items):
    without_admin = list()
    for user in items:
        if user.username != current_user.username:
            without_admin.append(user)
    return without_admin


@admin.route('/<username>/admin_panel', methods=['GET', 'POST'])
@admin_required
def admin_panel(username):
    return render_template('admin/admin_panel.html', users_search_result_disp="none")


@admin.route('/<username>/admin_panel/user_search', methods=['GET', 'POST'])
@admin_required
def user_search(username):
    page = request.args.get('page', 1, type=int)
    if request.method == 'POST':
        username = str(request.form.get('users_search_result'))
        if username == 'все':
            pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
            users = result_without_admin(pagination.items)
        else:
            pagination = User.query.filter(User.username.like("%{}%".format(username))).paginate(page, per_page=RESULT_COUNT, error_out=False)
            users = result_without_admin(pagination.items)
    else:
        pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        users = result_without_admin(pagination.items)

    return render_template('admin/admin_panel.html', users=users, pagination=pagination, users_search_result_disp="block", len=len)


@admin.route('/<username>/admin_panel/user_delete/<user_id>')
def user_delete(username, user_id):
    User.query.filter_by(id=user_id).delete()
    database.session.commit()
    return redirect(url_for('.user_search', username=username))

