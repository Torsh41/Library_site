from . import personal
from flask_login import login_required
from flask import request, render_template, redirect

@personal.route('<username>')
@login_required
def person(username):
    '''
    if request.method == 'GET':
        return username
    else:
        return '!!!'
    '''
    return render_template('user_page.html', username=username)