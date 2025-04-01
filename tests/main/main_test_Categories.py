import unittest
from . import *

class UserModelTestCase(unittest.TestCase):
    def test_categories_page(self):
        client = get_app_test_client()
        response = client.get('/categories')
        self.assertEqual(response.status_code, 200)
    
    def test_category_page(self):
        client = get_app_test_client()
        response = client.get('/categories/category/МХТП')
        self.assertEqual(response.status_code, 200)
         
         
if __name__ == '__main__':
    unittest.main_()


