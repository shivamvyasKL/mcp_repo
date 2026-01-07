"""Unit tests for the Test API"""
import unittest
import json
from app import app

class TestAPITestCase(unittest.TestCase):
    def setUp(self):
        """Set up test client"""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_home_endpoint(self):
        """Test the root endpoint"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)

    def test_health_check(self):
        """Test the health check endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

    def test_get_users(self):
        """Test getting all users"""
        response = self.client.get('/api/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('data', data)

    def test_get_user_by_id(self):
        """Test getting a specific user"""
        response = self.client.get('/api/users/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['id'], 1)

    def test_get_user_not_found(self):
        """Test getting a non-existent user"""
        response = self.client.get('/api/users/999')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_create_user(self):
        """Test creating a new user"""
        new_user = {
            "name": "Test User",
            "email": "test@example.com"
        }
        response = self.client.post(
            '/api/users',
            data=json.dumps(new_user),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['name'], 'Test User')

    def test_create_user_missing_fields(self):
        """Test creating a user with missing fields"""
        response = self.client.post(
            '/api/users',
            data=json.dumps({"name": "Test"}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

    def test_get_products(self):
        """Test getting all products"""
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertGreater(data['count'], 0)

    def test_get_product_by_id(self):
        """Test getting a specific product"""
        response = self.client.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])

    def test_get_time(self):
        """Test the time endpoint"""
        response = self.client.get('/api/time')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('timestamp', data)

    def test_echo_endpoint(self):
        """Test the echo endpoint"""
        test_data = {"message": "Hello, World!"}
        response = self.client.post(
            '/api/echo',
            data=json.dumps(test_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['echo'], test_data)

    def test_404_error(self):
        """Test 404 error handling"""
        response = self.client.get('/api/nonexistent')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertFalse(data['success'])

if __name__ == '__main__':
    unittest.main()
