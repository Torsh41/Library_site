import unittest
from app.models import User, Role
from app import database as db


app = None
# Define a test user
test_user_username = "AlexanderTheGreat"
test_user_email = "tsar@moskov.mvmvmvmvm"
test_user_password = "aaaaaaaaaaaaaaaaaaaaaaaa"
test_user = User(
    username=test_user_username.strip().replace("'", ""),
    email=test_user_email.strip().lower(),
    password=test_user_password,
    role=Role.ADMIN
)
# test_user.role = Role.USER


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

@with_app_context
def require_user_registration() -> User:
    """Get a registered user."""
    existing_user = db.session.execute(db.select(User).filter_by(username=test_user_username)).scalar_one_or_none()
    if existing_user is not None:
        return existing_user
    print(f"Registration - Test User:\n\tname='{test_user.username}', " +
          f"email='{test_user.email}', pwd={get_test_user_password()}'.")
    db.session.add(test_user)
    db.session.commit()
    return test_user

def get_app_test_client():
    """Get application client something to make http requests."""
    return app.test_client(use_cookies=True)

def get_test_user_password():
    return test_user_password
