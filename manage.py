import os
from app import create_app, socketio


app = create_app(os.getenv('FLASK_CONFIG') or 'production')
if __name__ == '__main__':    
    socketio.run(debug=False, app=app)
    
 
