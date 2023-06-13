from . import main
from app.init import database
from app.models import BookGrade, Book, Comment, SearchResult, Category, User, TopicPost, DiscussionTopic, Role
from flask import render_template, request, redirect, url_for, make_response, jsonify
from app.main.sort import sorting
from flask_login import current_user, login_required
import copy


ELEMS_COUNT = 6
months_dict = {
        1:'января',
        2:'февраля',
        3:'марта',
        4:'апреля',
        5:'мая',
        6:'июня',
        7:'июля',
        8:'августа',
        9:'сентября',
        10:'октября',
        11:'ноября',
        12:'декабря'
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
    pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(1, per_page=ELEMS_COUNT, error_out=False)
    comments = pagination.items
    fin_grade = 0
    grade_count = 0
    grades = BookGrade.query.filter_by(book=book).all()    
    for value in grades:
        fin_grade += value.grade
        grade_count += 1
    if grade_count:    
        fin_grade = round(fin_grade / grade_count, 1)
   
    return render_template('main/book_page.html', book=book, fin_grade=fin_grade, comments=comments, pagination=pagination, len=len, str=str, grade_count=grade_count, int=int, display="none") 


@main.route('/get_comments_page/<book_name>/<page>', methods=['GET'])
def get_comments_page(book_name, page):
    page = int(page)
    book = Book.query.filter_by(name=book_name).first()
    comments = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=ELEMS_COUNT, error_out=False).items
    users = list()
    user_is_admin = (current_user.role == Role.ADMIN)
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(user_is_admin=user_is_admin, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_name=book_name, username=user.username, name_of_current_user=current_user.username, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])
    

@main.route('/<username>/<book_name>/add_comment', methods=['POST'])
@login_required
def add_comment(username, book_name):
    book = Book.query.filter_by(name=book_name).first()
    comment = Comment(body=str(request.form.get('comment')).strip(), book=book, user=current_user._get_current_object())
    database.session.add(comment)
    database.session.commit()
    comments = book.comments.all(); last_page = len(comments) // ELEMS_COUNT; id_of_added_comment = comments[-1].id
    if len(comments) % ELEMS_COUNT > 0:
        last_page += 1
    comments = book.comments.order_by(Comment.timestamp.asc()).paginate(last_page, per_page=ELEMS_COUNT, error_out=False).items
    users = list()
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(pages=last_page, id_of_added_comment=id_of_added_comment, id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_name=book_name, username=user.username, name_of_current_user=current_user.username, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])
    
    
@main.route('/<username>/<book_name>/edit-comment/<comment_id>', methods=['POST'])
@login_required
def edit_comment(username, comment_id, book_name):
    comment = Comment.query.filter_by(id=comment_id).first()
    comment.body = request.form.get('newComment')
    database.session.add(comment)
    database.session.commit()
    return jsonify(dict(id=comment_id, body=comment.body, username=username, book_name=book_name))
   

@main.route('/<username>/give-grade/<book_id>/<grade>') 
@login_required
def give_grade(username, book_id, grade):
    book = Book.query.filter_by(id=book_id).first()
    previous_grade = BookGrade.query.filter_by(user=current_user, book=book).first()
    if previous_grade:
        database.session.delete(previous_grade)
        database.session.commit()
            
    grade = BookGrade(grade=grade, user=current_user, book=book)
    database.session.add(grade)
    database.session.commit()
    return redirect(url_for('main.book_page', name=book.name))


@main.route('/<username>/<book_name>/delete-comment/<comment_id>/<page>', methods=['GET'])  
@login_required
def comment_delete(username, book_name, comment_id, page):
    page = int(page)
    comment = Comment.query.filter_by(id=comment_id).first()
    database.session.delete(comment)
    database.session.commit()
    book = Book.query.filter_by(name=book_name).first()
    if book.comments.all(): 
        has_elems = True
        comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages = comments_pagination.pages
        if not comments_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, username=username, book_name=book_name))
    

@main.route('/categories', methods=['GET'])
def categories():
    list_id = request.args.get('list_id', None, type=int)
    category_pagination = Category.query.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('main/categories.html', categories=categories, category_pagination=category_pagination, list_id=list_id)


@main.route('/get_categories_page/<page>', methods=['GET'])
def get_categories_page(page):
    page = int(page)
    categories = Category.query.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False).items
    return jsonify([dict(id=category.id, name=category.name) for category in categories])
    
    
