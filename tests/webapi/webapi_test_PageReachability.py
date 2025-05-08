import unittest
# from werkzeug.test import Client, TestResponse
from app.models import Category, Book, User, Role
from app import database as db
from . import *
from .UserPrototype import UserPrototype, test_user, test_admin


class PersonalPagesTest(unittest.TestCase):
    """Check if pages defined inside personal module are reachable."""
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Personal Page Reachability Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()
        _ = cls.test_user.login(cls.client)
        # Ensure that at least one category and one book exist
        with app.app_context():
            category_name = "The Necessary Category"
            category = Category.query.filter_by(name=category_name).first()
            if category is None:
                category = Category(name = category_name)
            db.session.add(category)
            book_isbn = "9780590353427"
            book_name = "The Necessary Book"
            book = Book.query.filter_by(name=book_name).first()
            if book is None:
                book = Book(isbn = book_isbn, name = book_name)
            db.session.add(book)
            db.session.commit()

    def test_user_page(self):
        response = self.client.get("/user/" + self.test_user.name)
        errmsg = "Error: unable to reach /user/<username> page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_edit_profile(self):
        response = self.client.get("/user/" + self.test_user.name + "/edit-profile")
        errmsg = "Error: unable to reach /user/<username>/edit-profile page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_edit_avatar(self):
        response = self.client.get("/user/" + self.test_user.name + "/edit-profile/edit-avatar")
        errmsg = "Error: unable to reach /user/<username>/edit-profile/edit-avatar page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_add_list(self):
        response = self.client.post("/user/" + self.test_user.name + "/add-list")
        errmsg = "Error: unable to reach /user/<username>/add-list page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_get_lists(self):
        response = self.client.get("/user/" + self.test_user.name + "/get_lists_page/1")
        errmsg = "Error: unable to reach /user/<username>/get_lists_page/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_get_books(self):
        response = self.client.get("/user/" + self.test_user.name + "/get_books_page/1/1")
        errmsg = "Error: unable to reach /user/<username>/get_books_page/1/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_add_new_book(self):
        response = self.client.get("/user/" + self.test_user.name + "/add-new-book")
        errmsg = "Error: unable to reach /user/<username>/add-new-book page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_add_book_in_list_tmp(self):
        response = self.client.get("/user/" + self.test_user.name + "/add-book-in-list-tmp/1")
        errmsg = "Error: unable to reach /user/<username>/add-book-in-list-tmp/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_get_lists_page_to_add_book(self):
        response = self.client.get("/user/" + self.test_user.name + "/get_lists_page_to_add_book/1")
        errmsg = "Error: unable to reach /user/<username>/get_lists_page_to_add_book/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_add_book_in_list(self):
        response = self.client.get("/user/" + self.test_user.name + "/add-book-in-list/1/1/read_state")
        errmsg = "Error: unable to reach /user/<username>/add-book-in-list/1/1/read_state page."
        self.assertEqual(response.status_code, 302, msg=errmsg)

    def test_delete_list(self):
        response = self.client.get("/user/" + self.test_user.name + "/delete-list/1/1")
        errmsg = "Error: unable to reach /user/<username>/delete-list/1/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_delete_item(self):
        response = self.client.get("/user/" + self.test_user.name + "/delete-item/1/1/1")
        errmsg = "Error: unable to reach /user/<username>/delete-item/1/1/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_get_categories_page_for_book_adding(self):
        response = self.client.get("/user/" + self.test_user.name + "/get_categories_page_for_book_adding/1")
        errmsg = "Error: unable to reach /user/<username>//get_categories_page_for_book_adding/1 page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_delete_list(self):
        response = self.client.get("/user/change_read_state")
        errmsg = "Error: unable to reach /user/change_read_state page."
        self.assertEqual(response.status_code, 200, msg=errmsg)

    def test_delete_list(self):
        response = self.client.get("/user/add-books")
        errmsg = "Error: unable to reach /user/add-books page."
        self.assertEqual(response.status_code, 200, msg=errmsg)


class AuthPagesTest(unittest.TestCase):
    """Check if pages defined inside auth module are reachable."""
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Auth Page Reachability Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()
        _ = cls.test_user.login(cls.client)

    # def test_user_page(self):
    #     response = self.client.get("/user/" + self.test_user.name)
    #     errmsg = "Error: unable to reach /user/<username> page."
    #     self.assertEqual(response.status_code, 200, msg=errmsg)

