from . import main
from app.init import database
from app.models import BookGrade, Book, Comment, SearchResult, Category, User, TopicPost, DiscussionTopic, Role, BooksMaintaining
from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import current_user, login_required
from app.decorators import admin_required, check_actual_password
from app.parse_excel import *
import copy
from operator import itemgetter
from sqlalchemy.exc import IntegrityError
ELEMS_COUNT = 8
TOP_BOOKS_COUNT = 3
BOOKS_MAINTAINING_PER_PAGE = 20
months_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}


@main.app_context_processor
def inject_roles():
    return dict(Role=Role)


@main.app_context_processor
def inject_months_dict():
    return dict(months_dict=months_dict)


@main.route('/<name>/get-cover', methods=['GET'])
def cover(name):
    book = Book.query.filter_by(name=name).first()
    cover = make_response(book.cover)
    return cover


@main.route('/<post_id>/get-post_screenshot', methods=['GET'])
def post_screenshot(post_id):
    post = TopicPost.query.filter_by(id=post_id).first()
    file = make_response(post.file)
    return file


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/book-page/<name>', methods=['GET'])
def book_page(name):
    book = Book.query.filter_by(name=name).first()
    pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(
        1, per_page=ELEMS_COUNT, error_out=False)
    comments = pagination.items
    grades = book.grades.all()
    try:
        fin_grade = round(
            sum([value.grade for value in grades]) / len(grades), 1)
    except:
        fin_grade = 0
    return render_template('main/book_page.html', book=book, fin_grade=fin_grade, comments=comments, pagination=pagination, len=len, str=str, grade_count=len(grades), int=int, display="none")


@main.route('/get_comments_page/<book_name>/<page>', methods=['GET'])
def get_comments_page(book_name, page):
    page = int(page)
    book = Book.query.filter_by(name=book_name).first()
    comments = book.comments.order_by(Comment.timestamp.asc()).paginate(
        page, per_page=ELEMS_COUNT, error_out=False).items
    users = list()
    user_is_admin = True if (current_user.is_authenticated and current_user.role == Role.ADMIN) else False
    name_of_current_user = current_user.username if (current_user.is_authenticated) else None
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(cur_page=page, user_is_admin=user_is_admin, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_name=book_name, username=user.username, name_of_current_user=name_of_current_user, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])


@main.route('/<username>/<book_name>/add_comment', methods=['POST'])
@login_required
@check_actual_password
def add_comment(username, book_name):
    if current_user.username != username:
        return render_template('403.html')
    book = Book.query.filter_by(name=book_name).first()
    comment = Comment(body=str(request.form.get('comment')).strip().replace(
        "'", ""), book=book, user=current_user._get_current_object())
    database.session.add(comment)
    database.session.commit()
    comments = book.comments.all()
    last_page = len(comments) // ELEMS_COUNT
    id_of_added_comment = comments[-1].id
    if len(comments) % ELEMS_COUNT > 0:
        last_page += 1
    comments = book.comments.order_by(Comment.timestamp.asc()).paginate(last_page, per_page=ELEMS_COUNT, error_out=False).items
    user_is_admin = True if current_user.role == Role.ADMIN else False
    users = list()
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(pages=last_page, user_is_admin=user_is_admin, id_of_added_comment=id_of_added_comment, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_name=book_name, username=user.username, name_of_current_user=current_user.username, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])


@main.route('/<username>/<book_name>/edit-comment/<comment_id>', methods=['POST'])
@login_required
@check_actual_password
def edit_comment(username, comment_id, book_name):
    if current_user.username != username:
        return render_template('403.html')
    comment = Comment.query.filter_by(id=comment_id).first()
    comment.body = str(request.form.get('newComment')).strip().replace("'", "")
    database.session.add(comment)
    database.session.commit()
    return jsonify(dict(id=comment_id, body=comment.body, username=current_user.username, book_name=book_name))


@main.route('/<username>/give-grade/<book_id>/<grade>')
@login_required
@check_actual_password
def give_grade(username, book_id, grade):
    if current_user.username != username:
        return render_template('403.html')
    book = Book.query.filter_by(id=book_id).first()
    previous_grade = BookGrade.query.filter_by(
        user=current_user, book=book).first()
    if previous_grade:
        database.session.delete(previous_grade)

    grade = BookGrade(grade=grade, user=current_user, book=book)
    database.session.add(grade)
    database.session.commit()
    return redirect(url_for('main.book_page', name=book.name))


