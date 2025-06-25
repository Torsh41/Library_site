import unittest
from app.models import ModerationRequest, Role
from app import database as db
from . import *
from . import app
from .UserPrototype import UserPrototype, test_user, test_admin
from .CategoryPrototype import CategoryPrototype
from .BookPrototype import BookPrototype


class MainModuleTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs only during initialization of the test case"""
        print("\nLog : Running Main Module Funcionality Tests...")
        cls.client = get_app_test_client()
        cls.test_user = test_admin.copy()
        cls.category = CategoryPrototype(name="main module category")
        cls.category2 = CategoryPrototype(name="main module category2")
        cls.book_moderated_yes = BookPrototype(name="main module book moderation accepted",
                                  user_id=cls.test_user.get().id,
                                  category_id=cls.category.get().id,
                                  moderation_request_status=ModerationRequest.STATUS_ACCEPTED)
        cls.book_moderated_not = BookPrototype(name="main module book moderation rejected",
                                  user_id=cls.test_user.get().id,
                                  category_id=cls.category.get().id,
                                  moderation_request_status=ModerationRequest.STATUS_REJECTED)
        cls.book_moderated_idk = BookPrototype(name="asd",
                                  user_id=cls.test_user.get().id,
                                  category_id=cls.category.get().id,
                                  moderation_request_status=ModerationRequest.STATUS_OPEN)
    
    def test_category_page(self):
        """Test category page"""
        response = self.client.get("/category/" + str(self.category.get().id))
        errmsg = "Error: unsuccessful API call to /category/<int:category_id>."
        self.assertEqual(response.status_code, 200, msg=errmsg)


