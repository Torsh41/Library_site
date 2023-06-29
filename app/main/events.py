from flask_socketio import emit
from app.begin_to_app import socketio


@socketio.on('send post')
def add_post(post):
    return emit('response',  {'data': post['post_body']}, broadcast=True)
    # #return jsonify(posts)
    # return emit('response', {'data': posts}, broadcast=True)
    
    
@socketio.on('connect')
def test_connect():
    emit('response', {'data': 'Connected'})


@socketio.on('disconnect')
def test_disconnect():
    emit('response', 'Client disconnected')