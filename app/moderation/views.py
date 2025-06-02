from . import moderation
from flask_login import current_user
from flask import render_template, redirect, abort, url_for, request, jsonify
from .. import database
from app.models import User, Role, Book, Category, SearchResult
from .forms import BookSearchFiltersForm, SetModerationStatusForm
from app.common.forms import BookSearchForm
from app.decorators import *
import datetime


# TODO: dynamically assign per_page parameter
# PAGINATION_PER_PAGE = 10


@moderation.route('/book/search', methods=['GET', 'POST'])
@moderator_required
def book_search():
    return render_template(
        'moderation/moderation_panel.html',
        form=BookSearchForm(),
        status_form=SetModerationStatusForm(),
        ModerationRequest=ModerationRequest
    )


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
        book.moderation_request.timestamp = datetime.datetime.now()
        database.session.add(book.moderation_request)
        database.session.commit()
        return jsonify({
            "result": True,
            "status_id": int(form.status.data),
            "status_name": ModerationRequest.status_dict[int(form.status.data)]
            }), 200
    return jsonify({
        "result": False,
        "errors": form.errors
    }), 200


