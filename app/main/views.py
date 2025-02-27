from . import main
from .. import database
from app.main import *
from app.models import BookGrade, Book, Comment, Category, User, TopicPost, DiscussionTopic, Role, BooksMaintaining, PrivateChat, PrivateChatPost
from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import current_user, login_required
from app.decorators import admin_required, check_actual_password
from app.parse_excel import *
import copy
from datetime import datetime


@main.app_context_processor
def inject_roles():
    return dict(Role=Role)


@main.app_context_processor
def inject_months_dict():
    return dict(months_dict=months_dict)


@main.route('/<int:book_id>/get-cover', methods=['GET'])
def cover(book_id):
    book = Book.query.filter_by(id=book_id).first()
    cover = make_response(book.cover)
    return cover


@main.route('/<post_id>/get-post-screenshot', methods=['GET'])
def post_screenshot(post_id):
    post = TopicPost.query.filter_by(id=post_id).first()
    file = make_response(post.file)
    return file


@main.route('/<post_id>/get-post-screenshot-on-private-chat', methods=['GET'])
def post_screenshot_on_private_chat(post_id):
    post = PrivateChatPost.query.filter_by(id=post_id).first()
    file = make_response(post.file)
    return file


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/book-page/<int:book_id>', methods=['GET'])
def book_page(book_id):
    list_id = request.args.get('list_id', None, type=int)
    book = Book.query.filter_by(id=book_id).first()
    pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(
        1, per_page=ELEMS_COUNT, error_out=False)
    comments = pagination.items
    grades = book.grades.all()
    try:
        fin_grade = round(sum([value.grade for value in grades]) / len(grades), 1)
    except:
        fin_grade = 0
    return render_template('main/book_page.html', book=book, fin_grade=fin_grade, comments=comments, pagination=pagination, len=len, str=str, grade_count=len(grades), int=int, list_id=list_id, display="none")


@main.route('/get_comments_page/<int:book_id>/<int:page>', methods=['GET'])
def get_comments_page(book_id, page):
    book = Book.query.filter_by(id=book_id).first()
    comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(comments_pagination.iter_pages())
    comments = comments_pagination.items
    users = list()
    user_is_admin = True if (current_user.is_authenticated and current_user.role == Role.ADMIN) else False
    name_of_current_user = current_user.username if (current_user.is_authenticated) else None
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(cur_page=page, pages_count=pages_count, user_is_admin=user_is_admin, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_id=book_id, username=user.username, name_of_current_user=name_of_current_user, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])


@main.route('/<username>/<int:book_id>/add_comment', methods=['POST'])
@login_required
@check_actual_password
def add_comment(username, book_id):
    if current_user.username != username:
        return render_template('403.html')
    book = Book.query.filter_by(id=book_id).first()
    comment = Comment(body=str(request.form.get('comment')).strip().replace("'", ""), book=book, user=current_user._get_current_object())
    database.session.add(comment)
    database.session.commit()
    comments = book.comments.all()
    last_page = len(comments) // ELEMS_COUNT
    id_of_added_comment = comments[-1].id
    if len(comments) % ELEMS_COUNT > 0:
        last_page += 1
    comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(last_page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(comments_pagination.iter_pages())
    comments = comments_pagination.items
    user_is_admin = True if current_user.role == Role.ADMIN else False
    users = list()
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(pages=last_page, user_is_admin=user_is_admin, pages_count=pages_count, id_of_added_comment=id_of_added_comment, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_id=book_id, username=user.username, name_of_current_user=current_user.username, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])


@main.route('/<username>/<int:book_id>/edit-comment/<int:comment_id>', methods=['POST'])
@login_required
@check_actual_password
def edit_comment(username, comment_id, book_id):
    if current_user.username != username:
        return render_template('403.html')
    comment = Comment.query.filter_by(id=comment_id).first()
    comment.body = str(request.form.get('newComment')).strip().replace("'", "")
    comment.timestamp = datetime.now()
    database.session.add(comment)
    database.session.commit()
    return jsonify(dict(id=comment_id, body=comment.body, username=current_user.username, book_id=book_id, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year)))