@main.route('/category/<name>/search', methods=['GET', 'POST'])
def search_by_category(name):
    list_id = request.args.get('list_id', None, type=int)
    page_count = 1
    books = Book.query.all()
    res = list()
    for book in books:
        if book.category.name == name:
            res.append(book)  
    categories = Category.query.all()
    date_list = list()
    if res:
        for book in res:
            if not book.release_date in date_list:
                date_list.append(book.release_date)
   
    if request.method == 'POST':
        result = str(request.form.get('search_result')).strip().lower()
        if result == 'все':
            search_result = res
            if not search_result:
                search_result = 404
        elif result == '*':
            search_result = books
            if not search_result:
                search_result = 404
        else:
            release_date = request.form.get('release_date') 
            if release_date != '#':
                search_result = Book.query.filter_by(release_date=release_date).all()
            
            elif result:
                search_result = Book.query.filter(Book.name.like("%{}%".format(result))).all()
                search_result_ = Book.query.filter(Book.author.like("%{}%".format(result))).all()
                search_result_for_category = search_result + search_result_
                res_for_category = list()
                for item in search_result_for_category:
                       if item.category.name == name:
                           res_for_category.append(item)
                search_result = res_for_category      
            else:
                search_result = None
              
            if search_result:
                search_result_fin = [] 
                [search_result_fin.append(value) for value in search_result if value not in search_result_fin]
                fin_result = list()
                for each in search_result_fin:
                    if each:
                        fin_result.append(each)
                search_result = fin_result
            else:
                search_result = 404
                page_count = None
        all_search_result = search_result
            
        if search_result != 404:
                old_books_result = SearchResult.query.all()
                if old_books_result:
                    for elem in old_books_result:
                        database.session.delete(elem)
                    database.session.commit()
                for book in search_result:
                    book_for_cur_result = SearchResult(book)
                    database.session.add(book_for_cur_result)
                database.session.commit()
                if len(search_result) > ELEMS_COUNT:
                    page_count = int(len(search_result) / ELEMS_COUNT)
                    if len(search_result) % ELEMS_COUNT > 0:
                        page_count += 1
                    search_result = search_result[:ELEMS_COUNT] 
                else:
                    page_count = 1
        return render_template('main/category_page.html', search_result=search_result, date_list=date_list, categories=categories, len=len, page_count=page_count, page=1, range=range, name=name, list_id=list_id, all_search_result=all_search_result)
    
    elif page := request.args.get('page', None, type=int):
        cur_result = SearchResult.query.all()
        page_count = 1; temp_arr = list(); search_result = dict(); counter = 0
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
            return render_template('main/category_page.html', name=name, search_result=0, date_list=date_list, len=len)
        return render_template('main/category_page.html', search_result=search_result, date_list=date_list, categories=categories, len=len, page_count=page_count, page=page, range=range, name=name, list_id=list_id, all_search_result=cur_result)
    
    return render_template('main/category_page.html', name=name, search_result=0, date_list=date_list, categories=categories, len=len)


@main.route('/forum')
def forum():
    category_pagination = Category.query.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False)
    categories = category_pagination.items
    pagination_for_topics_foreach_category = list()
    for category in categories:
        pagination_for_topics_foreach_category.append(category.topics.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False))
        
    return render_template('main/forum.html', pagination_for_topics_foreach_category=pagination_for_topics_foreach_category, category_pagination=category_pagination, categories=categories, len=len, zip=zip, display="none")


@main.route('/forum/<topic_id>')
def topic(topic_id):
    posts_page = request.args.get('posts_page', 1, type=int)
    topic = DiscussionTopic.query.filter_by(id=topic_id).first() 
    posts_pagination = topic.posts.order_by().paginate(posts_page, per_page=ELEMS_COUNT, error_out=False)
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        posts.append({"id": post.id, "file": post.file, "body": post.body, "post_timestamp": post.timestamp, "username": user.username, "user_timestamp": user.timestamp, "city": user.city, "age": user.age, "about_me": user.about_me, "gender": user.gender})
    return render_template('main/forum_discussion.html', topic_id=topic_id, topic_name=topic.name, posts_count=len(topic.posts.all()), posts_pagination=posts_pagination, posts=posts, str=str)


