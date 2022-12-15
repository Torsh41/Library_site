from . import personal
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, make_response
from .forms import EditProfileForm, AddListForm, AddNewBookForm
from ..begin_to_app import database
from app.models import User, Cataloge, Book, Item, BookGrade


@personal.route('/<username>/edit-profile/edit-avatar')
@login_required
def avatar(username):
    user = User.query.filter_by(username=username).first()
    avatar = make_response(user.avatar)
    return avatar
    
    
@personal.route('/<username>')
@login_required
def person(username):
    user = User.query.filter_by(username=username).first()
    catalogues = Cataloge.query.filter_by(user_id=user.id).all()
    return render_template('personal/user_page.html', user=user, catalogues=catalogues)


@personal.route('/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
def edit(username):
    form = EditProfileForm()
    if form.validate_on_submit():  
        if request.files['avatar']:
            current_user.avatar = bytes(request.files['avatar'].read())
        current_user.city = form.city.data
        current_user.gender = str(request.form.get('gender'))
        current_user.age = form.age.data
        current_user.about_me = form.description.data
        database.session.add(current_user._get_current_object())
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('personal/edit_user_page_profile.html', form=form)


@personal.route('/<username>/add-list', methods=['GET', 'POST'])
@login_required
def add_list(username):
    form = AddListForm()
    if form.validate_on_submit():
        cataloge = Cataloge(name=form.list_name.data, user=current_user._get_current_object())
        database.session.add(cataloge)
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('personal/add_list.html', form=form)


@personal.route('/<username>/add-new-book', methods=['GET', 'POST'])
@login_required
def add_new_book(username):
    form = AddNewBookForm()
    if form.validate_on_submit():
        genre = request.form.getlist('genres')
        genre_ = ''
        for value in genre:
            genre_ += str(value) + '  '
            
        book = Book(isbn=form.isbn.data, name=str(form.name.data).strip(), author=str(form.author.data).strip(), publishing_house=str(form.publishing_house.data).strip(), \
                    description=form.description.data, release_date=form.release_date.data, count_of_chapters=form.chapters_count.data, \
                    genre=genre_, user=current_user._get_current_object())
        database.session.add(book)
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('personal/add_book.html', form=form)


@personal.route('/<username>/add-book-in-list/<book_id>')
@login_required
def add_book_in_list_tmp(username, book_id):
    user = User.query.filter_by(username=username).first()
    catalogues = Cataloge.query.filter_by(user_id=user.id).all()
    return render_template('personal/user_page_add_book.html', username=username, book_id=book_id, catalogues=catalogues)


@personal.route('/<username>/add-book-in-list/<list_id>/<book_id>', methods=['GET', 'POST'])
@login_required
def add_book_in_list(username, list_id, book_id):
    cataloge = Cataloge.query.filter_by(id=list_id).first()
    book = Book.query.filter_by(id=book_id).first()
    flag = False
    if cataloge:
        for item_ in cataloge.items:
            if book.name == item_.book.name:
                flag = True
                
    if flag is False: 
        item = Item(read_state='unknown', book=book, cataloge=cataloge)     
        database.session.add(item)
        database.session.commit()
    return redirect(url_for('.person', username=username))

