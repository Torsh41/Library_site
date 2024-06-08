from flask_socketio import emit, join_room, leave_room
from .. import socketio
from app.main import ELEMS_COUNT, months_dict, MAX_INVITATIONS_PER_CHAT
from app import database
from app.models import User, PrivateChatPost, PrivateChat, ChatInvitation
from flask_login import current_user, login_required
from app.decorators import check_actual_password
from datetime import datetime


@socketio.on('join', namespace='/private_chat')
@login_required
@check_actual_password
def joined(message):
    room = int(message['room'])
    join_room(room)
    emit('status', {"result": True}, to=room)


@socketio.on('send post', namespace='/private_chat')
@login_required
@check_actual_password
def add_post(msg):
    room = int(msg['chat_id'])
    chat = PrivateChat.query.filter_by(id=msg['chat_id']).first()
    if msg['filename'] != '':
        post = PrivateChatPost(body=str(msg['post_body']).strip().replace(
            "'", ""), edited=False, user=current_user, private_chat=chat, file=msg['screenshot'])
    else:
        post = PrivateChatPost(body=str(msg['post_body']).strip().replace(
            "'", ""), edited=False, user=current_user, private_chat=chat, file=bytes(False))
    if post_id_for_answer := msg['post_id_to_answer']:
        post.answer_to_post = post_id_for_answer
    else:
        post.answer_to_post = 0
    database.session.add(post)
    database.session.commit()
    posts_for_pagi = chat.posts.all()
    last_page = len(posts_for_pagi) // ELEMS_COUNT
    if len(posts_for_pagi) % ELEMS_COUNT > 0:
        last_page += 1
    posts_pagination = chat.posts.order_by(PrivateChatPost.id).paginate(last_page, per_page=ELEMS_COUNT, error_out=False)
    pages_count = list(posts_pagination.iter_pages())
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            if post.answer_to_post:
                post_from = chat.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date(
                    ).month], post_year=str(post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                    post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
        else:
            if post.answer_to_post:
                post_from = chat.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, basic_post_exist=True, base_id=post_from.id, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date(
                    ).month], post_year=str(post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
                else:
                    posts.append(dict(this_is_answer=True, basic_post_exist=False, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))
            else:
                posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), chat_id=chat.id, cur_page=posts_pagination.page, pages_count=pages_count, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                    post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender, edited=post.edited))

    return emit('add post', {'data': posts}, to=room)
    
    
@socketio.on('del post', namespace='/private_chat')
@login_required
@check_actual_password
def post_delete(data):
    page = int(data['page']); chat_id = data['chat_id']; room = int(chat_id)
    chat = PrivateChat.query.filter_by(id=int(chat_id)).first()
    post = chat.posts.filter_by(id=int(data['post_id'])).first()
    database.session.delete(post)
    database.session.commit()
    if users_posts := chat.posts.all():
        has_elems = True
        posts_pagination = chat.posts.order_by(PrivateChatPost.id).paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages_count = list(posts_pagination.iter_pages())
        if not posts_pagination.items:
            page -= 1
    else:
        page = 1
        pages_count = [1]
        has_elems = False
    response = dict(cur_page=page, pages_count=pages_count, has_elems=has_elems, posts_count=len(users_posts)); 
    return emit('del post response', {'response': response, 'chat_id': chat_id, 'post_id': data['post_id']}, to=room)


@socketio.on('edit post', namespace='/private_chat')
@login_required
@check_actual_password
def edit_post(data):
    room = int(data['chat_id'])
    post = PrivateChatPost.query.filter_by(id=data['post_id']).first()
    post.body = str(data['new_post']).strip().replace("'", "")
    post.timestamp = datetime.now()
    post_date = str(post.timestamp.date().day) + " " + months_dict[post.timestamp.date().month] + " " + str(post.timestamp.date().year)
    post.edited = True
    database.session.add(post)
    database.session.commit()
    return emit('edit post response', {'chat_id': data['chat_id'], 'post_id': data['post_id'], 'post_body': post.body, 'post_date': post_date, 'username': current_user.username}, to=room)


@socketio.on('get invite', namespace='/private_chat')
@login_required
@check_actual_password
def invite(data):
    chat_invitations_count = PrivateChat.query.filter_by(id=int(data['chat_id'])).first().invitations.count()
    room = int(data['chat_id'])
    if chat_invitations_count >= MAX_INVITATIONS_PER_CHAT:
        return emit('invitation', {'result': False}, to=room)
    new_user = User.query.filter_by(id=int(data['user_id'])).first()
    invitation = ChatInvitation(user=new_user, private_chat=PrivateChat.query.filter_by(id=int(data['chat_id'])).first())
    database.session.add(invitation)
    database.session.commit()
    return emit('invitation', {'result': True, 'new_user_name': new_user.username}, to=room)


@socketio.on('leave chat', namespace='/private_chat')
@login_required
@check_actual_password
def leave_chat(data):
    invitation = ChatInvitation.query.filter_by(user_id=current_user.id).filter_by(private_chat_id=int(data['chat_id'])).first()
    database.session.delete(invitation)
    database.session.commit()
    room = int(data['chat_id'])
    leave_room(room)
    return emit('left', {'result': True, 'username': current_user.username}, to=room)