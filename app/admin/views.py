from . import admin
from flask_login import current_user
from flask import render_template, redirect, url_for, request, jsonify
from .. import database
from app.models import User, Book, Category, SearchResult
from .forms import AddCategoryForm
from app.decorators import admin_required, check_actual_password
import copy
RESULT_COUNT = 8


@admin.route('/<username>/admin_panel', methods=['GET', 'POST'])
@admin_required
@check_actual_password
def admin_panel(username):
    form = AddCategoryForm()
    category_page = request.args.get('category_page', None, type=int)
    if not category_page:
        category_pagination = Category.query.paginate(
            1, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
        return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, form=form, displays={"users_search_result_disp": "none", "book_categories_disp": "none", "add_category_disp": "none", "books_in_a_category_disp": "none"})
    else:
        category_pagination = Category.query.paginate(
            category_page, per_page=RESULT_COUNT, error_out=False)
        categories = category_pagination.items
        return render_template('admin/admin_panel.html', categories=categories, category_pagination=category_pagination, form=form, displays={"users_search_result_disp": "none", "book_categories_disp": "block", "add_category_disp": "none", "books_in_a_category_disp": "none"})


@admin.route('/<username>/admin_panel/user_search', methods=['POST'])
@admin_required
@check_actual_password
def user_search(username):
    users = User.query.all()
    if users:
        search_username = str(request.form.get('users_search_result'))
        if search_username == 'все':
            last_page = (len(users) - 1) // RESULT_COUNT
            if len(users) % RESULT_COUNT > 0:
                last_page += 1
            user_pagination = User.query.filter(User.username != current_user.username).paginate(1, per_page=RESULT_COUNT, error_out=False)
            if user_pagination.items:
                users = user_pagination.items
                pages_count = list(user_pagination.iter_pages())
                return jsonify([dict(result=True, cur_page=1, pages_count=pages_count, page=last_page, id=user.id, username=user.username) for user in users])
            else:
                return jsonify([dict(result=False)])
        else:
            user = User.query.filter((User.username != current_user.username) & (
                User.username.like("%{}%".format(search_username)))).first()
            if user:
                last_page = 1
                pages_count = [1]
                return jsonify([dict(result=True, cur_page=1, pages_count=pages_count, page=last_page, id=user.id, username=user.username)])
            else:
                return jsonify([dict(result=False)])
    else:
        return jsonify([dict(result=False)])


@admin.route('/get_user_search_page/<page>', methods=['GET'])
@admin_required
@check_actual_password
def get_user_search_page(page):
    page = int(page)
    user_pagination = User.query.filter(User.username != current_user.username).paginate(page, per_page=RESULT_COUNT, error_out=False)
    pages_count = list(user_pagination.iter_pages())
    users = user_pagination.items
    return jsonify([dict(cur_page=page, id=user.id, email=user.email, username=user.username, pages_count=pages_count, city=user.city, gender=user.gender, age=user.age, about_me=user.about_me) for user in users])


@admin.route('/<username>/get_category_search_page/<page>', methods=['GET'])
@admin_required
@check_actual_password
def get_category_search_page(username, page):
    page = int(page)
    category_pagination = Category.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
    pages_count = list(category_pagination.iter_pages())
    categories = category_pagination.items
    return jsonify([dict(username=current_user.username, cur_page=page, pages_count=pages_count, id=category.id, name=category.name) for category in categories])


@admin.route('/<username>/add-category', methods=['POST'])
@admin_required
@check_actual_password
def add_category(username):
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name=str(form.category_name.data).strip().lower().replace("'", ""))
        database.session.add(category)
        database.session.commit()
        categories = Category.query.all()
        last_page = len(categories) // RESULT_COUNT
        if len(categories) % RESULT_COUNT > 0:
            last_page += 1
        return redirect(url_for('.admin_panel', username=username, category_page=last_page))

    category_page = request.args.get('category_page', 1, type=int)
    category_pagination = Category.query.paginate(
        category_page, per_page=RESULT_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('admin/admin_panel.html', categories=categories, form=form, category_pagination=category_pagination, displays={"users_search_result_disp": "none", "book_categories_disp": "block", "add_category_disp": "block", "books_in_a_category_disp": "none"})


@admin.route('/admin_panel/user_delete/<user_id>/<page>', methods=['GET'])
@admin_required
@check_actual_password
def user_delete(user_id, page):
    page = int(page)
    user = User.query.filter((User.id != current_user.id)
                             & (User.id == user_id)).first()
    database.session.delete(user)
    database.session.commit()
    if users := User.query.filter(User.id != current_user.id).all():
        has_elems = True
        user_pagination = User.query.filter(User.id != current_user.id).paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages_count = list(user_pagination.iter_pages())
        if not user_pagination.items:
            page -= 1
    else:
        page = 1
        pages_count = 1
        has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems))