@main.route('/<username>/give-grade/<int:book_id>', methods=['GET'])
@login_required
@check_actual_password
def give_grade(username, book_id):
    if current_user.username != username:
        return render_template('403.html')
    book = Book.query.filter_by(id=book_id).first()
    grade = int(request.args.get('grade'))
    previous_grade = BookGrade.query.filter_by(user=current_user, book=book).first()
    if previous_grade:
        database.session.delete(previous_grade)

    grade = BookGrade(grade=grade, user=current_user, book=book)
    database.session.add(grade)
    database.session.commit()
    return redirect(url_for('main.book_page', book_id=book.id))


@main.route('/<username>/<int:book_id>/delete-comment/<int:comment_id>/<int:page>', methods=['GET'])
@login_required
@check_actual_password
def comment_delete(username, book_id, comment_id, page):
    if current_user.username != username:
        return render_template('403.html')
    page = int(page)
    book = Book.query.filter_by(id=book_id).first()
    comment = book.comments.filter_by(id=comment_id).first()
    database.session.delete(comment)
    database.session.commit()
    if book.comments.all():
        has_elems = True
        comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages_count = list(comments_pagination.iter_pages())
        if not comments_pagination.items:
            page -= 1
    else:
        page = 1; pages_count = [1]; has_elems = False
    return jsonify(dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, username=current_user.username, book_id=book_id))


