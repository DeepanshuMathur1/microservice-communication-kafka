import unittest
from app import app

class OrderServiceTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_place_order_success(self):
        response = self.app.post('/order', json={'item_id': 'item1', 'quantity': 1})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Order placed successfully', str(response.data))

    def test_place_order_invalid_format(self):
        response = self.app.post('/order', json={'item': 'item1', 'amount': 1})
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid order format', str(response.data))

if __name__ == '__main__':
    unittest.main()
