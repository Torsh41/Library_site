from . import common
from .forms import BookSearchForm
from app import database
from app.models import *
from flask import render_template, request, redirect, abort, url_for, make_response, jsonify
from flask_login import current_user, login_required
from app.decorators import *
import datetime


@common.route('/book/search/', methods=['POST'])
def book_search_filters():
    PAGINATION_PER_PAGE = 12
    form = BookSearchForm(request.form)
    page = form.page.data if form.page.data else 1
    extended = form.extended.data if form.extended.data else True

    # NOTE: not fully tested, errors might occur
    query = database.select(Book)
    if form.validate_on_submit():
        app.logger.info("VALIDATED_ON_SUBMIT")
        if form.category.data:
            query = query.filter(Book.category_id==int(form.category.data))
        if form.bookname.data:
            query = query.filter(Book.name.like(f"%{form.bookname.data.strip()}%"))
        if form.author.data:
            query = query.filter(Book.name.like(f"%{form.author.data.strip()}%"))
        if form.publishing_house.data:
            query = query.filter(Book.name.like(f"%{form.publishing_house.data.strip()}%"))
        if form.release_year_min.data:
            date_min = datetime.date(int(form.release_year_min.data), 1, 1)
            query = query.filter(Book.release_date >= date_min)
        if form.release_year_max.data:
            date_max = datetime.date(int(form.release_year_max.data), 1, 1)
            query = query.filter(Book.release_date < date_max)
        if form.description.data:
            query = query.filter(Book.name.like(f"%{form.description.data.strip()}%"))
        if form.username.data:
            query = query.join(Book.user)
            query = query.filter(User.username.like(f"%{form.username.data.strip()}%"))
        if form.status.data:
            @moderator_required
            def filter_moderation_status(query):
                query = query.join(Book.moderation_request)
                query = query.filter(ModerationRequest._status==int(form.status.data))
                return query
            query = filter_moderation_status(query)
    else:
        app.logger.info("ERROR VALIDATE ON SUBMIT")
        app.logger.info(form.errors)
        return jsonify({ "result": False } | form.errors), 200

    query = query.order_by(Book.timestamp)
    pagination = database.paginate(query, page=page, per_page=PAGINATION_PER_PAGE)
    book_list = []
    for book in pagination.items:
        grade_list = [0] + [grade.grade for grade in book.grades.all()]
        grade_avg = sum(grade_list) / len(grade_list)
        book_info = {
            "id": book.id,
            "name": book.name,
            "author": book.author,
            "release_year": book.release_year,
            "moderation_status": book.moderation_request.status_str(),
            "category": book.category.name,
            "grade_avg": grade_avg,
        }
        # Add extended info
        if extended:
            book_info |= {
                "isbn": book.isbn,
                "reference_url": book.reference_url,
                "publishing_house": book.publishing_house,
                "upload_datetime": book.timestamp.isoformat(),
                "description": book.description,
                "count_of_chapters": book.count_of_chapters,
                "moderation_comment": book.moderation_request.comment,
                "username": book.user.username,
            }
        book_list.append(book_info)
    return jsonify({
        "result": True,
        "book_list": book_list,
        "pagination": {
            "page": pagination.page,
            "per_page": pagination.per_page,
            "page_list": list(pagination.iter_pages()),
        },
        "current_user": {
            "is_authenticated": current_user.is_authenticated,
            "username": current_user.username if current_user.is_authenticated else None,
        },
    }), 200


