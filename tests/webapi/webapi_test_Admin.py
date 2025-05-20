import unittest
from app.models import Category, Role
from app import database as db
from . import *
from . import app
from .UserPrototype import test_user, test_admin


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