@main.route('/<username>/<discussion_topic_id>/add_post', methods=['POST'])
@login_required
def add_post(username, discussion_topic_id):
    user = User.query.filter_by(username=username).first()
    topic = DiscussionTopic.query.filter_by(id=discussion_topic_id).first()
    if request.files['screenshot'].filename != '':
        post = TopicPost(body=str(request.form.get('post_body')).strip(), user=user, topic=topic, file=request.files['screenshot'].read())
    else:
        post = TopicPost(body=str(request.form.get('post_body')).strip(), user=user, topic=topic, file=bytes(False))
    database.session.add(post)
    database.session.commit()
    topic = DiscussionTopic.query.filter_by(id=discussion_topic_id).first()
    posts_for_pagi = topic.posts.all(); last_page = len(posts_for_pagi) // ELEMS_COUNT
    if len(posts_for_pagi) % ELEMS_COUNT > 0:
        last_page += 1
    posts_pagination = topic.posts.order_by().paginate(last_page, per_page=ELEMS_COUNT, error_out=False) 
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            posts.append(dict(posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date().year), current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
        else:
            posts.append(dict(posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date().year), current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
    return jsonify(posts)
    
    
@main.route('/get_categories_page_on_forum/<page>', methods=['GET'])
def get_categories_page_on_forum(page):
    page = int(page)
    categories = Category.query.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False).items
    categories_topics = dict()
    for category in categories:
        topics_pagination = category.topics.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False)
        category_topics = [dict(id=topic.id, name=topic.name, cur_page=1, topic_pages=topics_pagination.pages) for topic in topics_pagination.items]
        categories_topics[category.id] = copy.deepcopy(category_topics)
        
    if current_user.is_authenticated:
        username_of_cur_user = current_user.username
    else:
        username_of_cur_user = False
    return jsonify([dict(username_of_cur_user=username_of_cur_user, id=category.id, name=category.name, topics=topics, topics_count=len(topics)) for category, topics in zip(categories, categories_topics.values())])


@main.route('/get_posts_page/<topic_id>/<page>', methods=['GET'])
def get_posts_page(topic_id, page):
    page = int(page)
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    posts_pagination = topic.posts.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False) 
    posts = list()
    if current_user.is_authenticated:
        username = current_user.username
    else:
        username = None
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            posts.append(dict(cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date().year), current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
        else:
            posts.append(dict(cur_page=posts_pagination.page, topic_id=topic_id, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(post.timestamp.date().year), current_username=username, username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
    return jsonify(posts)
    
    
@main.route('/<username>/del_post/<topic_id>/<post_id>/<page>', methods=['GET'])
@login_required
def post_delete(username, topic_id, post_id, page):
    page = int(page)
    post = TopicPost.query.filter_by(id=post_id).first()
    database.session.delete(post)
    database.session.commit()
    topic = DiscussionTopic.query.filter_by(id=topic_id).first()
    if posts := topic.posts.all():
        has_elems = True
        posts_pagination = topic.posts.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages = posts_pagination.pages
        if not posts_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, posts_count=len(posts)))


@main.route('/search_category_on_forum', methods=['POST'])
def search_category_on_forum():
    category_name = str(request.form.get('category_name')).strip().lower()
    found_category = Category.query.filter(Category.name.like("%{}%".format(category_name))).first()
    if found_category:
        page = 1; cur_page_items = list()
        while True:
            cur_page_items = Category.query.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False).items
            if found_category in cur_page_items:
                break
            page += 1
              
        categories_topics = dict()
        for category in cur_page_items:
            topics_pagination = category.topics.order_by().paginate(1, per_page=ELEMS_COUNT, error_out=False)
            category_topics = [dict(id=topic.id, name=topic.name, cur_page=1, pages=topics_pagination.pages) for topic in topics_pagination.items]
            categories_topics[category.id] = copy.deepcopy(category_topics)
            
        if current_user.is_authenticated:
            username_of_cur_user = current_user.username
        else:
            username_of_cur_user = False
        return jsonify([dict(result=True, cur_page=page, username_of_cur_user=username_of_cur_user, id_of_found_elem=found_category.id, id=cur_page_category.id, name=cur_page_category.name, topics=topics, topics_count=len(topics)) for cur_page_category, topics in zip(cur_page_items, categories_topics.values())])
    else:
        return jsonify([dict(result=False)])
    
    
@main.route('/<username>/<category_name>/add_topic', methods=['POST'])
@login_required
def add_topic(username, category_name):
    page = request.args.get('page', 1, type=int)
    in_topic_name = str(request.form.get('topic_name')).strip()
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
        cur_category = Category.query.filter_by(name=category_name).first()
        topics_for_cur_category = cur_category.topics.all(); last_page = len(topics_for_cur_category) // ELEMS_COUNT
        if len(topics_for_cur_category) % ELEMS_COUNT > 0:
            last_page += 1
        topics_for_cur_category_by_page = cur_category.topics.order_by().paginate(last_page, per_page=ELEMS_COUNT, error_out=False).items
        return jsonify([dict(result=result, topic_pages=last_page, category_id=cur_category.id, topic_id=topic.id, name=topic.name, topics_count=len(topics_for_cur_category_by_page)) for topic in topics_for_cur_category_by_page])
    return jsonify([dict(result=result)])


@main.route('/get_topics_page_on_forum/<category_id>/<page>', methods=['GET'])
def get_topics_page_on_forum(category_id, page):
    page = int(page)
    category = Category.query.filter_by(id=category_id).first()
    topics = category.topics.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False).items
    return jsonify([dict(id=topic.id, name=topic.name) for topic in topics])
   
  
        
        
   