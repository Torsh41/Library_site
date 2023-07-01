import os
from app.begin_to_app import create_app, socketio


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
if __name__ == '__main__':    
    socketio.run(debug=True, app=application)
    
 
