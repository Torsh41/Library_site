from . import personal
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, make_response, jsonify
from .forms import EditProfileForm, AddListForm, AddNewBookForm
from ..begin_to_app import database
from app.models import User, Cataloge, Book, Item, Category, Role
import copy
LISTS_COUNT = 2
BOOKS_COUNT = 5


@personal.app_context_processor
def inject_roles():
    return dict(Role=Role)


@personal.route('/<username>/edit-profile/edit-avatar')
def avatar(username):
    user = User.query.filter_by(username=username).first()
    avatar = make_response(user.avatar)
    return avatar
    
    
@personal.route('/<username>')
@login_required
def person(username, flag=False):
    form = AddListForm()
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
    catalogues = pagination.items
    paginations_for_books_in_lists = list()
    for cataloge in catalogues:
        books_pagination = cataloge.items.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
        paginations_for_books_in_lists.append(books_pagination)
        
    return render_template('personal/user_page.html', user=user, catalogues=catalogues, pagination=pagination, paginations_for_books_in_lists=paginations_for_books_in_lists, len=len, flag=flag, form=form, zip=zip, display="none")


@personal.route('/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
def edit(username):
    form = EditProfileForm()
    if form.validate_on_submit():  
        if request.files['avatar']:
            current_user.avatar = bytes(request.files['avatar'].read())
        current_user.city = form.city.data
        current_user.gender = str(request.form.get('gender'))
        current_user.age = form.age.data
        current_user.about_me = form.description.data
        database.session.add(current_user._get_current_object())
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('personal/edit_user_page_profile.html', form=form)


@personal.route('/<username>/add-list', methods=['POST'])
@login_required
def add_list(username):
    form = AddListForm()
    if form.validate_on_submit():
        cataloge = Cataloge(name=str(form.list_name.data).strip().lower(), user=current_user._get_current_object())
        database.session.add(cataloge)
        database.session.commit()
        user = User.query.filter_by(username=username).first()
        user_cataloges = user.cataloges.all()
        page = int(len(user_cataloges) / LISTS_COUNT)
        if len(user_cataloges) % LISTS_COUNT > 0:
            page += 1
        return redirect(url_for('.person', username=username, page=page))
    categories = Category.query.all()
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
    catalogues = pagination.items
    return render_template('personal/user_page.html', user=user, catalogues=catalogues, pagination=pagination, categories=categories, len=len, form=form, zip=zip, display="block")


@personal.route('/<username>/get_lists_page/<page>', methods=['GET'])
@login_required
def get_lists_page(username, page):
    page = int(page)
    user = User.query.filter_by(username=username).first()
    pagination = user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
    cataloges = pagination.items
    cataloges_items = dict()
    for cataloge in cataloges:
        items_pagination = cataloge.items.order_by().paginate(1, per_page=BOOKS_COUNT, error_out=False)
        cataloge_items = [dict(id=item.id, read_state=item.read_state, name=item.book.name, cur_page=1, pages=items_pagination.pages) for item in items_pagination.items]
        cataloges_items[cataloge.id] = copy.deepcopy(cataloge_items)
        
    return jsonify([dict(cur_page=pagination.page, pages=pagination.pages, id=cataloge.id, name=cataloge.name, items=items, username=user.username) for cataloge, items in zip(cataloges, cataloges_items.values())])
    

@personal.route('/<username>/get_books_page/<cataloge_id>/<page>', methods=['GET'])
@login_required
def get_books_page(username, cataloge_id, page):
    page = int(page)
    cataloge = Cataloge.query.filter_by(id=cataloge_id).first()
    items_pagination = cataloge.items.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
    items = items_pagination.items
    return jsonify([dict(id=item.id, name=item.book.name, read_state=item.read_state, username_of_cur_user=username) for item in items])
    
    
@personal.route('/<username>/add-new-book', methods=['GET', 'POST'])
@login_required
def add_new_book(username):
    categories = Category.query.all()
    form = AddNewBookForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(name=str(request.form.get('category'))).first()
        book = Book(cover=bytes(request.files['cover'].read()), isbn=form.isbn.data, name=str(form.name.data).strip().lower(), author=str(form.author.data).strip().lower(), publishing_house=str(form.publishing_house.data).strip(), \
                    description=form.description.data, release_date=form.release_date.data, count_of_chapters=form.chapters_count.data, \
                    category=category, user=current_user._get_current_object())
        
        if not book.cover:
            book.default_cover()
            
        database.session.add(book)
        database.session.commit()
        return redirect(url_for('.person', username=username, flag=True))
    return render_template('personal/add_book.html', form=form, categories=categories, range=range, len=len)


@personal.route('/<username>/add-book-in-list/<book_id>', methods=['GET', 'POST'])
@login_required
def add_book_in_list_tmp(username, book_id):
    list_id = request.args.get('list_id', None, type=int)
    if request.form:
        read_state = request.form.get('read_state')
    else:
        read_state = "Читаю"
    user = User.query.filter_by(username=username).first()
    if list_id:
        return redirect(url_for('.add_book_in_list', username=username, list_id=list_id, book_id=book_id, read_state=read_state))
    
    catalogues = Cataloge.query.filter_by(user_id=user.id).all()
    return render_template('personal/user_page_add_book.html', username=username, book_id=book_id, catalogues=catalogues, read_state=read_state)


@personal.route('/<username>/add-book-in-list/<list_id>/<book_id>/<read_state>', methods=['GET', 'POST'])
@login_required
def add_book_in_list(username, list_id, book_id, read_state):
    cataloge = Cataloge.query.filter_by(id=list_id).first()
    book = Book.query.filter_by(id=book_id).first()
    flag = False
    if cataloge:
        for item_ in cataloge.items:
            if book.name == item_.book.name:
                item_for_replace = item_
                flag = True
                break
                
    if flag: 
        database.session.delete(item_for_replace)
        database.session.commit()
       
    item = Item(read_state=str(read_state), book=book, cataloge=cataloge)     
    database.session.add(item)
    database.session.commit()
    return redirect(url_for('.person', username=username))


@personal.route('/<username>/delete-list/<list_id>/<page>', methods=['GET'])
@login_required
def list_delete(username, list_id, page):
    page = int(page)
    user = User.query.filter_by(username=username).first()
    cataloge = Cataloge.query.filter_by(id=list_id).first()
    database.session.delete(cataloge)
    database.session.commit()
    if cataloges := user.cataloges.all():
        has_elems = True
        cataloge_pagination = user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
        pages = cataloge_pagination.pages
        if not cataloge_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, username=username))


@personal.route('/<username>/delete-item/<cataloge_id>/<item_id>/<page>', methods=['GET'])
@login_required
def item_delete(username, cataloge_id, item_id, page):
    page = int(page)
    cataloge = Cataloge.query.filter_by(id=cataloge_id).first()
    item = Item.query.filter_by(id=item_id).first()
    database.session.delete(item)
    database.session.commit()
    if cataloge.items.all(): 
        has_elems = True
        items_pagination = cataloge.items.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
        pages = items_pagination.pages
        if not items_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, username=username))