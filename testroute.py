import unittest
from app import app

class TestWelcomeRoute(unittest.TestCase):

    def setUp(self):
        # Create a test client
        self.app = app.test_client()
        # Propagate the exceptions to the test client
        self.app.testing = True 

    def test_welcome_status_code(self):
        # Sends an HTTP GET request to the application
        # on the specified path
        response = self.app.get('/')

        # Assert the status code of the response
        self.assertEqual(response.status_code, 200)

    def test_welcome_content(self):
        response = self.app.get('/')

        # Ensure the response contains the desired content
        self.assertIn(b'Welcome to our site!', response.data)
        self.assertIn(b'Login', response.data)

if __name__ == "__main__":
    unittest.main()
