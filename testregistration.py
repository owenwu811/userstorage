import unittest
from app import app, db, User  # Adjust the imports as per your setup

class AuthTestCase(unittest.TestCase):

    def setUp(self):
    # Set up the test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Set up test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user_credentials.db'
        with app.app_context():
            db.create_all()

    def register(self, username, password, confirm_password):
        return self.client.post('/register', data=dict(
            username=username, password=password, confirm_password=confirm_password
        ), follow_redirects=True)
    
    def test_valid_registration(self):
        response = self.register('testuser', 'testpassword', 'testpassword')
        self.assertIn(b'Login', response.data)


if __name__ == "__main__":
    unittest.main()