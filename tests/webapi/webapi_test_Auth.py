import unittest
from werkzeug.test import Client, TestResponse
from app.models import Category, Book, User, Role
from app import database as db
from . import *
from . import app
from .UserPrototype import UserPrototype, test_user, test_admin

from pprint import pprint

class AuthModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Auth Module Funcionality Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_user.copy()

    def test_registration(self):
        """Test user registration
        TODO: somwhere in this function, the global test_user is being
        dropped from the database. It's not fatal, but weird and annoying"""
        # Extract CSRF token from /auth/register page (the ugly way)
        response = self.client.post("/auth/register")
        csrf_token = extract_csrf_token(response.data.decode("utf-8"))
        # Delete user if already exists
        email = "somerandom@email.mmmmmmmmmmmmmm"
        username = "RegistrationUser"
        password = "gibberish"
        password2 = "gibberish"
        with app.app_context():
            existing_user = User.query.filter_by(email=email).first()
            if existing_user is not None:
                db.session.delete(existing_user)
                db.session.commit()
        # User registration
        response = self.client.post("/auth/register", data={
            "csrf_token": csrf_token,
            "email": email,
            "username": username,
            "password": password,
            "password2": password2
        })
        errmsg = f"Error: unsuccessful registration attempt."
        self.assertEqual(response.status_code, 302, msg=errmsg)

    def test_login(self):
        """Test user login"""
        response = self.test_user.login(self.client)
        errmsg = f"Error: unsuccessful login attempt."
        self.assertEqual(response.status_code, 302, msg=errmsg)
        errmsg = f"Error: response redirects to a different page, than /user/<username>."
        self.assertEqual(response.headers["Location"], "/user/" + self.test_user.name, msg=errmsg)

    # def test_logout(self):
    #     """Test user logout"""
    #     response = self.test_user.login(self.client)
    #     errmsg = f"Error: unsuccessful login attempt."
    #     self.assertEqual(response.status_code, 302, msg=errmsg)
    #     response = self.client.post("/auth/logout")
    #     pprint(response.__dict__)
    #     print(response.data.decode("utf-8"))
    #     errmsg = f"Error: unable to log out. (???)"
    #     self.assertEqual(response.status_code, 200, msg=errmsg)

    # def test_change_password(self):
    #     """Test user password change
    #     Requires an email server/client/something to recieve the csrf token
    #     to be able to do anything. In the TODO list."""
    #     pass


