from . import personal
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, make_response, jsonify
from .forms import EditProfileForm, AddNewBookForm
from .. import database
from app.models import User, Cataloge, Book, Item, Category, Role
from app.decorators import admin_required, check_actual_password
from app.parse_excel import add_many_books
from datetime import datetime
import copy
LISTS_COUNT = 2
BOOKS_COUNT = 5
CATEGORIES_COUNT = 5


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
@check_actual_password
def person(username, flag=False):
    if current_user.username != username:
        return render_template('403.html')
    page = request.args.get('page', 1, type=int)
    items_page = request.args.get('items_page', 1, type=int)
    cataloge_id = request.args.get('cataloge_id', None, type=int)
    cataloge_for_adding = None
    if cataloge_id:
        cataloge_for_adding = current_user.cataloges.filter_by(
            id=cataloge_id).first()

    pagination = current_user.cataloges.order_by().paginate(
        page, per_page=LISTS_COUNT, error_out=False)
    catalogues = pagination.items
    paginations_for_books_in_lists = list()
    cur_books_page_for_cataloges = list()
    for cataloge in catalogues:
        if cataloge == cataloge_for_adding:
            books_pagination = cataloge.items.order_by().paginate(
                items_page, per_page=BOOKS_COUNT, error_out=False)
            p = items_page
            if not books_pagination.items:
                books_pagination = cataloge.items.order_by().paginate(
                    1, per_page=BOOKS_COUNT, error_out=False)
                p = 1
        else:
            books_pagination = cataloge.items.order_by().paginate(
                1, per_page=BOOKS_COUNT, error_out=False)
            p = 1
        cur_books_page_for_cataloges.append(p)
        paginations_for_books_in_lists.append(books_pagination)
    return render_template('personal/user_page.html', user=current_user, catalogues=catalogues, pagination=pagination, paginations_for_books_in_lists=paginations_for_books_in_lists, cur_books_page_for_cataloges=cur_books_page_for_cataloges, cataloges_page=page, len=len, flag=flag, zip=zip, display="none")


