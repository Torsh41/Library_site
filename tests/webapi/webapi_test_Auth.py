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


class PersonalModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Personal Module Funcionality Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_user.copy()

    def test_upload_book(self):
        """Test upload of one new book.
        """
        # User login
        response = self.test_user.login(self.client)
        errmsg = f"Error: unsuccessful login attempt."
        self.assertEqual(response.status_code, 302, msg=errmsg)
        # Create a new category
        with app.app_context():
            category_name = "A Category"
            category_name = str(category_name).strip().lower().replace("'", "")
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                category = Category(name = category_name)
            db.session.add(category)
            db.session.commit()
        # Extract CSRF token from the /admin/<username>/add-new-book page
        response = self.client.post("/user/" + self.test_user.name + "/add-new-book")
        csrf_token = extract_csrf_token(response.data.decode("utf-8"))
        errmsg = "Error: unsuccessful API call to /user/<username>/add-new-book"
        self.assertEqual(response.status_code, 200, msg=errmsg)
        # Create a "book"
        cover = b"An image binary"
        ISBN = "978-0-439-13636-5"
        title = "A book title"
        author = "An author"
        reference_url = "http://abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~:/?#[]@!$&'()*+,;%="
        publisher = "Publisher"
        description = "Very long and interesting description"
        release_date = "2025-05-14"
        chapter_count = "25"
        with app.app_context():
            book = Book.query.filter_by(isbn=ISBN).first()
            if book is not None:
                db.session.delete(book)
                db.session.commit()
        response = self.client.post("/user/" + self.test_user.name + "/add-new-book", data={
            "csrf_token": csrf_token,
            # "cover": cover,
            "isbn": ISBN,
            "name": title,
            "author": author,
            "publishing_house": publisher,
            "description": description,
            "release_date": release_date,
            "chapters_count": chapter_count,
            "category": category_name,
            "submit": "Добавить книгу в базу"
        })
        errmsg = "Error: unsuccessful API call to /user/<username>/add-new-book"
        self.assertEqual(response.status_code, 302, msg=errmsg)
        # Verify that the book was created
        with app.app_context():
            category = Category.query.filter_by(name=category_name).first()
            errmsg = "Error: unable to find previously created category by it's name"
            self.assertIsNotNone(category, msg=errmsg)
            book = Book.query.filter_by(isbn=ISBN).first()
            errmsg = "Error: book was not inserted into the database"
            self.assertIsNotNone(book, msg=errmsg)


class AdminModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Admin Module Funcionality Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()

    def test_add_category(self):
        """Test adding book category."""
        # User login
        response = self.test_user.login(self.client)
        errmsg = f"Error: unsuccessful login attempt."
        self.assertEqual(response.status_code, 302, msg=errmsg)
        # Extract CSRF token from the /admin/<username>/add-category page
        response = self.client.post("/admin/" + self.test_user.name + "/add-category")
        csrf_token = extract_csrf_token(response.data.decode("utf-8"))
        errmsg = "Error: unsuccessful API call to /admin/<username>/add-category"
        self.assertEqual(response.status_code, 200, msg=errmsg)
        # TODO: assert for CSRF token being correct/valid (TODO in other places as well)
        # Ensure that the category does not already exist
        category_name = "Another Category"
        category_name = str(category_name).strip().lower().replace("'", "")
        with app.app_context():
            category = Category.query.filter_by(name=category_name).first()
            if category is not None:
                db.session.delete(category)
                db.session.commit()
        # Create a category
        response = self.client.post("/admin/" + self.test_user.name + "/add-category", data={
            "csrf_token": csrf_token,
            "category_name": category_name
        })
        errmsg = "Error: unsuccessful API call to /admin/<username>/add-category"
        self.assertEqual(response.status_code, 302, msg=errmsg)
        # Verify that the category was created
        with app.app_context():
            category = Category.query.filter_by(name=category_name).first()
            errmsg = "Error: category was not inserted into the database"
            self.assertIsNotNone(category, msg=errmsg)

    def test_user_search(self):
        """Test an endpoint that returns JSON list of users"""
        import json
        user = test_user.copy()
        errmsg = ("Error: unsuccessful API call to /<username>/admin_panel/user_search; search_string=`{}`.")
        # Do an incorrect response
        search_string = ""
        response = self.client.post("/admin/" + self.test_user.name + "/admin_panel/user_search", data={
            "users_search_result": search_string
        })
        self.assertEqual(response.status_code, 200, msg=errmsg)
        self.assertEqual(json.loads(response.data)[0]["result"], False, msg=errmsg.format(search_string))
        # Get all users
        search_string = "*"
        response = self.client.post("/admin/" + self.test_user.name + "/admin_panel/user_search", data={
            "users_search_result": search_string
        })
        self.assertEqual(response.status_code, 200, msg=errmsg)
        self.assertEqual(json.loads(response.data)[0]["result"], True, msg=errmsg.format(search_string))
        # Search users by name
        search_string = "user"
        response = self.client.post("/admin/" + self.test_user.name + "/admin_panel/user_search", data={
            "users_search_result": search_string
        })
        self.assertEqual(response.status_code, 200, msg=errmsg)
        self.assertEqual(json.loads(response.data)[0]["result"], True, msg=errmsg.format(search_string))
        # Search users by email
        search_string = "@user"
        response = self.client.post("/admin/" + self.test_user.name + "/admin_panel/user_search", data={
            "users_search_result": search_string
        })
        self.assertEqual(response.status_code, 200, msg=errmsg)
        self.assertEqual(json.loads(response.data)[0]["result"], True, msg=errmsg.format(search_string))

        def test_set_user_role(self):
            user = UserPrototype("SetRoleTestUser", "Someemail@testuser.user", "123456", Role.ADMIN)
            # Ensure the user has ADMIN role
            with app.app_context():
                user.role = Role.by_id(Role.ADMIN)
                db.session.add(user)
                db.session.commit()
            # Set user role to USER
            response = self.client.get("/admin/admin_panel/set_user_role/" + user.id + "/" + Role.by_id(Role.USER).id)
            errmsg = "Error: unsuccessful API call to /admin/admin_panel/set_user_role/<user_id>/<role_id>"
            self.assertEqual(response.status_code, 200, msg=errmsg)
            # Sync user with database
            user = user.copy()
            errmsg = "Error: failed to set user role"
            self.assertEqual(user.role, Role.by_id(Role.USER).id, msg=errmsg)

