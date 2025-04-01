import unittest


# TODO: This is only a template
# Create the application with testing enviroment
# app = create_app('testing')
app = None

def main_(app_):
    global app
    app = app_
    suite = unittest.defaultTestLoader.discover(".", pattern="main_test_*.py")
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def with_app_context(func):
    """Helper decorator, to run a function within the app_context().
    Should be used, when a method needs to access the database.
    """
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

def get_app_test_client():
    """Get application client something to make http requests."""
    return app.test_client()

