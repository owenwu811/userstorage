import unittest
from app import app  # adjust the import to your actual file and app name

class LogoutTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the Flask test client
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.app = app.test_client()

    def test_logout(self):
        # Establish a user session
        with self.app.session_transaction() as session:
            session['username'] = 'testuser'
        
        # Make a request to the logout route
        response = self.app.get('/logout', follow_redirects=True)

        # Assert the user has been logged out
        with self.app.session_transaction() as session:
            self.assertIsNone(session.get('username'))
        
        # Assert that the response redirects to the login page
        self.assertIn(b'Login', response.data)  # Assuming your login page has the word "Login" in it

if __name__ == '__main__':
    unittest.main()