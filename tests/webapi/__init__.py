import unittest
from app.models import User, Role
from app import database as db


app = None


def main_(app_):
    global app
    app = app_
    suite = unittest.defaultTestLoader.discover(".", pattern="webapi_test_*.py")
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
    return app.test_client(use_cookies=True)

def extract_csrf_token(html: str) -> str:
    """Read html DOM to find element with id=csrf_token, and extract it's value.
    Input parameter should be of type String.
    Outputs a CSRF token of type string.
    """
    dom_element = html.find("id=\"csrf_token\"")
    token_start = html.find("value=\"", dom_element) + len("value=\"")
    token_end = html.find("\"", token_start)
    csrf_token = html[token_start:token_end]
    return csrf_token

