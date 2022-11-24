from dataclasses import dataclass
from unicodedata import name
from . import main
from app.init import database
from app.models import User, BookGrade, Book
from flask import render_template
from app.main.sort import sorting
from app.main.forms import SearchForm


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
 

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
     
    users = User.query.filter_by().all()
    rating_list = list()
    for user in users:
        rating_list.append([user.username, len(user.books), len(user.grades)])
    try:
        rating_list = sorting(rating_list, len(rating_list))
    except:
        pass
    
    form = SearchForm()
    if form.validate_on_submit():
        search_result = Book.query.filter_by(name=form.find_result.data).all()
        return render_template('search.html', rating_list=rating_list, search_result=search_result, form=form)
    return render_template('search.html', rating_list=rating_list, search_result=0, form=form)
 