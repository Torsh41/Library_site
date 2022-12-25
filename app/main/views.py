from . import main
from app.init import database
from app.models import BookGrade, Book, Comment
from flask import render_template, request, redirect, url_for
from app.main.sort import sorting
from flask_login import current_user, login_required


@main.route('/')
def index():
    return render_template('main/index.html')
 

@main.route('/search', methods=['GET', 'POST'])
def searching():
    books = Book.query.all()
    date_list = list()
    for book in books:
        if not book.release_date in date_list:
            date_list.append(book.release_date)
        
    if request.method == 'POST':
        result = str(request.form.get('search_result')).strip().lower()
        if result == 'все':
            search_result = books
        else:
            release_date = request.form.get('release_date')
            if result and not release_date:
                search_result = Book.query.filter_by(name=result).first()
                search_result_ = Book.query.filter_by(author=result).all()
                
            elif result and release_date:
                search_result = Book.query.filter_by(name=result, release_date=release_date).first()
                search_result_ = Book.query.filter_by(author=result, release_date=release_date).all()
                
            elif not result and release_date:
                search_result = Book.query.filter_by(release_date=release_date).first()
                search_result_ = Book.query.filter_by(release_date=release_date).all()
            
            elif not result and not release_date:
                search_result = None
                search_result_ = []
                
            search_result_.append(search_result)
            search_result_fin = [] 
            [search_result_fin.append(value) for value in search_result_ if value not in search_result_fin]
            fin_result = list()
            for each in search_result_fin:
                if each:
                    fin_result.append(each)
            search_result = fin_result
            if not search_result:
                search_result = 404
                
        return render_template('main/search.html', search_result=search_result, date_list=date_list, len=len)
    return render_template('main/search.html', search_result=0, date_list=date_list, len=len)


@main.route('/book-page/<name>', methods=['GET', 'POST'])
def book_page(name):
    book = Book.query.filter_by(name=name).first()
    if request.method == 'POST' and request.form.get('comment') and current_user.is_authenticated:
        comment = Comment(body=request.form.get('comment'), book=book, user=current_user._get_current_object())
        database.session.add(comment)
        database.session.commit()
        return redirect(url_for('.book_page', name=book.name, page=-1))
    
    page = request.args.get('page', 1, type=int)
    if page == -1:
        page = round((book.comments.count() - 1) / 10 + 1, 1)
    
    pagination = book.comments.order_by(Comment.timestamp.asc()).paginate(page, per_page=10, error_out=False)
    comments = pagination.items
    
    if current_user.is_authenticated:
        book_grade_for_cur_user = BookGrade.query.filter_by(user=current_user._get_current_object(), book=book).first()
    else:
        book_grade_for_cur_user = 0
    
    fin_grade = 0
    grade_count = 0
    grades = BookGrade.query.filter_by(book=book).all()    
    for value in grades:
        fin_grade += value.grade
        grade_count += 1
    if grade_count:    
        fin_grade = round(fin_grade / grade_count, 1)
    return render_template('main/book_page.html', book=book, str=str, fin_grade=fin_grade, book_grade_for_cur_user=book_grade_for_cur_user, comments=comments, pagination=pagination, len=len)


@main.route('/<username>/give-grade/<book_id>/<grade>') 
@login_required
def give_grade(username, book_id, grade):
    book = Book.query.filter_by(id=book_id).first()
    grade = BookGrade(grade=grade, user=current_user, book=book)
    database.session.add(grade)
    database.session.commit()
    return redirect(url_for('main.book_page', name=book.name))


@main.route('/<username>/delete-comment/<comment_id>')  
@login_required
def comment_delete(username, comment_id):
    comment = Comment.query.filter_by(id=comment_id).first()
    book = comment.book
    database.session.delete(comment)
    database.session.commit()
    return redirect(url_for('main.book_page', name=book.name, page=request.args.get('page', type=int))) 