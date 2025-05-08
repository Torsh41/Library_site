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
        self.assertEqual(response.status_code, 200, msg=errmsg)

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

    def test_login(self):
        response = self.client.get("/auth/login")
        errmsg = "Error: unable to reach /auth/login page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_logout(self):
        response = self.client.get("/auth/logout")
        errmsg = "Error: unable to reach /auth/logout page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_register(self):
        response = self.client.get("/auth/register")
        errmsg = "Error: unable to reach /auth/register page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_confirm_token(self):
        response = self.client.get("/auth/confirm/insert_a_csrf_token_here")
        errmsg = "Error: unable to reach /auth/confirm/<token> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_unconfirmed(self):
        response = self.client.get("/auth/unconfirmed")
        errmsg = "Error: unable to reach /auth/unconfirmed page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_confirm(self):
        response = self.client.get("/auth/confirm")
        errmsg = "Error: unable to reach /auth/confirm page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)


class MainPagesTest(unittest.TestCase):
    """Check if pages defined inside main module are reachable."""
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Main Page Reachability Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()
        _ = cls.test_user.login(cls.client)

    def test_get_cover(self):
        response = self.client.get("/1/get-cover")
        errmsg = "Error: unable to reach /<int:book_id>/get-cover page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_post_screenshot(self):
        response = self.client.get("/1/get-post-screenshot")
        errmsg = "Error: unable to reach /<post_id>/get-post-screenshot page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_post_screenshot_on_private_chat(self):
        response = self.client.get("/1/get-post-screenshot-on-private-chat")
        errmsg = "Error: unable to reach /<post_id>/get-post-screenshot-on-private-chat page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_index(self):
        response = self.client.get("/")
        errmsg = "Error: unable to reach index page (route='/')."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_book_page(self):
        response = self.client.get("/book-page/1")
        errmsg = "Error: unable to reach /book-page/<int:book_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_comments_page(self):
        response = self.client.get("/get_comments_page/1/1")
        errmsg = "Error: unable to reach /get_comments_page/<int:book_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_add_comment(self):
        response = self.client.get("/1/1/add_comment")
        errmsg = "Error: unable to reach /<username>/<int:book_id>/add_comment page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_edit_comment(self):
        response = self.client.get("/1/1/edit-comment/1")
        errmsg = "Error: unable to reach /<username>/<int:book_id>/edit-comment/<int:comment_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_give_grade(self):
        response = self.client.get("/1/give-grade/1")
        errmsg = "Error: unable to reach /<username>/give-grade/<int:book_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_delete_comment(self):
        response = self.client.get("/1/1/delete-comment/1/1")
        errmsg = "Error: unable to reach /<username>/<int:book_id>/delete-comment/<int:comment_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_categories(self):
        response = self.client.get("/categories")
        errmsg = "Error: unable to reach /categories page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_categories_page(self):
        response = self.client.get("/get_categories_page/1")
        errmsg = "Error: unable to reach /get_categories_page/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_category(self):
        response = self.client.get("/category/1")
        errmsg = "Error: unable to reach /category/<int:id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_category_search(self):
        response = self.client.get("/category/1/search")
        errmsg = "Error: unable to reach /category/<int:id>/search page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum(self):
        response = self.client.get("/forum")
        errmsg = "Error: unable to reach /forum page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_with_id(self):
        response = self.client.get("/forum/1")
        errmsg = "Error: unable to reach /forum/<int:topic_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_categories_page_on_forum(self):
        response = self.client.get("/get_categories_page_on_forum/1")
        errmsg = "Error: unable to reach /get_categories_page_on_forum/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_posts_page(self):
        response = self.client.get("/get_posts_page/1/1")
        errmsg = "Error: unable to reach /get_posts_page/<int:topic_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_search_category_on_forum(self):
        response = self.client.get("/search_category_on_forum")
        errmsg = "Error: unable to reach /search_category_on_forum page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_add_topic(self):
        response = self.client.get("/1/1/add_topic")
        errmsg = "Error: unable to reach /<username>/<int:category_id>/add_topic page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_topics_page_on_forum(self):
        response = self.client.get("/get_topics_page_on_forum/1/1")
        errmsg = "Error: unable to reach /get_topics_page_on_forum/<int:category_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_delete_topic(self):
        response = self.client.get("/delete-topic/1/1/1")
        errmsg = "Error: unable to reach /delete-topic/<int:category_id>/<int:topic_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining(self):
        response = self.client.get("/books-maintaining")
        errmsg = "Error: unable to reach /books-maintaining page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining_add_file(self):
        response = self.client.get("/books-maintaining/add-file")
        errmsg = "Error: unable to reach /books-maintaining/add-file page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining_search(self):
        response = self.client.get("/books-maintaining/search")
        errmsg = "Error: unable to reach /books-maintaining/search page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining_get_page(self):
        response = self.client.get("/books-maintaining/get-page/1")
        errmsg = "Error: unable to reach /books-maintaining/get-page/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining_change_count(self):
        response = self.client.get("/books-maintaining/change-count")
        errmsg = "Error: unable to reach /books-maintaining/change-count page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_books_maintaining_del_book(self):
        response = self.client.get("/books-maintaining/del-book")
        errmsg = "Error: unable to reach /books-maintaining/del-book page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_create_private_chat(self):
        response = self.client.get("/forum/create_private_chat")
        errmsg = "Error: unable to reach /forum/create_private_chat page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_private_chats(self):
        response = self.client.get("/forum/private_chats")
        errmsg = "Error: unable to reach /forum/private_chats page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_delete_private_chat(self):
        response = self.client.get("/forum/delete_private_chat/1/1")
        errmsg = "Error: unable to reach /forum/delete_private_chat/<int:chat_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_get_chats_page(self):
        response = self.client.get("/forum/get_chats_page/1")
        errmsg = "Error: unable to reach /forum/get_chats_page/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_private_chat_with_id(self):
        response = self.client.get("/forum/private_chat/1")
        errmsg = "Error: unable to reach /forum/private_chat/<int:chat_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_posts_page_on_chat_disc(self):
        response = self.client.get("/get_posts_page_on_chat_disc/1/1")
        errmsg = "Error: unable to reach /get_posts_page_on_chat_disc/<int:chat_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_forum_get_users_page_to_invite(self):
        response = self.client.get("/forum/private_chat/1/get_users_page_to_invite/1")
        errmsg = "Error: unable to reach /forum/private_chat/<int:chat_id>/get_users_page_to_invite/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_change_topic_name(self):
        response = self.client.get("/change-topic-name/1/1")
        errmsg = "Error: unable to reach /change-topic-name/<int:category_id>/<int:topic_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)


