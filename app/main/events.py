from flask_socketio import emit
from app.begin_to_app import socketio
from app.init import database
from app.models import User, TopicPost, DiscussionTopic
from flask_login import current_user, login_required
from app.decorators import check_actual_password
ELEMS_COUNT = 10
months_dict = {
    1: 'января',
    2: 'февраля',
    3: 'марта',
    4: 'апреля',
    5: 'мая',
    6: 'июня',
    7: 'июля',
    8: 'августа',
    9: 'сентября',
    10: 'октября',
    11: 'ноября',
    12: 'декабря'
}


@socketio.on('send post')
@login_required
@check_actual_password
def add_post(msg):
    topic = DiscussionTopic.query.filter_by(id=msg['topic_id']).first()
    if msg['filename'] != '':
        post = TopicPost(body=str(msg['post_body']).strip().replace(
            "'", ""), user=current_user, topic=topic, file=msg['screenshot'])
    else:
        post = TopicPost(body=str(msg['post_body']).strip().replace(
            "'", ""), user=current_user, topic=topic, file=bytes(False))
    if post_id_for_answer := msg['post_id_to_answer']:
        post.answer_to_post = post_id_for_answer
    else:
        post.answer_to_post = 0
    database.session.add(post)
    database.session.commit()
    posts_for_pagi = topic.posts.all()
    last_page = len(posts_for_pagi) // ELEMS_COUNT
    if len(posts_for_pagi) % ELEMS_COUNT > 0:
        last_page += 1
    posts_pagination = topic.posts.order_by().paginate(
        last_page, per_page=ELEMS_COUNT, error_out=False)
    posts = list()
    for post in posts_pagination.items:
        user = User.query.filter_by(id=post.user_id).first()
        if post.file:
            if post.answer_to_post:
                post_from = topic.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date(
                    ).month], post_year=str(post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
                else:
                    posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
            else:
                posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=True, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                    post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
        else:
            if post.answer_to_post:
                post_from = topic.posts.filter_by(
                    id=post.answer_to_post).first()
                if post_from:
                    posts.append(dict(this_is_answer=True, username_of_post_from=post_from.user.username, body_of_post_from=post_from.body, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date(
                    ).month], post_year=str(post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
                else:
                    posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                        post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))
            else:
                posts.append(dict(this_is_answer=False, posts_count=len(posts_for_pagi), topic_id=topic.id, cur_page=posts_pagination.page, pages=posts_pagination.pages, id=post.id, body=post.body, file=False, post_day=str(post.timestamp.date().day), post_month=months_dict[post.timestamp.date().month], post_year=str(
                    post.timestamp.date().year), username=user.username, user_day=str(user.timestamp.date().day), user_month=months_dict[user.timestamp.date().month], user_year=str(user.timestamp.date().year), city=user.city, age=user.age, about_me=user.about_me, gender=user.gender))

    return emit('add post', {'data': posts}, broadcast=True)
    
    
@socketio.on('del post')
@login_required
@check_actual_password
def post_delete(data):
    page = int(data['page']); topic_id = data['topic_id']
    post = TopicPost.query.filter_by(id=int(data['post_id'])).first()
    database.session.delete(post)
    database.session.commit()
    topic = DiscussionTopic.query.filter_by(id=int(topic_id)).first()
    if users_posts := topic.posts.all():
        has_elems = True
        posts_pagination = topic.posts.order_by().paginate(page, per_page=ELEMS_COUNT, error_out=False)
        pages = posts_pagination.pages
        if not posts_pagination.items:
            page -= 1
    else:
        page = 1
        pages = 1
        has_elems = False
    response = dict(cur_page=page, pages=pages, has_elems=has_elems, posts_count=len(users_posts)); 
    return emit('del post response', {'response': response, 'topic_id': topic_id, 'post_id': data['post_id']}, broadcast=True)
