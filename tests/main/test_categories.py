import unittest
from app.begin_to_app import create_app

class UserModelTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client(use_cookies=True)
        
    def test_categories_page(self):
        response = self.client.get('/categories')
        self.assertEqual(response.status_code, 200)
    
    def test_category_page(self):
        response = self.client.get('/categories/category/<name>', name='МХТП')
        self.assertEqual(response.status_code, 200)
         

       

if __name__ == '__main__':
    unittest.main()


