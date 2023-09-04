import unittest
from db import db, User
from datetime import datetime, timedelta

# ... [rest of your code]

class AuthTestCase(unittest.TestCase):

    # ... [rest of your methods]

    def test_account_lockout_after_multiple_incorrect_attempts(self):
        self.register('testuser', 'testpassword', 'testpassword')
        
        # Attempt to login with wrong password 10 times
        for _ in range(10):
            response = self.login('testuser', 'wrongpassword')
        
        # Now, after the 10th attempt, it should say it's locked out
        response = self.login('testuser', 'wrongpassword')
        self.assertIn(b'Too many failed login attempts. Try again in 5 minutes.', response.data)

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

    # ... [rest of your methods]