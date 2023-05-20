from . import admin
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, jsonify
from ..begin_to_app import database
from app.models import User, Cataloge, Book, Item, Category
from .forms import AddCategoryForm
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
    form = AddCategoryForm()
    category_page = request.args.get('category_page', None, type=int)
    page = request.args.get('page', None, type=int)
    if not category_page and not page:
        category_pagination = Category.query.paginate(1, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
       
    elif category_page:
        category_pagination = Category.query.paginate(category_page, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
        return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, form=form, displays={"users_search_result_disp":"none", "book_categories_disp":"block", "add_category_disp":"none", "books_in_a_category_disp":"none"})
    
    elif page:
        category_pagination = Category.query.paginate(1, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
        user_pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        users = result_without_admin(user_pagination.items)
        return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, users=users, user_pagination=user_pagination, form=form, displays={"users_search_result_disp":"block", "book_categories_disp":"none", "add_category_disp":"none", "books_in_a_category_disp":"none"})
    return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, form=form, displays={"users_search_result_disp":"none", "book_categories_disp":"none", "add_category_disp":"none", "books_in_a_category_disp":"none"})


@admin.route('/<username>/admin_panel/user_search', methods=['POST'])
@admin_required
def user_search(username):
    page = request.args.get('page', 1, type=int)
    username = str(request.form.get('users_search_result'))
    if username == 'все':
        user_pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        users = result_without_admin(user_pagination.items)
    else:
        user_pagination = User.query.filter(User.username.like("%{}%".format(username))).paginate(page, per_page=RESULT_COUNT, error_out=False)
        users = result_without_admin(user_pagination.items)
    
    form = AddCategoryForm()
    category_pagination = Category.query.paginate(1, per_page=RESULT_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, users=users, user_pagination=user_pagination, form=form, displays={"users_search_result_disp":"block", "book_categories_disp":"none", "add_category_disp":"none", "books_in_a_category_disp":"none"}, len=len)


@admin.route('/get_user_search_page/<page>', methods=['GET'])
@admin_required
def get_user_search_page(page):
    page = int(page)
    user_pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
    users = result_without_admin(user_pagination.items)
    return jsonify([dict(id=user.id, email=user.email, username=user.username, city=user.city, gender=user.gender, age=user.age, about_me=user.about_me) for user in users])
    
    
@admin.route('/get_category_search_page/<page>', methods=['GET'])   
@admin_required
def get_category_search_page(page):
    page = int(page)
    category_pagination = Category.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
    categories = category_pagination.items
    return jsonify([dict(id=category.id, name=category.name) for category in categories])
    
    
@admin.route('/<username>/add-category', methods=['POST'])
@admin_required
def add_category(username):
    category_page = request.args.get('category_page', 1, type=int)
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name=str(form.category_name.data).strip().lower())
        database.session.add(category)
        database.session.commit()
        category_pagination = Category.query.paginate(category_page, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
        return render_template('admin/admin_panel.html', categories=categories, form=form, category_pagination=category_pagination, displays={"users_search_result_disp":"none", "book_categories_disp":"block", "add_category_disp":"none", "books_in_a_category_disp":"none"})
    
    category_pagination = Category.query.paginate(category_page, per_page=RESULT_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('admin/admin_panel.html', categories=categories, form=form, category_pagination=category_pagination, displays={"users_search_result_disp":"none", "book_categories_disp":"block", "add_category_disp":"block", "books_in_a_category_disp":"none"})


@admin.route('/admin_panel/user_delete/<user_id>/<page>', methods=['GET'])
@admin_required
def user_delete(user_id, page):
    page = int(page)
    User.query.filter_by(id=user_id).delete()
    database.session.commit()
    if users := User.query.all():
        has_elems = True
        user_pagination = User.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages = user_pagination.pages
        if not user_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems))


@admin.route('/admin_panel/category_delete/<category_id>/<page>', methods=['GET'])
@admin_required
def category_delete(category_id, page):
    page = int(page)
    Category.query.filter_by(id=category_id).delete()
    database.session.commit()
    if categories := Category.query.all():
        has_elems = True
        category_pagination = Category.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages = category_pagination.pages
        if not category_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems))

