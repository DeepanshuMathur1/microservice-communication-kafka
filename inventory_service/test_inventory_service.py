import unittest
from app import app, inventory

class InventoryServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_inventory(self):
        response = self.app.get('/inventory')
        self.assertEqual(response.status_code, 200)
        self.assertIn('item1', str(response.data))
        self.assertIn('item2', str(response.data))

if __name__ == '__main__':
    unittest.main()