@main.route('/<username>/<book_name>/delete-comment/<comment_id>/<page>', methods=['GET'])
@login_required
@check_actual_password
def comment_delete(username, book_name, comment_id, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    book = Book.query.filter_by(name=book_name).first()
    comment = book.comments.filter_by(id=comment_id).first()
    database.session.delete(comment)
    database.session.commit()
    if book.comments.all():
        has_elems = True
        comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(
            page, per_page=ELEMS_COUNT, error_out=False)
        pages = comments_pagination.pages
        if not comments_pagination.items:
            page -= 1
    else:
        page = 1
        pages = 1
        has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, username=current_user.username, book_name=book_name))


@main.route('/categories', methods=['GET'])
def categories():
    list_id = request.args.get('list_id', None, type=int)
    category_pagination = Category.query.order_by().paginate(
        1, per_page=ELEMS_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('main/categories.html', categories=categories, category_pagination=category_pagination, list_id=list_id)


@main.route('/get_categories_page/<page>', methods=['GET'])
def get_categories_page(page):
    page = int(page)
    categories = Category.query.order_by().paginate(
        page, per_page=ELEMS_COUNT, error_out=False).items
    return jsonify([dict(cur_page=page, id=category.id, name=category.name) for category in categories])


@main.route('/category/<name>/search', methods=['GET', 'POST'])
def search_by_category(name):
    list_id = request.args.get('list_id', None, type=int)
    page_count = 1
    category = Category.query.filter_by(name=name).first()
    res = category.books.all()
    books = Book.query.all()
    date_list = list()
    if res:
        top_books = list()
        for book in res:
            try:
                top_books.append([book, round(
                    sum([value.grade for value in book.grades.all()]) / len(book.grades.all()), 1)])
            except:
                top_books.append([book, 0])
            if not book.release_date in date_list:
                date_list.append(book.release_date)
        if len(top_books) > TOP_BOOKS_COUNT:
            top_books = sorted(top_books, key=itemgetter(1))[-TOP_BOOKS_COUNT:]
        else:
            top_books = sorted(top_books, key=itemgetter(1))
    else:
        top_books = list()

    if request.method == 'POST':
        result = str(request.form.get('search_result')).strip().lower()
        if result == 'все':
            search_result = res

        elif result == '*':
            search_result = books

        else:
            release_date = request.form.get('release_date')
            if release_date != '#':
                search_result = category.books.filter_by(
                    release_date=release_date).all()

            elif result:
                search_result = category.books.filter((Book.name.like("%{}%".format(result))) | (
                    Book.author.like("%{}%".format(result)))).all()
            else:
                search_result = None

            if search_result:
                search_result_fin = []
                [search_result_fin.append(
                    value) for value in search_result if value and value not in search_result_fin]
                search_result = search_result_fin
            else:
                page_count = None

        if not search_result:
            search_result = 404
        all_search_result = search_result

        if search_result != 404:
            old_books_result = SearchResult.query.all()
            if old_books_result:
                for elem in old_books_result:
                    database.session.delete(elem)
            for book in search_result:
                book_for_cur_result = SearchResult(book)
                database.session.add(book_for_cur_result)
            database.session.commit()
            if len(search_result) > ELEMS_COUNT:
                page_count = len(search_result) // ELEMS_COUNT
                if len(search_result) % ELEMS_COUNT > 0:
                    page_count += 1
                search_result = search_result[:ELEMS_COUNT]
            else:
                page_count = 1
        return render_template('main/category_page.html', search_result=search_result, date_list=date_list, top_books=top_books, len=len, page_count=page_count, page=1, range=range, name=name, list_id=list_id, all_search_result=all_search_result)

    elif page := request.args.get('page', None, type=int):
        cur_result = SearchResult.query.all()
        page_count = 1
        temp_arr = list()
        search_result = dict()
        counter = 0
        for book in cur_result:
            counter += 1
            temp_arr.append(book)
            if counter % ELEMS_COUNT == 0:
                search_result[page_count] = copy.copy(temp_arr)
                page_count += 1
                temp_arr = list()

        if counter % ELEMS_COUNT > 0:
            search_result[page_count] = temp_arr
        else:
            page_count -= 1
        try:
            search_result = search_result[page]
        except:
            return render_template('main/category_page.html', name=name, search_result=0, date_list=date_list, top_books=top_books, list_id=list_id, len=len)
        return render_template('main/category_page.html', search_result=search_result, date_list=date_list, top_books=top_books, len=len, page_count=page_count, page=page, range=range, name=name, list_id=list_id, all_search_result=cur_result)
    return render_template('main/category_page.html', name=name, search_result=0, date_list=date_list, top_books=top_books, list_id=list_id, len=len)


@main.route('/forum')
def forum():
    category_pagination = Category.query.order_by().paginate(
        1, per_page=ELEMS_COUNT, error_out=False)
    categories = category_pagination.items
    pagination_for_topics_foreach_category = list()
    for category in categories:
        pagination_for_topics_foreach_category.append(
            category.topics.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False))
    return render_template('main/forum.html', pagination_for_topics_foreach_category=pagination_for_topics_foreach_category, category_pagination=category_pagination, categories=categories, len=len, zip=zip, display="none")


