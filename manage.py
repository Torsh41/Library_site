# import mimetypes
# mimetypes.add_type('text/javascript', '.js', True)
# mimetypes.add_type('text/css', '.css')
import os
from app.begin_to_app import create_app, socketio


application = create_app(os.getenv('FLASK_CONFIG') or 'default')
if __name__ == '__main__':    
    socketio.run(debug=True, app=application)
    
 
