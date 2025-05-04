import unittest
from . import *


class RegistrationTest(unittest.TestCase):
    def test_registration(self):
        """Testing registration of a new user"""
        client = get_app_test_client()
        response = client.post("/auth/register", data={
            "username": "some_user",
            "email": "random_email@some_mail.some_domain",
            "password": "123456"
        })
        self.assertEqual(response.status_code, 200)


class LoginTest(unittest.TestCase):
    def test_login(self):
        """Testing login of a user"""
        test_user = require_user_registration()
        client = get_app_test_client()
        response = client.post("/auth/login", data={
            "email": test_user.email,
            "password": get_test_user_password()
        })
        self.assertEqual(response.status_code, 200)


class PageReachablity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs before every test-method"""
        cls.test_user = require_user_registration()
        cls.client = get_app_test_client()
        # log in the test user
        response = cls.client.post("/auth/login", data={
            "email": cls.test_user.email,
            "password": get_test_user_password()
        })

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_categories_page(self):
        response = self.client.get("/categories")
        self.assertEqual(response.status_code, 200)

    def test_forum_page(self):
        response = self.client.get("/forum")
        self.assertEqual(response.status_code, 200)

    def test_private_chats_page(self):
        response = self.client.get("/forum/private_chats", follow_redirects=True)
        # Should contain a single redirect from /auth/login to /forum/private_chats
        self.assertEqual(len(response.history), 1)
        self.assertEqual(response.status_code, 200)

    def test_books_maintaining_page(self):
        response = self.client.get("/books-maintaining", follow_redirects=True)
        # Should contain a single redirect from /auth/login to /books-maintaining
        self.assertEqual(len(response.history), 1)
        self.assertEqual(response.status_code, 200)

    def test_user_page(self):
        response = self.client.get("/user/" + self.test_user.username, follow_redirects=True)
        # Should contain a single redirect from /auth/login to /user/<username>
        self.assertEqual(len(response.history), 1)
        self.assertEqual(response.status_code, 200)

    def test_edit_profile_page(self):
        response = self.client.get("/user/" + self.test_user.username, "/edit-profile", follow_redirects=True)
        # Should contain a single redirect from /auth/login to /user/<username>/edit-profile
        self.assertEqual(len(response.history), 1)
        self.assertEqual(response.status_code, 200)
        
    def test_admin_panel_page(self):
        response = self.client.get("/admin/" + self.test_user.username + "/admin_panel", follow_redirects=True)
        # Should contain a single redirect from /auth/login to /admin/<username>/admin_panel
        self.assertEqual(len(response.history), 1)
        self.assertEqual(response.status_code, 200)
        
