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
    page = request.args.get('page', 1, type=int)
    pagination = user.catalogues.order_by().paginate(page, per_page=2, error_out=False)
    catalogues = pagination.items
    return render_template('personal/user_page.html', user=user, catalogues=catalogues, pagination=pagination, len=len)


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
        cataloge = Cataloge(name=str(form.list_name.data).strip().lower(), user=current_user._get_current_object())
        database.session.add(cataloge)
        database.session.commit()
        return redirect(url_for('.person', username=username, page=request.args.get('page')))
    return render_template('personal/add_list.html', form=form)


@personal.route('/<username>/add-new-book', methods=['GET', 'POST'])
@login_required
def add_new_book(username):
    form = AddNewBookForm()
    if form.validate_on_submit():
        genre = request.form.getlist('genres')
        genre_ = ''
        for value in genre:
            genre_ += str(value) + ' '
            
        book = Book(isbn=form.isbn.data, name=str(form.name.data).strip().lower(), author=str(form.author.data).strip().lower(), publishing_house=str(form.publishing_house.data).strip(), \
                    description=form.description.data, release_date=form.release_date.data, count_of_chapters=form.chapters_count.data, \
                    genre=genre_, user=current_user._get_current_object())
        database.session.add(book)
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('personal/add_book.html', form=form)


@personal.route('/<username>/add-book-in-list/<book_id>', methods=['POST'])
@login_required
def add_book_in_list_tmp(username, book_id):
    read_state = request.form.get('read_state')
    user = User.query.filter_by(username=username).first()
    catalogues = Cataloge.query.filter_by(user_id=user.id).all()
    return render_template('personal/user_page_add_book.html', username=username, book_id=book_id, catalogues=catalogues, read_state=read_state)


@personal.route('/<username>/add-book-in-list/<list_id>/<book_id>/<read_state>', methods=['GET', 'POST'])
@login_required
def add_book_in_list(username, list_id, book_id, read_state):
    cataloge = Cataloge.query.filter_by(id=list_id).first()
    book = Book.query.filter_by(id=book_id).first()
    flag = False
    if cataloge:
        for item_ in cataloge.items:
            if book.name == item_.book.name:
                flag = True
                
    if flag is False: 
        item = Item(read_state=str(read_state), book=book, cataloge=cataloge)     
        database.session.add(item)
        database.session.commit()
    return redirect(url_for('.person', username=username))


@personal.route('/<username>/delete-list/<list_id>')
@login_required
def list_delete(username, list_id):
    cataloge = Cataloge.query.filter_by(id=list_id).first()
    database.session.delete(cataloge)
    database.session.commit()
    return redirect(url_for('personal.person', username=username, page=request.args.get('page', type=int))) 


@personal.route('/<username>/delete-item/<item_id>')
@login_required
def item_delete(username, item_id):
    item = Item.query.filter_by(id=item_id).first()
    database.session.delete(item)
    database.session.commit()
    return redirect(url_for('personal.person', username=username, page=request.args.get('page', type=int))) 