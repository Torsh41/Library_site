import os
from app.begin_to_app import create_app
#from flask_script import Manager
application = create_app(os.getenv('FLASK_CONFIG') or 'default')
#manager = Manager(app)
#with application.app_context():
    #database.create_all()

if __name__ == '__main__':    
    application.run(debug=True, port=8000, host='127.0.0.1')
 