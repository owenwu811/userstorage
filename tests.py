import unittest
from app import app, db, User  # Adjust the imports as per your setup

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Set up test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user_credentials.db'
        db.create_all()

    def tearDown(self):
        # Clean up after each test
        db.session.remove()
        db.drop_all()

    def register(self, username, password, confirm_password):
        return self.client.post('/register', data=dict(
            username=username, password=password, confirm_password=confirm_password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username, password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_valid_registration(self):
        response = self.register('test', 'test_password', 'test_password')
        self.assertIn(b'Login', response.data)

    def test_valid_login(self):
        self.register('test', 'test_password', 'test_password')
        response = self.login('test', 'test_password')
        self.assertIn(b'Login successful', response.data)

    def test_logout(self):
        self.register('test', 'test_password', 'test_password')
        self.login('test', 'test_password')
        response = self.logout()
        self.assertIn(b'Login', response.data)

    # More tests can be added (e.g., invalid registrations, invalid logins, etc.)

if __name__ == "__main__":
    unittest.main()

