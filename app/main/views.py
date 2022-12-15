from dataclasses import dataclass
from unicodedata import name
from . import main
from app.init import database
from app.models import User, BookGrade, Book
from flask import render_template, request, redirect, url_for
from app.main.sort import sorting
from app.main.forms import SearchForm
from flask_login import current_user, login_required


@main.route('/')
def index():
    return render_template('main/index.html')
 
'''
@main.route('/search/result/<search_result>/<form>')
def result(search_result, form):
    return render_template('main/search.html', form=form, search_result=search_result)
'''


@main.route('/search', methods=['GET', 'POST'])
def searching():
    '''
    Leonidus = User(email='leokazantsev19@mail.ru' , username='leo', password_hash="ddfdewcww", confirmed=1)
    deadly = Book(name='choppa', author='pidor', description="dsdfdwd", count_of_chapters=2, genre="zalupa", user=Leonidus)
    deadly_1 = Book(name='choppa666', author='pidor', description="dsdfdwddsq", count_of_chapters=1, genre="zalupa", user=Leonidus)
    database.session.add(Leonidus)
    database.session.add(deadly)
    database.session.commit()
    '''
    '''
    users = User.query.filter_by().all()
    rating_list = list()
    for user in users:
        rating_list.append([user.username, len(user.books), len(user.grades)])
    try:
        rating_list = sorting(rating_list, len(rating_list))
    except:
        pass
    '''
   
    if request.method == 'POST':
        search_result = Book.query.filter_by(name=str(request.form.get('search_result')).strip()).first()
        flag = False
        if not search_result:
            search_result = Book.query.filter_by(author=str(request.form.get('search_result')).strip()).all()
            flag = True
            if not search_result:
                search_result = 404
        return render_template('main/search.html', search_result=search_result, flag=flag)
    return render_template('main/search.html', search_result=0)


@main.route('/book-page/<name>')
def book_page(name):
    fin_grade = 0
    grade_count = 0
    book = Book.query.filter_by(name=name).first()
    grades = BookGrade.query.filter_by(book=book).all()
    book_grade_for_cur_user = BookGrade.query.filter_by(user=current_user, book=book).first()
    for value in grades:
        fin_grade += value.grade
        grade_count += 1
    if grade_count:    
        fin_grade = fin_grade / grade_count
    return render_template('main/book_page.html', book=book, str=str, fin_grade=fin_grade, book_grade_for_cur_user=book_grade_for_cur_user)


@main.route('/<username>/give-grade/<book_id>/<grade>') 
@login_required
def give_grade(username, book_id, grade):
    book = Book.query.filter_by(id=book_id).first()
    grade = BookGrade(grade=grade, user=current_user, book=book)
    database.session.add(grade)
    database.session.commit()
    return redirect(url_for('main.book_page', name=book.name))
    