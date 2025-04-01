import unittest
from . import *
# from app.models import User



class RegistrationTest(unittest.TestCase):
    def test_registration(self):
        """Testing registration of a new user"""
        client = get_app_test_client()
        ret = client.post("/auth/register", data={
            "username": "some_user",
            "email": "talllep692@gmail.com",
            "password": "123456"
        })
        self.assertTrue(ret.status_code == 200, msg=f"Status code: {ret.status_code}")

class LoginTest(unittest.TestCase):
    def test_login(self):
        """Testing login of a user"""
        test_user = require_user_registration()
        client = get_app_test_client()
        ret = client.post("/auth/register", data={
            "email": test_user.email,
            "password": get_test_user_password()
        })
        self.assertTrue(ret.status_code == 200, msg=f"Status code: {ret.status_code}")
