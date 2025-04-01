import unittest
from app import create_app


# TODO: This is only a template
# Create the application with testing enviroment
# app = create_app('testing')

def main_():
    suite = get_test_suite()
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)

def get_test_suite():
    suite = unittest.defaultTestLoader.discover(".", pattern="main_test_*.py")
    return suite

def with_app_context(func):
    """Helper decorator, to run a function within the app_context().
    Should be used, when a method needs to access the database.
    """
    def wrapper(*args, **kwargs):
        with app.app_context():
            return func(*args, **kwargs)
    return wrapper

