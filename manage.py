import os
from app import create_app, socketio
from app.models import *


app = create_app(os.getenv('FLASK_CONFIG') or 'production')
if __name__ == '__main__':    
    socketio.run(debug=True, app=app)
    
 