@personal.route('/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
@check_actual_password
def edit(username):
    if current_user.username != username:
        return render_template('403.html')
    form = EditProfileForm()
    if form.validate_on_submit():
        if request.files['avatar']:
            current_user.avatar = bytes(request.files['avatar'].read())
        current_user.username = form.username.data.strip()
        current_user.city = form.city.data
        current_user.gender = str(request.form.get('gender'))
        current_user.age = form.age.data
        current_user.about_me = str(request.form.get('description')).strip()
        database.session.add(current_user._get_current_object())
        database.session.commit()
        return redirect(url_for('.person', username=current_user.username))
    return render_template('personal/edit_user_page_profile.html', form=form, city=current_user.city, gender=current_user.gender, age=current_user.age, about_me=current_user.about_me)


@personal.route('/<username>/add-list', methods=['POST'])
@login_required
@check_actual_password
def add_list(username):
    if current_user.username != username:
        return render_template('403.html')
    new_cataloge_name = str(request.form.get('newList')).strip().lower()
    user_cataloges = current_user.cataloges.all()
    result = 2
    for cataloge in user_cataloges:
        if new_cataloge_name == cataloge.name:
            result = 1
            break
    if len(current_user.cataloges.all()) > 5:
        result = 0

    if result == 2:
        cataloge = Cataloge(name=new_cataloge_name,
                            user=current_user._get_current_object())
        database.session.add(cataloge)
        database.session.commit()
        user_cataloges = current_user.cataloges.all()
        last_page = len(user_cataloges) // LISTS_COUNT
        if len(user_cataloges) % LISTS_COUNT > 0:
            last_page += 1

        cataloges_pagination = current_user.cataloges.order_by().paginate(last_page, per_page=LISTS_COUNT, error_out=False)
        pages_count = list(cataloges_pagination.iter_pages())
        cataloges = cataloges_pagination.items
        cataloges_items = dict()
        for cataloge in cataloges:
            items_pagination = cataloge.items.order_by().paginate(1, per_page=BOOKS_COUNT, error_out=False)
            cataloge_items = [dict(id=item.id, name=item.book.name, read_state=item.read_state, pages_count=list(items_pagination.iter_pages())) for item in items_pagination.items]
            cataloges_items[cataloge.id] = copy.deepcopy(cataloge_items)
        return jsonify([dict(result=result, last_page=last_page, pages_count=pages_count, id=cataloge.id, name=cataloge.name, items=items, username=username) for cataloge, items in zip(cataloges, cataloges_items.values())])
    else:
        return jsonify([dict(result=result)])


@personal.route('/<username>/get_lists_page/<page>', methods=['GET'])
@login_required
@check_actual_password
def get_lists_page(username, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    pagination = current_user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
    pages_count = list(pagination.iter_pages())
    cataloges = pagination.items
    cataloges_items = dict()
    for cataloge in cataloges:
        items_pagination = cataloge.items.order_by().paginate(1, per_page=BOOKS_COUNT, error_out=False)
        cataloge_items = [dict(id=item.id, read_state=item.read_state, name=item.book.name,
                               cur_page=1, pages_count=list(items_pagination.iter_pages())) for item in items_pagination.items]
        cataloges_items[cataloge.id] = copy.deepcopy(cataloge_items)
    return jsonify([dict(cur_page=pagination.page, pages_count=pages_count, id=cataloge.id, name=cataloge.name, items=items, username=current_user.username) for cataloge, items in zip(cataloges, cataloges_items.values())])


@personal.route('/<username>/get_books_page/<cataloge_id>/<page>', methods=['GET'])
@login_required
@check_actual_password
def get_books_page(username, cataloge_id, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    cataloge = Cataloge.query.filter_by(id=cataloge_id).first()
    if cataloge:
        items_pagination = cataloge.items.order_by().paginate(page, per_page=BOOKS_COUNT, error_out=False)
        pages_count = list(items_pagination.iter_pages())
        items = items_pagination.items
        return jsonify([dict(cur_page=page, pages_count=pages_count, id=item.id, name=item.book.name, read_state=item.read_state, username_of_cur_user=current_user.username) for item in items])
    return render_template("500.html")


@personal.route('/<username>/add-new-book', methods=['GET', 'POST'])
@login_required
@check_actual_password
def add_new_book(username):
    if current_user.username != username:
        return render_template('403.html')
    pagination = Category.query.paginate(
        1, per_page=CATEGORIES_COUNT, error_out=False)
    categories = pagination.items
    form = AddNewBookForm()
    if form.validate_on_submit():
        category = Category.query.filter_by(
            name=str(request.form.get('category'))).first()
        book = Book(cover=bytes(request.files['cover'].read()), isbn=form.isbn.data, name=str(form.name.data).strip().lower().replace("'", ""), author=str(form.author.data).strip().lower(), publishing_house=str(form.publishing_house.data).strip(),
                    description=form.description.data, release_date=form.release_date.data, count_of_chapters=form.chapters_count.data,
                    category=category, user=current_user._get_current_object())

        if not book.cover:
            book.default_cover()

        database.session.add(book)
        database.session.commit()
        return redirect(url_for('.person', username=current_user.username, flag=True))
    return render_template('personal/add_book.html', form=form, categories=categories, pagination=pagination, range=range, len=len)


@personal.route('/<username>/add-book-in-list-tmp/<book_id>', methods=['GET', 'POST'])
@login_required
@check_actual_password
def add_book_in_list_tmp(username, book_id):
    if current_user.username != username:
        return render_template('403.html')
    list_id = request.args.get('list_id', None, type=int)
    if request.form:
        read_state = request.form.get('read_state')
    else:
        read_state = "Читаю"
    if list_id:
        return redirect(url_for('.add_book_in_list', username=current_user.username, list_id=list_id, book_id=book_id, read_state=read_state))

    catalogues_pagination = current_user.cataloges.paginate(
        1, per_page=LISTS_COUNT, error_out=False)
    return render_template('personal/user_page_add_book.html', username=username, book_id=book_id, catalogues=catalogues_pagination.items, catalogues_pagination=catalogues_pagination, read_state=read_state)


@personal.route('/<username>/get_lists_page_to_add_book/<page>', methods=['GET'])
@login_required
@check_actual_password
def get_lists_page_to_add_book(username, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    cataloges_pagination = current_user.cataloges.paginate(page, per_page=LISTS_COUNT, error_out=False)
    return jsonify([dict(cur_page=page, id=cataloge.id, pages_count=list(cataloges_pagination.iter_pages()), name=cataloge.name, username=current_user.username) for cataloge in cataloges_pagination.items])


@personal.route('/<username>/add-book-in-list/<list_id>/<book_id>/<read_state>', methods=['GET', 'POST'])
@login_required
@check_actual_password
def add_book_in_list(username, list_id, book_id, read_state):
    if current_user.username != username:
        return render_template('403.html')
    cataloge_for_adding = current_user.cataloges.filter_by(id=list_id).first()
    book = Book.query.filter_by(id=book_id).first()
    flag = False
    page = 1
    if cataloge_for_adding and book:
        all_pages = current_user.cataloges.order_by().paginate(1, per_page=LISTS_COUNT, error_out=False).pages
        while page <= all_pages:
            pagination = current_user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
            cur_user_cataloges = pagination.items
            if cataloge_for_adding in cur_user_cataloges:
                break
            page += 1

        for item_ in cataloge_for_adding.items:
            if book.name == item_.book.name:
                item_for_replace = item_
                flag = True
                break
        if flag:
            database.session.delete(item_for_replace)
        item = Item(read_state=str(read_state), book=book,
                    cataloge=cataloge_for_adding)
        database.session.add(item)
        database.session.commit()
        all_cataloge_items = cataloge_for_adding.items.all()
        items_page = len(all_cataloge_items) // BOOKS_COUNT
        if len(all_cataloge_items) % BOOKS_COUNT > 0:
            items_page += 1

        return redirect(url_for('.person', username=current_user.username, page=page, items_page=items_page, cataloge_id=cataloge_for_adding.id))
    else:
        return render_template("500.html")


@personal.route('/<username>/delete-list/<list_id>/<page>', methods=['GET'])
@login_required
@check_actual_password
def list_delete(username, list_id, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    cataloge = current_user.cataloges.filter_by(id=list_id).first()
    database.session.delete(cataloge)
    database.session.commit()
    if cataloges := current_user.cataloges.all():
        has_elems = True
        cataloge_pagination = current_user.cataloges.order_by().paginate(page, per_page=LISTS_COUNT, error_out=False)
        pages_count = list(cataloge_pagination.iter_pages())
        if not cataloge_pagination.items:
            page = page - 1
    else:
        page = 1
        pages_count = [1]
        has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, username=current_user.username))


@personal.route('/<username>/delete-item/<cataloge_id>/<item_id>/<page>', methods=['GET'])
@login_required
@check_actual_password
def item_delete(username, cataloge_id, item_id, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    cataloge = current_user.cataloges.filter_by(id=cataloge_id).first()
    item = cataloge.items.filter_by(id=item_id).first()
    database.session.delete(item)
    database.session.commit()
    if cataloge.items.all():
        has_elems = True
        items_pagination = cataloge.items.order_by().paginate(page, per_page=BOOKS_COUNT, error_out=False)
        pages_count = list(items_pagination.iter_pages())
        if not items_pagination.items:
            page = page - 1
    else:
        page = 1
        pages_count = [1]
        has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, username=current_user.username))


@personal.route('/<username>/get_categories_page_for_book_adding/<page>', methods=['GET'])
@login_required
@check_actual_password
def get_categories_page_for_book_adding(username, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    categories_pagination = Category.query.paginate(page, per_page=CATEGORIES_COUNT, error_out=False)
    categories = categories_pagination.items
    pages_count = list(categories_pagination.iter_pages())
    return jsonify([dict(cur_page=page, pages_count=pages_count, username=current_user.username, id=category.id, name=category.name) for category in categories])


# изменение состояния чтения книги
@personal.route('/change_read_state/', methods=['POST'])
@login_required
@check_actual_password
def change_read_state():
    try:
        item = Item.query.filter_by(id=request.form.get('item_id')).first()
        item.read_state = str(request.form.get('read_state')).strip()
        database.session.add(item)
        database.session.commit()
        return jsonify(dict(read_state=item.read_state))
    except:
        return jsonify(dict(read_state=False))


# множественная загрузка книг
@personal.route('/add-books', methods=['POST'])
@admin_required
@check_actual_password
def add_new_books():
    file = request.files['data_file']
    if file.filename.split('.')[-1] != "xlsx":
        return jsonify(dict(result=False))
    
    data : list | bool = add_many_books(file)
    if not data:
        return jsonify(dict(result=False))
    
    count = 0
    for book in data:
        category = Category.query.filter_by(name=str(book[8])).first()
        if Book.query.filter_by(name=book[1]).first() or not category:
            continue
        try:
            datetime.strptime(book[6], "%d.%m.%Y")
        except:
            book[6] = datetime.today()
            
        book_obj = Book(cover=False, name=book[1], isbn=book[2], author=book[3], publishing_house=book[4], description=book[5], release_date=book[6], count_of_chapters=book[7], 
                        category=category, user=current_user._get_current_object())
        
        if not book_obj.cover:
            book_obj.default_cover()
            
        database.session.add(book_obj)
        count += 1
    database.session.commit()
    
    return jsonify(dict(result=True, count=count))
   
    