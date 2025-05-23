from . import moderation
from flask_login import current_user
from flask import render_template, redirect, abort, url_for, request, jsonify
from .. import database
from app.models import User, Role, Book, Category, SearchResult
from .forms import BookSearchFiltersForm, SetModerationStatusForm
from app.decorators import *
from datetime import datetime


### TODO: Get list of books all books, with filters, pagination



@moderation.route('/book/search', methods=['GET', 'POST'])
@moderator_required
def book_search():
    category_list = database.session.execute(
            database.select(Category).order_by(Category.name)
    ).scalars().all()
    category_select_list = [(cy.id, cy.name) for cy in category_list]
    # TODO: add an "all category" choice
    form = BookSearchFiltersForm(category_list=category_select_list)



    # return "{}".format(form.status.data)
    # TODO: dynamicly set form.category.choices
    query = database.select(Book)
    from app import app
    app.logger.info("New Query")
    app.logger.info("form.category.data: '%s'", form.category.data)
    app.logger.info("form.bookname.data: '%s'", form.bookname.data)
    app.logger.info("form.status.data: '%s'", form.status.data)
    app.logger.info("form.username.data: '%s'", form.username.data)
    app.logger.info("%s", ModerationRequest.__dict__)
    if form.validate_on_submit():
        if form.category.data:
            query = query.filter(Book.category_id==int(form.category.data))
            app.logger.info("Filtering by category")
        if form.bookname.data:
            query = query.filter(Book.name.like(f"%{form.bookname.data}%"))
            app.logger.info("Filtering by bookname")
        if form.username.data:
            query = query.join(Book.user)
            query = query.filter(User.username.like(f"%{form.username.data}%"))
            app.logger.info("Filtering by usename")
        if form.status.data:
            query = query.join(Book.moderation_request)
            query = query.filter(ModerationRequest._status==int(form.status.data))
            app.logger.info("Filtering by moderation status")
            # (Book.author.like("%{}%".format(result)))
    query = query.order_by(Book.timestamp)
    book_list = database.session.execute(query).scalars().all()
    RESULT_COUNT=5
    # form = AddCategoryForm()
    category_page = request.args.get('category_page', None, type=int)
    if not category_page:
        category_page = 1
    category_pagination = (Category.query
                            .paginate(category_page,
                                      per_page=RESULT_COUNT,
                                      error_out=False))
    categories = category_pagination.items
    return render_template(
        'moderation/moderation_panel.html',
        category_select_list=category_select_list,
        book_list=book_list,
        # category_pagination=category_pagination,
        form=form,
        status_form=SetModerationStatusForm()
    )


@moderation.route('/book/searchh', methods=['GET'])
@moderator_required
def book_searchh():
    # ret = {"result": False}
    ret = [{"result": False}]
    users = User.query.all()
    search_string = str(request.form.get('users_search_result'))
    if users is None or search_string == "":
        return ret
    result = False
    pages_count = None
    last_page = None
    if '*' in search_string:
        last_page = (len(users) - 1) // USERS_COUNT
        if len(users) % USERS_COUNT > 0:
            last_page += 1
        user_pagination = (User.query
                            .filter(User.username != current_user.username)
                            .paginate(1, per_page=USERS_COUNT, error_out=False))
        if user_pagination.items:
            users = user_pagination.items
            result = True
            pages_count = list(user_pagination.iter_pages())
            last_page = last_page
    elif '@' in search_string:
        at_symbol = search_string.find('@')
        users = User.query.filter(
                (User.username != current_user.username) &
                (User.email.like("%{}%@%{}%".format(search_string[:at_symbol], search_string[at_symbol + 1:])))
        ).first()
        if users:
            users = [users]
            result = True
            last_page = 1
            pages_count = [1]
    else:
        users = User.query.filter(
                (User.username != current_user.username) &
                (User.username.like("%{}%".format(search_string)))
        ).first()
        if users:
            users = [users]
            result = True
            last_page = 1
            pages_count = [1]
    if result:
        ret = [{
            "result": result,
            "cur_page": 1,
            "pages_count": pages_count,
            "page": last_page,
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        } for user in users]
    return jsonify(ret)





    category = Category.query.filter_by(id=id).first()
    if category is None:
        return abort(400)
    res = database.session.execute(
            database.select(Book)
                    .join(Book.category)
                    .filter_by(id=category.id)
                    .join(Book.moderation_request)
                    .filter_by(status=ModerationRequest.STATUS_ACCEPTED)
           .order_by(Book.id)
    ).scalars().all()
    result = str(request.form.get('search_result')).strip().lower()
    if result == '*':
        search_result = res
    else:
        search_result = list()
        release_date = request.form.get('release_date').strip()
        description = request.form.get('description').strip()
        if result:
            search_result += category.books.filter(
                (Book.name.like("%{}%".format(result))) |
                (Book.author.like("%{}%".format(result)))
            ).all()
        if release_date:
            search_result += category.books.filter_by(release_date=release_date).all()
        if description:
            search_result += category.books.filter(
                (Book.description.like("%{}%".format(description)))
            ).all()
        
        search_result = sorted(search_result, key=lambda value: value.id)
            
    if search_result:
        search_result = list(set(search_result))
        results_count = len(search_result)
        pages_count = len(search_result) // ELEMS_COUNT
        if len(search_result) % ELEMS_COUNT > 0:
            pages_count += 1
        
        books = list(); res = dict()
        for book in search_result:
            if book_grades := book.grades.all():
                book_grade = round(sum([value.grade for value in book_grades]) / len(book_grades), 1)
            else:
                book_grade = 0
            books.append(dict(
                result=True,
                id=book.id,
                name=book.name,
                grade=book_grade,
                category_id=category.id,
                current_user_is_auth=current_user_is_auth,
                username=username,
                author=book.author,
                pages_count=pages_count,
                results_count=results_count
            ))
        for page in range(1, pages_count + 1):
            res[page] = books[(page - 1) * ELEMS_COUNT: page * ELEMS_COUNT]
            
        return jsonify(dict(result=True, data=res))
    return jsonify(dict(result=False))


@moderation.route('/book/set_moderation_status', methods=['POST'])
@moderator_required
def set_moderation_status():
    form = SetModerationStatusForm(request.form)
    if form.validate_on_submit():
        book = database.session.execute(
                database.select(Book).filter_by(id=form.book_id.data)
        ).scalar_one_or_none()
        if book is None:
            form.errors["book_id"] = "Такой книги не существует..."
            return jsonify({
                "result": False,
                "errors": form.errors
            }), 200
        book.moderation_request.comment = form.comment.data.strip()
        book.moderation_request.status = int(form.status.data)
        book.moderation_request.timestamp = datetime.now()
        database.session.add(book.moderation_request)
        database.session.commit()
        return jsonify({"result": True}), 200
    return jsonify({
        "result": False,
        "errors": form.errors
    }), 200