class AdminPagesTest(unittest.TestCase):
    """Check if pages defined inside admin module are reachable."""
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Admin Page Reachability Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()
        _ = cls.test_user.login(cls.client)

    def test_admin_panel(self):
        response = self.client.get("/admin/<username>/admin_panel")
        errmsg = "Error: unable to reach /admin/<username>/admin_panel page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_admin_panel_user_search(self):
        response = self.client.get("/admin/<username>/admin_panel/user_search")
        errmsg = "Error: unable to reach /admin/<username>/admin_panel/user_search page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_user_search_page(self):
        response = self.client.get("/admin/get_user_search_page/1")
        errmsg = "Error: unable to reach /admin/get_user_search_page/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_get_category_search_page(self):
        response = self.client.get("/admin/<username>/get_category_search_page/1")
        errmsg = "Error: unable to reach /admin/<username>/get_category_search_page/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_add_category(self):
        response = self.client.get("/admin/<username>/add-category")
        errmsg = "Error: unable to reach /admin/<username>/add-category page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_admin_paneluser_delete(self):
        response = self.client.get("/admin/admin_panel/user_delete/1/1")
        errmsg = "Error: unable to reach /admin/admin_panel/user_delete/<int:user_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_category_delete(self):
        response = self.client.get("/admin/<username>/category_delete/1/1")
        errmsg = "Error: unable to reach /admin/<username>/category_delete/<int:category_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_search_books_on_admin_panel(self):
        response = self.client.get("/admin/<username>/search_books_on_admin_panel/1")
        errmsg = "Error: unable to reach /admin/<username>/search_books_on_admin_panel/<int:category_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_del_book(self):
        response = self.client.get("/admin/<username>/del_book/1/1/1")
        errmsg = "Error: unable to reach /admin/<username>/del_book/<int:category_id>/<int:book_id>/<int:page> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)

    def test_change_book_info(self):
        response = self.client.get("/admin/<username>/change_book_info/1")
        errmsg = "Error: unable to reach /admin/<username>/change_book_info/<int:book_id> page."
        self.assertNotEqual(response.status_code, 404, msg=errmsg)


