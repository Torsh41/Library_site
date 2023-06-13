from . import admin
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, jsonify
from ..begin_to_app import database
from app.models import User, Cataloge, Book, Item, Category, SearchResult
from .forms import AddCategoryForm
from app.decorators import admin_required
import copy


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
    users = User.query.all()
    if users:
        last_page = len(users) // RESULT_COUNT
        if len(users) % RESULT_COUNT > 0:
            last_page += 1
    
        username = str(request.form.get('users_search_result'))
        if username == 'все':
            user_pagination = User.query.paginate(last_page, per_page=RESULT_COUNT, error_out=False)
            if user_pagination.items:
                users = result_without_admin(user_pagination.items)
                return jsonify([dict(result=True, page=last_page, id=user.id, username=user.username) for user in users])
            else:
                return jsonify([dict(result=False)])
        else:
            user = User.query.filter(User.username.like("%{}%".format(username))).first()
            if user:
                users = result_without_admin([user])
                last_page = 1
                return jsonify([dict(result=True, page=last_page, id=user.id, username=user.username)])
            else:
                return jsonify([dict(result=False)])
    else:
        return jsonify([dict(result=False)])   
    
    
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
    form = AddCategoryForm()
    if form.validate_on_submit():
        category = Category(name=str(form.category_name.data).strip().lower())
        database.session.add(category)
        database.session.commit()
        categories = Category.query.all()
        last_page = len(categories) // RESULT_COUNT
        if len(categories) % RESULT_COUNT > 0:
            last_page += 1 
        return redirect(url_for('.admin_panel', username=username, category_page=last_page))#render_template('admin/admin_panel.html', categories=categories, form=form, category_pagination=category_pagination, displays={"users_search_result_disp":"none", "book_categories_disp":"block", "add_category_disp":"none", "books_in_a_category_disp":"none"})
    
    category_page = request.args.get('category_page', 1, type=int)
    category_pagination = Category.query.paginate(category_page, per_page=RESULT_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('admin/admin_panel.html', categories=categories, form=form, category_pagination=category_pagination, displays={"users_search_result_disp":"none", "book_categories_disp":"block", "add_category_disp":"block", "books_in_a_category_disp":"none"})


@admin.route('/admin_panel/user_delete/<user_id>/<page>', methods=['GET'])
@admin_required
def user_delete(user_id, page):
    page = int(page)
    user = User.query.filter_by(id=user_id).first()
    database.session.delete(user)
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
    category = Category.query.filter_by(id=category_id).first()
    database.session.delete(category)
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


@admin.route('/<username>/search_books_on_admin_panel/<category>', methods=['GET', 'POST'])
@admin_required
def search_books_on_admin_panel(username, category):
    category = Category.query.filter_by(name=category).first()
    if request.method == "POST":
        result = str(request.form.get('search_result')).strip().lower()
        if result == "все":
            books = category.books.all()
        else:
            books = category.books.filter(Book.name.like("%{}%".format(result))).all()
            books_ = category.books.filter(Book.author.like("%{}%".format(result))).all()
            books = books + books_
        search_result_fin = [] 
        [search_result_fin.append(value) for value in books if value not in search_result_fin]
        fin_result = list()
        for each in search_result_fin:
            if each:
                fin_result.append(each)
        books = fin_result
        if books:
            pages = len(books) // RESULT_COUNT
            if len(books) % RESULT_COUNT > 0:
                pages += 1
            books_grades = list() 
            old_books_result = SearchResult.query.all()
            if old_books_result:
                for elem in old_books_result:
                    database.session.delete(elem)
            for book in books:
                book_for_cur_result = SearchResult(book)
                database.session.add(book_for_cur_result)
                grades = book.grades.all()
                try:
                    books_grades.append(round(sum([value.grade for value in grades]) / len(grades), 1))
                except:
                    books_grades.append(None)
            database.session.commit()
            books = books[:RESULT_COUNT] 
            return jsonify([dict(has_books=True, pages=pages, id=book.id, name=book.name, author=book.author, release_date=book.release_date, grade=book_grade) for book, book_grade in zip(books, books_grades)])
        else:
            return jsonify([dict(has_books=False)])
              
    elif page := request.args.get('page', None, type=int):
        cur_result_for_pagi = SearchResult.query.all()
        page_count = 1; temp_arr = list(); books = dict(); counter = 0
        for book in cur_result_for_pagi:
            counter += 1
            temp_arr.append(book)
            if counter % RESULT_COUNT == 0:
                books[page_count] = copy.copy(temp_arr)
                page_count += 1
                temp_arr = list()
                
        if counter % RESULT_COUNT > 0:
            books[page_count] = temp_arr
        books_grades = list()
        for book in books[page]:
            grades = book.grades.all()
            try:
                books_grades.append(round(sum([value.grade for value in grades]) / len(grades), 1))
            except:
                books_grades.append(None)
        return jsonify([dict(id=book.id, name=book.name, author=book.author, release_date=book.release_date, grade=book_grade) for book, book_grade in zip(books[page], books_grades)])
    
    return render_template('500.html')
            
        
    
    