@admin.route('/<username>/category_delete/<category_id>/<page>', methods=['GET'])
@admin_required
@check_actual_password
def category_delete(username, category_id, page):
    page = int(page)
    category = Category.query.filter_by(id=category_id).first()
    database.session.delete(category)
    database.session.commit()
    if categories := Category.query.all():
        has_elems = True
        category_pagination = Category.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages_count = list(category_pagination.iter_pages())
        if not category_pagination.items:
            page = page - 1
    else:
        page = 1
        pages_count = 1
        has_elems = False
    return jsonify(dict(username=current_user.username, cur_page=page, pages_count=pages_count, has_elems=has_elems))


@admin.route('/<username>/search_books_on_admin_panel/<category_name>', methods=['GET', 'POST'])
@admin_required
@check_actual_password
def search_books_on_admin_panel(username, category_name):
    category = Category.query.filter_by(name=category_name).first()
    if request.method == "POST":
        result = str(request.form.get('search_result')).strip().lower()
        if result == "все":
            books = category.books.all()
        else:
            books = category.books.filter((Book.name.like("%{}%".format(result))) | (
                Book.author.like("%{}%".format(result)))).all()
        search_result_fin = []
        [search_result_fin.append(value) for value in books if value and value not in search_result_fin]
        books = search_result_fin
        if books:
            pages = len(books) // RESULT_COUNT
            if len(books) % RESULT_COUNT > 0:
                pages += 1
                
            # формируем список страниц с добавлением границ для правильного отображения их большого количества в пагинации
            if pages > RESULT_COUNT:
                pages_count = list()
                for p in range(1, pages + 1):
                    if p % 4 == 0:
                        pages_count.append(None)
                    else:
                        pages_count.append(p)
            else:
                pages_count = list(range(1, pages + 1))      
                             
            # удаление прошлых результатов поиска из бд
            database.session.query(SearchResult).delete()
            
            # old_books_result = SearchResult.query.all()
            # if old_books_result:
            #     for elem in old_books_result:
            #         database.session.delete(elem)
            
            books_grades = list()
            for book in books:
                book_for_cur_result = SearchResult(book)
                database.session.add(book_for_cur_result)
                grades = book.grades.all()
                try:
                    books_grades.append(round(sum([value.grade for value in grades]) / len(grades), 1))
                except:
                    books_grades.append(0)
            database.session.commit()
            if len(books) > RESULT_COUNT:
                books = books[:RESULT_COUNT]
            return jsonify([dict(has_books=True, pages=pages, cur_page=1, pages_count=pages_count, username=current_user.username, category=category.name, id=book.id, name=book.name, author=book.author, release_date=book.release_date, grade=book_grade) for book, book_grade in zip(books, books_grades)])
        else:
            return jsonify([dict(has_books=False)])

    elif page := request.args.get('page', None, type=int):
        cur_result_pagination = SearchResult.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages_count = list(cur_result_pagination.iter_pages())
        cur_result = cur_result_pagination.items
        #cur_result_for_pagi = SearchResult.query.all()
        if cur_result:
        # if cur_result_for_pagi:
        #     page_count = 1
        #     temp_arr = list()
        #     books = dict()
        #     counter = 0
        #     for book in cur_result_for_pagi:
        #         counter += 1
        #         temp_arr.append(book)
        #         if counter % RESULT_COUNT == 0:
        #             books[page_count] = copy.copy(temp_arr)
        #             page_count += 1
        #             temp_arr = list()

        #     if counter % RESULT_COUNT > 0:
        #         books[page_count] = temp_arr
            return jsonify([dict(has_books=True, cur_page=page, pages_count=pages_count, username=current_user.username, category=category.name, id=book.id, name=book.name, author=book.author, release_date=book.release_date, grade=book.grade) for book in cur_result])#books[page]])
        else:
            return jsonify([dict(has_books=False)])
    return render_template('500.html')


@admin.route('/<username>/del_book/<category_name>/<book_id>/<page>', methods=['GET'])
@admin_required
@check_actual_password
def del_book(username, category_name, book_id, page):
    page = int(page)
    book = Book.query.filter_by(id=book_id).first()
    database.session.delete(book)
    book_for_search_result = SearchResult.query.filter_by(id=book_id).first()
    database.session.delete(book_for_search_result)
    database.session.commit()
    if books := SearchResult.query.all():
        has_elems = True
        books_result_pagination = SearchResult.query.paginate(page, per_page=RESULT_COUNT, error_out=False)
        pages_count = list(books_result_pagination.iter_pages())
        if not books_result_pagination.items:
            page = page - 1
    else:
        page = 1
        pages_count = 1
        has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, username=current_user.username, category=category_name))
