from . import moderation
from flask_login import current_user
from flask import render_template, redirect, abort, url_for, request, jsonify
from .. import database
from app.models import User, Role, Book, Category, SearchResult
from .forms import BookSearchFiltersForm, SetModerationStatusForm
from app.decorators import *
from datetime import datetime


PAGINATION_PER_PAGE = 10


@moderation.route('/book/search/<int:page>', methods=['GET', 'POST'])
@moderator_required
def book_search_pagination(page):
    from app import app
    # import flask
    app.logger.info("Page: %s", page)
    category_list = database.session.execute(
            database.select(Category).order_by(Category.name)
    ).scalars().all()
    category_select_list = [(cy.id, cy.name) for cy in category_list]
    form = BookSearchFiltersForm(category_list=category_select_list)
    query = database.select(Book)
    if form.validate_on_submit():
        if form.category.data:
            query = query.filter(Book.category_id==int(form.category.data))
        if form.bookname.data:
            query = query.filter(Book.name.like(f"%{form.bookname.data}%"))
        if form.username.data:
            query = query.join(Book.user)
            query = query.filter(User.username.like(f"%{form.username.data}%"))
        if form.status.data:
            query = query.join(Book.moderation_request)
            query = query.filter(ModerationRequest._status==int(form.status.data))
    query = query.order_by(Book.timestamp)
    app.logger.info("Page: %s", page)
    pagintaion = database.paginate(query, page=page, per_page=PAGINATION_PER_PAGE)
    app.logger.info("Page: %s", page)
    book_list = pagintaion.items
    return render_template(
        'moderation/moderation_panel.html',
        category_select_list=category_select_list,
        book_list=book_list,
        pagination=pagintaion,
        form=form,
        status_form=SetModerationStatusForm()
    )


@moderation.route('/book/search', methods=['GET', 'POST'])
@moderator_required
def book_search():
    return book_search_pagination(1)


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


