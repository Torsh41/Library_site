import unittest
from app.models import Category, Book
from app import database as db
from . import *
from . import app
from .UserPrototype import test_user, test_admin

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