@main.route('/categories', methods=['GET'])
def categories():
    list_id = request.args.get('list_id', None, type=int)
    category_pagination = Category.query.order_by().paginate(
        1, per_page=ELEMS_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('main/categories.html', categories=categories, category_pagination=category_pagination, list_id=list_id)


@main.route('/get_categories_page/<int:page>', methods=['GET'])
def get_categories_page(page):
    categories_pagination = Category.query.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(categories_pagination.iter_pages())
    categories = categories_pagination.items
    return jsonify([dict(cur_page=page, id=category.id, pages_count=pages_count, name=category.name) for category in categories])


@main.route('/category/<int:id>', methods=['GET'])
def category(id):
    list_id = request.args.get('list_id', None, type=int)
    category = Category.query.filter_by(id=id).first()
    if not category:
        return render_template('404.html')
    res = category.books.all()
    top_books = list(); new_books = list()
    if res:
        for book in res:
            try:
                top_books.append([book, round(sum([value.grade for value in book.grades.all()]) / len(book.grades.all()), 1)])
                new_books.append([book, round(sum([value.grade for value in book.grades.all()]) / len(book.grades.all()), 1)])
            except:
                top_books.append([book, 0])
                new_books.append([book, 0])
           
        if len(top_books) > TOP_BOOKS_COUNT:
            top_books = sorted(top_books, key=lambda value: value[1], reverse=True)[:TOP_BOOKS_COUNT]
            new_books = sorted(new_books, key=lambda value: value[0].timestamp, reverse=True)[:TOP_BOOKS_COUNT]
        else:
            top_books = sorted(top_books, key=lambda value: value[1], reverse=True)
            new_books = sorted(new_books, key=lambda value: value[0].timestamp, reverse=True)
    return render_template('main/category_page.html', top_books=top_books, new_books=new_books, name=category.name, id=category.id, list_id=list_id, len=len)
        
        
@main.route('/category/<int:id>/search', methods=['POST'])
def search_by_category(id):
    if current_user.is_authenticated:
        current_user_is_auth = True; username = current_user.username
    else:
        current_user_is_auth = False; username = None
 
    category = Category.query.filter_by(id=id).first()
    if category is None:
        return render_template('404.html')
    res = category.books.order_by(Book.id).all()
    result = str(request.form.get('search_result')).strip().lower()
    if result == '*':
        search_result = res
    else:
        search_result = list(); release_date = request.form.get('release_date').strip(); description = request.form.get('description').strip()
        if result:
            search_result += category.books.filter((Book.name.like("%{}%".format(result))) | (Book.author.like("%{}%".format(result)))).all()
        if release_date:
            search_result += category.books.filter_by(release_date=release_date).all()
        if description:
            search_result += category.books.filter((Book.description.like("%{}%".format(description)))).all()
        
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
            books.append(dict(result=True, id=book.id, name=book.name, grade=book_grade, category_id=category.id, current_user_is_auth=current_user_is_auth, username=username, author=book.author, pages_count=pages_count, results_count=results_count))
        for page in range(1, pages_count + 1):
            res[page] = books[(page - 1) * ELEMS_COUNT: page * ELEMS_COUNT]
            
        return jsonify(dict(result=True, data=res))
    return jsonify(dict(result=False))


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


@main.route('/forum/<int:topic_id>')
def topic(topic_id):
    posts_page = request.args.get('posts_page', 1, type=int)
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        user_is_admin = 1
    else:
        user_is_admin = 0
    posts_pagination = topic.posts.order_by(TopicPost.id).paginate(
        posts_page, per_page=ELEMS_COUNT, error_out=False)
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.answer_to_post:
            post_from = topic.posts.filter_by(id=post.answer_to_post).first()
            if post_from:
                posts.append({"this_is_answer": True, "basic_post_exist": True, "base_id": post_from.id, "username_of_post_from": post_from.user.username, "body_of_post_from": post_from.body, "id": post.id, "file": post.file, "body": post.body,
                             "post_timestamp": post.timestamp, "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
            else:
                posts.append({"this_is_answer": True, "basic_post_exist": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                             "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
        else:
            posts.append({"this_is_answer": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                         "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
    return render_template('main/forum_discussion.html', user_is_admin=user_is_admin, topic_id=topic_id, topic_name=topic.name, posts_count=len(topic.posts.all()), posts_pagination=posts_pagination, posts=posts, str=str)


@main.route('/get_categories_page_on_forum/<int:page>', methods=['GET'])
def get_categories_page_on_forum(page):
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


@main.route('/get_posts_page/<int:topic_id>/<int:page>', methods=['GET'])
def get_posts_page(topic_id, page):
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    posts_pagination = topic.posts.order_by(TopicPost.id).paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(posts_pagination.iter_pages())
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
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
        else:
            if post.answer_to_post:
                post_from = topic.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
    return jsonify(dict(posts=posts, pages_count=pages_count))


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
            if current_user.role == Role.ADMIN:
                is_admin = True
            else:
                is_admin = False
            username_of_cur_user = current_user.username
        else:
            username_of_cur_user = False; is_admin = False
        return jsonify([dict(result=True, cur_page=page, username_of_cur_user=username_of_cur_user, cur_user_is_admin=is_admin, id_of_found_elem=found_category.id, id=cur_page_category.id, name=cur_page_category.name, topics=topics, topics_count=len(cur_page_category.topics.all())) for cur_page_category, topics in zip(cur_page_items, categories_topics.values())])
    else:
        return jsonify([dict(result=False)])


@main.route('/<username>/<int:category_id>/add_topic', methods=['POST'])
@login_required
@check_actual_password
def add_topic(username, category_id):
    if current_user.username != username:
        return render_template('403.html')
    in_topic_name = str(request.form.get('topic_name')).strip().lower()
    cur_category = Category.query.filter_by(id=category_id).first()
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
        return jsonify([dict(result=result, cur_user_is_admin=is_admin, pages_count=pages_count, topic_pages=last_page, category_id=cur_category.id, topic_id=topic.id, name=topic.name, topics_count=len(topics_for_cur_category)) for topic in topics_for_cur_category_by_page])
    return jsonify([dict(result=result)])


@main.route('/get_topics_page_on_forum/<int:category_id>/<int:page>', methods=['GET'])
def get_topics_page_on_forum(category_id, page):
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        is_admin = True
    else:
        is_admin = False
    category = Category.query.filter_by(id=category_id).first()
    topics_pagination = category.topics.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(topics_pagination.iter_pages())
    topics = topics_pagination.items
    return jsonify([dict(cur_user_is_admin=is_admin, cur_page=page, id=topic.id, name=topic.name, pages_count=pages_count) for topic in topics])


@main.route('/delete-topic/<int:category_id>/<int:topic_id>/<int:page>', methods=['GET'])
@admin_required
@check_actual_password
def topic_delete(category_id, topic_id, page):
    category = Category.query.filter_by(id=category_id).first()
    if category:
        topic = category.topics.filter_by(id=topic_id).first()
        database.session.delete(topic)
        database.session.commit()
    else:
        return render_template('404.html')

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
    
    data_len = BooksMaintaining.query.count()
    # найдем количество страниц
    pages = data_len // BOOKS_MAINTAINING_PER_PAGE
    if data_len % BOOKS_MAINTAINING_PER_PAGE > 0:
        pages += 1
    # pages - она же последняя страница
    data_pagination = BooksMaintaining.query.order_by().paginate(pages, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
    pages_count_arr = list(data_pagination.iter_pages())
    data = data_pagination.items
    
    return jsonify([dict(result=True, pages_count_arr=pages_count_arr, cur_page=pages, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
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
        pages_count_arr = list(pagination.iter_pages())
        return jsonify([dict(result=True, cur_page=1, pages_count_arr=pages_count_arr, id_of_found_elem=book.id, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                            categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                            pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                            link=book_info.link, count=book_info.count) for book_info in pagination.items])
    for page in range(2, pagination.pages + 1):  
        items_pagination = BooksMaintaining.query.paginate(page, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
        items = items_pagination.items
        if book in items:
            pages_count_arr = list(items_pagination.iter_pages())
            return jsonify([dict(result=True, cur_page=page, pages_count_arr=pages_count_arr, id_of_found_elem=book.id, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
                                categories=book_info.categories, publishing_date=book_info.publishing_date, publishing_house=book_info.publishing_house,
                                pages_count=book_info.pages_count, isbn=book_info.isbn, comments=book_info.comments, summary=book_info.summary, 
                                link=book_info.link, count=book_info.count) for book_info in items])
            

@main.route('/books-maintaining/get-page/<int:page>', methods=['GET'])
@admin_required
@check_actual_password
def get_books_info_page(page):
    data_pagination = BooksMaintaining.query.order_by().paginate(page, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
    pages_count_arr = list(data_pagination.iter_pages())
    data = data_pagination.items
    return jsonify([dict(cur_page=page, pages_count_arr=pages_count_arr, id=book_info.id, name=book_info.name, authors=book_info.authors, series=book_info.series, 
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
        page = int(request.form.get('page'))
        book = BooksMaintaining.query.filter_by(id=int(request.form.get('id'))).first()
        database.session.delete(book)
        database.session.commit()
        
        # получаем данные для перестройки пагинации
        if BooksMaintaining.query.all():
            data_pagination = BooksMaintaining.query.order_by().paginate(page, per_page=BOOKS_MAINTAINING_PER_PAGE, error_out=False)
            pages_count_arr = list(data_pagination.iter_pages())
            if not data_pagination.items:
                page -= 1
            return jsonify(dict(result=True, cur_page=page, pages_count_arr=pages_count_arr))
        else:
            return jsonify(dict(result=False))
    except:
        return jsonify(dict(result=False))
    

@main.route('/forum/create_private_chat', methods=['POST'])
@login_required
@check_actual_password
def create_private_chat():
    private_chat_name = request.form.get('private_chat_name').strip().lower()
    if current_user.private_chats.filter_by(name=private_chat_name).first():
        return jsonify(dict(result=1))
    elif len(current_user.private_chats.all()) >= MAX_PRIVATE_CHATS_PER_USER:
        return jsonify(dict(result=0))
    private_chat = PrivateChat(name=private_chat_name, creator=current_user._get_current_object())
    database.session.add(private_chat)
    database.session.commit()
    return jsonify(dict(result=2))


@main.route('/forum/private_chats', methods=['GET'])
@login_required
@check_actual_password
def private_chats():
    private_chats = current_user.private_chats.all()
    chats_invitations = current_user.chats_invitations.all()
    chats_info = list()
    for private_chat in private_chats:
        chats_info.append([private_chat.id, private_chat.name, "created"])
    for chat_invitation in chats_invitations:
        chats_info.append([chat_invitation.private_chat.id, chat_invitation.private_chat.name, "invited"])
        
    if chats_info:   
        # найдем количество страниц
        info_count = len(chats_info)
        pages = info_count // ELEMS_COUNT
        if info_count % ELEMS_COUNT > 0:
            pages += 1
        
        res = dict()
        for page in range(1, pages + 1):
            res[page] = chats_info[(page - 1) * ELEMS_COUNT: page * ELEMS_COUNT]
        chats_info = res[1]
    else:
        pages = None
    invitations = current_user.chats_invitations.filter_by(viewed=False).all()
    for invitation in invitations:
        invitation.viewed = True
        database.session.add(invitation)
    database.session.commit()
    return render_template('main/private_chats.html', chats_info=chats_info, pages=pages, range=range)
    

@main.route('/forum/delete_private_chat/<int:chat_id>/<int:page>', methods=['GET'])
@login_required
@check_actual_password
def delete_private_chat(chat_id, page):
    private_chat = current_user.private_chats.filter_by(id=chat_id).first()
    database.session.delete(private_chat)
    database.session.commit()
        
    # получаем данные для перестройки пагинации
    private_chats = current_user.private_chats.all()
    chats_invitations = current_user.chats_invitations.all()
    chats_info = list()
    for private_chat in private_chats:
        chats_info.append([private_chat.id, private_chat.name, "created"])
    for chat_invitation in chats_invitations:
        chats_info.append([chat_invitation.private_chat.id, chat_invitation.private_chat.name, "invited"])
        
    if chats_info:   
        has_elems = True
        # найдем количество страниц
        info_count = len(chats_info)
        pages_count = info_count // ELEMS_COUNT
        if info_count % ELEMS_COUNT > 0:
            pages_count += 1
        
        res = dict(); pages_count_list = list()
        for page in range(1, pages_count + 1):
            res[page] = chats_info[(page - 1) * ELEMS_COUNT: page * ELEMS_COUNT]
        if res.get(page):
            chats_info = res[page]
            cur_page = page
        else:
            chats_info = res[page - 1]
            cur_page = page - 1
        for page in range(1, pages_count + 1):
            if page % 4 != 0:
                pages_count_list.append(page)
            else:
                pages_count_list.append(None)
        return jsonify([dict(has_elems=has_elems, cur_page=cur_page, pages_count=pages_count_list, id=chat[0], name=chat[1], type=chat[2]) for chat in chats_info])
    return jsonify([dict(has_elems=False)])
 
 
@main.route('/forum/get_chats_page/<int:page>', methods=['GET'])
@login_required
@check_actual_password
def get_chats_page(page):
    chats_info = list()
    private_chats = current_user.private_chats.all()
    chats_invitations = current_user.chats_invitations.all()
    for private_chat in private_chats:
        chats_info.append([private_chat.id, private_chat.name, "created"])
    for chat_invitation in chats_invitations:
        chats_info.append([chat_invitation.private_chat.id, chat_invitation.private_chat.name, "invited"])
        
    # найдем количество страниц
    info_count = len(chats_info)
    pages_count = info_count // ELEMS_COUNT
    if info_count % ELEMS_COUNT > 0:
        pages_count += 1
    
    res = dict(); pages_count_list = list()
    for page in range(1, pages_count + 1):
        res[page] = chats_info[(page - 1) * ELEMS_COUNT: page * ELEMS_COUNT]
    chats_info = res[page]
    for page in range(1, pages_count + 1):
        if page % 4 != 0:
            pages_count_list.append(page)
        else:
            pages_count_list.append(None)
    return jsonify([dict(cur_page=page, pages_count=pages_count_list, id=chat[0], name=chat[1], type=chat[2]) for chat in chats_info])


@main.route('/forum/private_chat/<int:chat_id>', methods=['GET'])
@login_required
@check_actual_password
def private_chat(chat_id):
    chat = PrivateChat.query.filter_by(id=chat_id).first()
    if not chat or (chat not in current_user.private_chats and not current_user.chats_invitations.filter_by(private_chat=chat).first()):
        return render_template('403.html')

    participants_count = chat.invitations.count() + 1
    if current_user.is_authenticated and current_user.role == Role.ADMIN:
        user_is_admin = 1
    else:
        user_is_admin = 0
    posts_pagination = chat.posts.order_by(PrivateChatPost.id).paginate(1, per_page=ELEMS_COUNT, error_out=False)
   
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.answer_to_post:
            post_from = chat.posts.filter_by(id=post.answer_to_post).first()
            if post_from:
                posts.append({"this_is_answer": True, "basic_post_exist": True, "base_id": post_from.id, "username_of_post_from": post_from.user.username, "body_of_post_from": post_from.body, "id": post.id, "file": post.file, "body": post.body,
                             "post_timestamp": post.timestamp, "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
            else:
                posts.append({"this_is_answer": True, "basic_post_exist": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                             "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
        else:
            posts.append({"this_is_answer": False, "id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp,
                         "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender, "edited": post.edited})
    return render_template('main/private_chat_discussion.html', chat_creator_id=chat.creator.id, user_is_admin=user_is_admin, chat_id=chat.id, chat_name=chat.name, posts_count=len(chat.posts.all()), participants_count=participants_count, posts_pagination=posts_pagination, posts=posts, str=str)


@main.route('/get_posts_page_on_chat_disc/<int:chat_id>/<int:page>', methods=['GET'])
@login_required
@check_actual_password
def get_posts_page_on_chat_disc(chat_id, page):
    posts = list()
    chat = PrivateChat.query.filter_by(id=chat_id).first()
    posts_pagination = chat.posts.order_by(PrivateChatPost.id).paginate(page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(posts_pagination.iter_pages())
    username = current_user.username
    if current_user.role == Role.ADMIN:
        user_is_admin = True
    else:
        user_is_admin = False

    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            if post.answer_to_post:
                post_from = chat.posts.filter_by(id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
        else:
            if post.answer_to_post:
                post_from = chat.posts.filter_by(id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                    ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, cur_page=posts_pagination.page, chat_id=chat_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date(
                ).year), user_is_admin=user_is_admin, current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
    return jsonify(dict(posts=posts, pages_count=pages_count))


@main.route('/forum/private_chat/<int:chat_id>/get_users_page_to_invite/<int:page>', methods=['GET'])
@login_required
@check_actual_password
def get_users_page_to_invite(chat_id, page):
    chat = PrivateChat.query.filter_by(id=chat_id).first()
    if chat:
        invited_users_id_to_cur_chat = [invitation.user.id for invitation in chat.invitations.all()]  
        users_pagination = User.query.filter(User.id != current_user.id).filter(User.id != chat.creator.id).filter(~User.id.in_(invited_users_id_to_cur_chat)).paginate(page, per_page=USERS_COUNT, error_out=False)
        if not users_pagination.items:
            return jsonify([dict(result=False)])
        pages_count = list(users_pagination.iter_pages())
        users = users_pagination.items
        return jsonify([dict(result=True, cur_page=page, id=user.id, username=user.username, pages_count=pages_count, chat_id=chat.id) for user in users])
    else:
        return render_template('404.html')
    

@main.route('/change-topic-name/<int:category_id>/<int:topic_id>', methods=['POST'])
@admin_required
@check_actual_password 
def change_topic_name(category_id, topic_id):
    category = Category.query.filter_by(id=category_id).first()
    if not category:
        return render_template('404.html')
    topic = category.topics.filter_by(id=topic_id).first()
    topic.name = str(request.form.get('topic_changed_name')).strip().replace("'", "")
    database.session.add(topic)
    database.session.commit()
    return jsonify(dict(category_id=category_id, topic_id=topic_id, name=topic.name, username=current_user.username))
 
       
