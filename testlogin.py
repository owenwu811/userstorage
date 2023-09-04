import unittest
from app import app, db, User
class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_user_credentials.db'
        with app.app_context():
            db.create_all()

    def register(self, username, password, confirm_password):
        return self.client.post('/register', data=dict(
            username=username, password=password, confirm_password=confirm_password
        ), follow_redirects=True)

    def login(self, username, password):
        return self.client.post('/login', data=dict(
            username=username, password=password
        ), follow_redirects=True)

    def test_valid_login(self):
        
        self.register('testuser', 'testpassword', 'testpassword')
        
        # Now, try logging in
        response = self.login('testuser', 'testpassword')
        self.assertIn(b'Welcome to Our Website, testuser!', response.data)

    # Other cleanup or tests ...

    def tearDown(self):
        with app.app_context():
            db.drop_all()

if __name__ == "__main__":
    unittest.main()

