import os
from app.begin_to_app import create_app
#from flask_script import Manager
#manager = Manager(app)
application = create_app(os.getenv('FLASK_CONFIG') or 'default')
if __name__ == '__main__':    
    application.run(debug=True)
    
 
