from . import main
from app.init import database
from app.models import BookGrade, Book, Comment, SearchResult, Category, User, TopicMessage
from flask import render_template, request, redirect, url_for, make_response, jsonify
from app.main.sort import sorting
from flask_login import current_user, login_required
import copy


SEARCH_ITEMS_COUNT = 6
COMMENTS_COUNT = 8
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


@main.route('/<name>/get-cover')
def cover(name):
    book = Book.query.filter_by(name=name).first()
    cover = make_response(book.cover)
    return cover


@main.route('/')
def index():
    return render_template('main/index.html')
 

@main.route('/book-page/<name>', methods=['GET', 'POST'])
def book_page(name):
    global months_dict
    book = Book.query.filter_by(name=name).first()
    if request.method == 'POST' and request.form.get('comment') and current_user.is_authenticated:
        comment = Comment(body=request.form.get('comment'), book=book, user=current_user._get_current_object())
        database.session.add(comment)
        database.session.commit()
        return redirect(url_for('.book_page', name=book.name, page=-1))
    
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = round((book.comments.count() - 1) / COMMENTS_COUNT + 1, 1)
    
    pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=COMMENTS_COUNT, error_out=False)
    comments = pagination.items
    fin_grade = 0
    grade_count = 0
    grades = BookGrade.query.filter_by(book=book).all()    
    for value in grades:
        fin_grade += value.grade
        grade_count += 1
    if grade_count:    
        fin_grade = round(fin_grade / grade_count, 1)
   
    return render_template('main/book_page.html', book=book, fin_grade=fin_grade, comments=comments, pagination=pagination, len=len, str=str, grade_count=grade_count, months_dict=months_dict, int=int, display="none") 


@main.route('/get_comments_page/<book_name>/<page>', methods=['GET'])
def get_comments_page(book_name, page):
    page = int(page)
    book = Book.query.filter_by(name=book_name).first()
    comments = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=COMMENTS_COUNT, error_out=False).items
    users = list()
    for comment in comments:
        users.append(User.query.filter_by(id=comment.user_id).first())
    return jsonify([dict(id=comment.id, body=comment.body, day=str(comment.timestamp.date().day), month=months_dict[comment.timestamp.date().month], year=str(comment.timestamp.date().year), book_name=book_name, username=user.username, name_of_current_user=current_user.username, current_user_is_authenticated=current_user.is_authenticated) for comment, user in zip(comments, users)])
    

@main.route('/<username>/<book_name>/edit-comment/<comment_id>', methods=['POST'])
@login_required
def edit_comment(username, comment_id, book_name):
    comment = Comment.query.filter_by(id=comment_id).first()
    comment.body = request.form.get('newComment')
    database.session.add(comment)
    database.session.commit()
    page = request.args.get('page')
    return redirect(url_for('main.book_page', name=book_name, page=page))
   

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
        comments_pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=COMMENTS_COUNT, error_out=False)
        pages = comments_pagination.pages
        if not comments_pagination.items:
            page = page - 1
    else:
        page = 1; pages = 1; has_elems = False
    return jsonify(dict(cur_page=page, pages=pages, has_elems=has_elems, username=username, book_name=book_name))
    

@main.route('/categories', methods=['GET'])
def categories():
    list_id = request.args.get('list_id', None, type=int)
    category_pagination = Category.query.order_by().paginate(1, per_page=SEARCH_ITEMS_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('main/categories.html', categories=categories, category_pagination=category_pagination, list_id=list_id)


@main.route('/get_categories_page/<page>', methods=['GET'])
def get_categories_page(page):
    page = int(page)
    categories = Category.query.order_by().paginate(page, per_page=SEARCH_ITEMS_COUNT, error_out=False).items
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
                if len(search_result) > SEARCH_ITEMS_COUNT:
                    page_count = int(len(search_result) / SEARCH_ITEMS_COUNT)
                    if len(search_result) % SEARCH_ITEMS_COUNT > 0:
                        page_count += 1
                    search_result = search_result[:SEARCH_ITEMS_COUNT] 
                else:
                    page_count = 1
        return render_template('main/category_page.html', search_result=search_result, date_list=date_list, categories=categories, len=len, page_count=page_count, page=1, range=range, name=name, list_id=list_id, all_search_result=all_search_result)
    
    elif page := request.args.get('page', None, type=int):
        cur_result = SearchResult.query.all()
        page_count = 1; temp_arr = list(); search_result = dict(); counter = 0
        for book in cur_result:
            counter += 1
            temp_arr.append(book)
            if counter % SEARCH_ITEMS_COUNT == 0:
                search_result[page_count] = copy.copy(temp_arr)
                page_count += 1
                temp_arr = list()
                
        if counter % SEARCH_ITEMS_COUNT > 0:
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
    category_page = request.args.get('category_page', 1, type=int)
    category_pagination = Category.query.order_by().paginate(category_page, per_page=SEARCH_ITEMS_COUNT, error_out=False)
    categories = category_pagination.items
    return render_template('main/forum.html', category_pagination=category_pagination, categories=categories, len=len)


@main.route('/forum/<topic_name>')
def topic(topic_name):
    return render_template('main/forum_discussion.html', topic_name=topic_name)


@main.route('/get_categories_page_on_forum/<page>', methods=['GET'])
def get_categories_page_on_forum(page):
    page = int(page)
    categories = Category.query.order_by().paginate(page, per_page=SEARCH_ITEMS_COUNT, error_out=False).items
    categories_topics = dict()
    for category in categories:
        topics_pagination = category.topics.order_by().paginate(1, per_page=SEARCH_ITEMS_COUNT, error_out=False)
        category_topics = [dict(id=topic.id, body=topic.body, cur_page=1, pages=topics_pagination.pages) for topic in topics_pagination.items]
        categories_topics[category.id] = copy.deepcopy(category_topics)
        
    return jsonify([dict(id=category.id, name=category.name, topics=topics, topics_count=len(topics)) for category, topics in zip(categories, categories_topics.values())])


@main.route('/search_category_on_forum', methods=['POST'])
def search_category_on_forum():
    category_name = str(request.form.get('category_name')).strip().lower()
    found_category = Category.query.filter(Category.name.like("%{}%".format(category_name))).first()
    if found_category:
        page = 1; cur_page_items = list()
        while True:
            cur_page_items = Category.query.order_by().paginate(page, per_page=SEARCH_ITEMS_COUNT, error_out=False).items
            if found_category in cur_page_items:
                break
            page += 1
              
        categories_topics = dict()
        for category in cur_page_items:
            topics_pagination = category.topics.order_by().paginate(1, per_page=SEARCH_ITEMS_COUNT, error_out=False)
            category_topics = [dict(id=topic.id, body=topic.body, cur_page=1, pages=topics_pagination.pages) for topic in topics_pagination.items]
            categories_topics[category.id] = copy.deepcopy(category_topics)
        return jsonify([dict(result=True, id_of_found_elem=found_category.id, id=cur_page_category.id, name=cur_page_category.name, topics=topics, topics_count=len(topics)) for cur_page_category, topics in zip(cur_page_items, categories_topics.values())])
    else:
        return jsonify([dict(result=False)])
        
   