from . import personal
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, request, make_response
from .forms import EditProfileForm, AddListForm
from ..begin_to_app import database
from app.models import User, Cataloge


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
    return render_template('user_page.html', user=user, catalogues=catalogues)


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
    return render_template('edit_user_page_profile.html', form=form)


@personal.route('/<username>/add-list', methods=['GET', 'POST'])
@login_required
def add_list(username):
    #form = AddListForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        cataloge = Cataloge(name=request.form.get('list_name'), user=current_user._get_current_object())
        database.session.add(cataloge)
        database.session.commit()
        return redirect(url_for('.person', username=username))
    return render_template('add_list.html')
   