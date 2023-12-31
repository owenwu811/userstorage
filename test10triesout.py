import unittest
import re
from db import db, User
from datetime import datetime, timedelta
from app import app

# ... [rest of your code]

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        # Set up the test client
        self.client = app.test_client()
        
        # Set up an application context
        self.app_context = app.app_context()  # Create an application context
        self.app_context.push()  # Push the context
        
        app.config['TESTING'] = True

    def tearDown(self):
        # Pop the context after the test is done
        self.app_context.pop()  

    def test_account_lockout_after_multiple_incorrect_attempts(self):
        self.register('testuser', 'testpassword', 'testpassword')
        
        # Attempt to login with wrong password 10 times
        for _ in range(10):
            response = self.login('testuser', 'wrongpassword')
        
        # Now, after the 10th attempt, it should say it's locked out
        response = self.login('testuser', 'wrongpassword')
        
        # Use regex pattern to match the message structure
        pattern = re.compile(b'Too many failed login attempts. Try again in \d+ minutes.')
        self.assertTrue(pattern.search(response.data))

    def test_successful_login_after_lockout_expires(self):
        self.register('testuser', 'testpassword', 'testpassword')
        
        # Simulate account being locked out
        user = User.query.filter_by(username='testuser').first()
        user.locked_until = datetime.utcnow() + timedelta(minutes=5)
        db.session.commit()
        
        # Simulate time passing to after lockout duration
        user.locked_until = datetime.utcnow() - timedelta(minutes=1)
        db.session.commit()
        
        # Now, attempt to login with correct credentials
        response = self.login('testuser', 'testpassword')
        self.assertIn(b'Welcome to Our Website, testuser!', response.data)

    def register(self, username, password, confirm_password):
        # Your registration logic here. For example:
        return self.client.post('/register', data=dict(
            username=username, password=password, confirm_password=confirm_password
        ), follow_redirects=True)

    def login(self, username, password):
        # Your login logic here. For example:
        return self.client.post('/login', data=dict(
            username=username, password=password
        ), follow_redirects=True)

    # ... [rest of your methods]

if __name__ == "__main__":
    unittest.main()