@main.route('/forum/<topic_id>')
def topic(topic_id):
    posts_page = request.args.get('posts_page', 1, type=int)
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        user_is_admin = 1
    else:
        user_is_admin = 0
    posts_pagination = topic.posts.order_by().paginate(
        posts_page, per_page=ELEMS_COUNT, error_out=False)
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.answer_to_post:
            post_from = topic.posts.filter_by(id=post.answer_to_post).first()
            if post_from:
                posts.append({"this_is_answer": True, "username_of_post_from": post_from.user.username, "body_of_post_from": post_from.body, "id": post.id, "file": post.file, "body": post.body,
                             "post_timestamp": post.timestamp, "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender})
            else:
                posts.append({"this_is_answer": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                             "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender})
        else:
            posts.append({"this_is_answer": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                         "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender})
    return render_template('main/forum_discussion.html', user_is_admin=user_is_admin, topic_id=topic_id, topic_name=topic.name, posts_count=len(topic.posts.all()), posts_pagination=posts_pagination, posts=posts, str=str, display="none")


@main.route('/get_categories_page_on_forum/<page>', methods=['GET'])
def get_categories_page_on_forum(page):
    page = int(page)
    categories_pagination = Category.query.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(categories_pagination.iter_pages())
    categories = categories_pagination.items
    categories_topics = dict()
    for category in categories:
        topics_pagination = category.topics.order_by().paginate(
            1, per_page=ELEMS_COUNT, error_out=False)
        category_topics = [dict(id=topic.id, name=topic.name, cur_page=1,
                                topic_pages=list(topics_pagination.iter_pages())) for topic in topics_pagination.items]
        categories_topics[category.id] = copy.deepcopy(category_topics)

    if current_user.is_authenticated:
        username_of_cur_user = current_user.username
        if current_user.role == Role.ADMIN:
            is_admin = True
        else:
            is_admin = False
    else:
        username_of_cur_user = False
        is_admin = False

    return jsonify([dict(cur_user_is_admin=is_admin, cur_page=page, pages_count=pages_count, username_of_cur_user=username_of_cur_user, id=category.id, name=category.name, topics=topics, topics_count=len(category.topics.all())) for category, topics in zip(categories, categories_topics.values())])


@main.route('/get_posts_page/<topic_id>/<page>', methods=['GET'])
def get_posts_page(topic_id, page):
    page = int(page)
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    posts_pagination = topic.posts.order_by().paginate(
        page, per_page=ELEMS_COUNT, error_out=False)
    posts = list()
    if current_user.is_authenticated:
        username = current_user.username
        if current_user.role == Role.ADMIN:
            user_is_admin = True
        else:
            user_is_admin = False
    else:
        username = None
        user_is_admin = False

    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            if post.answer_to_post:
                post_from = topic.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
                else:
                    posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
        else:
            if post.answer_to_post:
                post_from = topic.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
                else:
                    posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
    return jsonify(posts)


@main.route('/search_category_on_forum', methods=['POST'])
def search_category_on_forum():
    category_name = str(request.form.get('category_name')).strip().lower()
    found_category = Category.query.filter(
        Category.name.like("%{}%".format(category_name))).first()
    if found_category:
        page = 1
        cur_page_items = list()
        while True:
            cur_page_items = Category.query.order_by().paginate(
                page, per_page=ELEMS_COUNT, error_out=False).items
            if found_category in cur_page_items:
                break
            page += 1

        categories_topics = dict()
        for category in cur_page_items:
            topics_pagination = category.topics.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False)
            category_topics = [dict(id=topic.id, name=topic.name, cur_page=1,
                                    pages_count=list(topics_pagination.iter_pages())) for topic in topics_pagination.items]
            categories_topics[category.id] = copy.deepcopy(category_topics)

        if current_user.is_authenticated:
            username_of_cur_user = current_user.username
        else:
            username_of_cur_user = False
        return jsonify([dict(result=True, cur_page=page, username_of_cur_user=username_of_cur_user, id_of_found_elem=found_category.id, id=cur_page_category.id, name=cur_page_category.name, topics=topics, topics_count=len(cur_page_category.topics.all())) for cur_page_category, topics in zip(cur_page_items, categories_topics.values())])
    else:
        return jsonify([dict(result=False)])


@main.route('/<username>/<category_name>/add_topic', methods=['POST'])
@login_required
@check_actual_password
def add_topic(username, category_name):
    if current_user.username != username:
        return render_template('403.html')
    page = request.args.get('page', 1, type=int)
    in_topic_name = str(request.form.get('topic_name')).strip().lower()
    cur_category = Category.query.filter_by(name=category_name).first()
    result = True
    for topic in cur_category.topics.all():
        if topic.name == in_topic_name:
            result = False
            break
    if result:
        topic = DiscussionTopic(name=in_topic_name, category=cur_category)
        database.session.add(topic)
        database.session.commit()
        topics_for_cur_category = cur_category.topics.all()
        last_page = len(topics_for_cur_category) // ELEMS_COUNT
        if len(topics_for_cur_category) % ELEMS_COUNT > 0:
            last_page += 1
            
        topics_pagination = cur_category.topics.order_by().paginate(last_page, per_page=ELEMS_COUNT, error_out=False)
        pages_count = list(topics_pagination.iter_pages())
        topics_for_cur_category_by_page = topics_pagination.items
        if current_user.role == Role.ADMIN:
            is_admin = True
        else:
            is_admin = False
        return jsonify([dict(result=result, cur_user_is_admin=is_admin, pages_count=pages_count, topic_pages=last_page, category_id=cur_category.id, topic_id=topic.id, name=topic.name, topics_count=len(topics_for_cur_category_by_page)) for topic in topics_for_cur_category_by_page])
    return jsonify([dict(result=result)])


@main.route('/get_topics_page_on_forum/<category_id>/<page>', methods=['GET'])
def get_topics_page_on_forum(category_id, page):
    page = int(page)
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        is_admin = True
    else:
        is_admin = False
    category = Category.query.filter_by(id=category_id).first()
    topics_pagination = category.topics.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(topics_pagination.iter_pages())
    topics = topics_pagination.items
    return jsonify([dict(cur_user_is_admin=is_admin, cur_page=page, id=topic.id, name=topic.name, pages_count=pages_count) for topic in topics])


@main.route('/<username>/edit_post/<topic_id>/<post_id>', methods=['POST'])
@login_required
@check_actual_password
def edit_post(username, topic_id, post_id):
    if current_user.username != username:
        return render_template('403.html')
    post = TopicPost.query.filter_by(id=post_id).first()
    post.body = str(request.form.get('newComment')).strip().replace("'", "")
    database.session.add(post)
    database.session.commit()
    return jsonify(dict(topic_id=topic_id, post_id=post_id, post_body=post.body, username=current_user.username))


@main.route('/delete-topic/<category_id>/<topic_id>/<page>', methods=['GET'])
@admin_required
@check_actual_password
def topic_delete(category_id, topic_id, page):
    page = int(page)
    category = Category.query.filter_by(id=category_id).first()
    if category:
        topic = category.topics.filter_by(id=topic_id).first()
        database.session.delete(topic)
        database.session.commit()

    if topics := category.topics.all():
        has_elems = True
        topics_pagination = category.topics.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages_count = list(topics_pagination.iter_pages())
        if not topics_pagination.items:
            page -= 1
    else:
        page = 1
        pages_count = 1
        has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, topics_count=len(topics)))


@main.route('/books-maintaining', methods=['GET'])
@admin_required
@check_actual_password
def books_relevance():
    pagination = BooksMaintaining.query.order_by().paginate(1, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
    return render_template('main/books_maintaining.html', info=pagination.items, pagination=pagination)


@main.route('/books-maintaining/add-file', methods=['POST'])
@admin_required
@check_actual_password
def add_new_books_info():
    file = request.files['data_file']
    if file.filename.split('.')[-1] != "xlsx":
        return jsonify([dict(result=False)])
    
    data = parse_excel(file)
    if not data:
        return jsonify([dict(result=False)])
    
    for book_info in data:
        if BooksMaintaining.query.filter_by(name=book_info[0]).first():
            continue
        book_obj = BooksMaintaining(name=book_info[0], authors=book_info[1], series=book_info[2], 
                        categories=book_info[3], publishing_date=book_info[4], publishing_house=book_info[5],
                        pages_count=book_info[6], isbn=book_info[7], comments=book_info[8], summary=book_info[9], 
                        link=book_info[10], count=book_info[11])
        
        database.session.add(book_obj)
    database.session.commit()
    
    data = BooksMaintaining.query.all(); data_len = len(data); data = data[data_len - BOOKS_MAINTAINING_PER_PAGE:]
    
    # найдем количество страниц
    pages = data_len // BOOKS_MAINTAINING_PER_PAGE
    if data_len % BOOKS_MAINTAINING_PER_PAGE > 0:
        pages += 1
    
    return jsonify([dict(result=True, pages=pages, cur_page=pages, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                        categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                        pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                        link=book_info.link, count=book_info.count) for book_info in data])
    # Название - 0
    # Авторы - 1
    # серия - 2
    # категории - 3
    # дата публикации - 4
    # Издательство - 5
    # Количество страниц - 6
    # ISBN - 7
    # Комментарии - 8
    # Описание - 9
    # Ссылка - 10
    

@main.route('/books-maintaining/search', methods=['POST'])
@admin_required
@check_actual_password
def search_book():
    book_name = str(request.form.get('search_result')).strip().lower()
    book = BooksMaintaining.query.filter(BooksMaintaining.name.like("%{}%".format(book_name))).first()
    if not book:
        return jsonify([dict(result=False)])
    
    pagination = BooksMaintaining.query.paginate(1, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
    if book in pagination.items:
        return jsonify([dict(result=True, cur_page=1, pages=pagination.pages, id_of_found_elem=book.id, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                            categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                            pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                            link=book_info.link, count=book_info.count) for book_info in pagination.items])
    for page in range(2, pagination.pages + 1):  
        items = BooksMaintaining.query.paginate(page, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False).items
        if book in items:
            return jsonify([dict(result=True, cur_page=page, pages=pagination.pages, id_of_found_elem=book.id, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                                categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                                pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                                link=book_info.link, count=book_info.count) for book_info in items])
            

@main.route('/books-maintaining/get-page/<page>', methods=['GET'])
@admin_required
@check_actual_password
def get_books_info_page(page):
    page = int(page)
    data = BooksMaintaining.query.order_by().paginate(page, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False).items
    return jsonify([dict(cur_page=page, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                        categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                        pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                        link=book_info.link, count=book_info.count) for book_info in data])
    

@main.route('/books-maintaining/change-count', methods=['POST'])
@admin_required
@check_actual_password
def change_books_count():
    book = BooksMaintaining.query.filter_by(id=int(request.form.get('id'))).first()
    book.count = int(request.form.get('new_count'))
    database.session.add(book)
    database.session.commit()
    return jsonify(dict(count=book.count))


@main.route('/books-maintaining/del-book', methods=['POST'])
@admin_required
@check_actual_password
def book_del():
    try:
        book = BooksMaintaining.query.filter_by(id=int(request.form.get('id'))).first()
        database.session.delete(book)
        database.session.commit()
        return jsonify(dict(result=True))
    except:
        return jsonify(dict(result=False))
