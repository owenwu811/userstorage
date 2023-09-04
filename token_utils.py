import jwt
from datetime import datetime, timedelta

SECRET_KEY = "."  # Consider using a stronger key

def generate_reset_token(email):
    payload = {
        'email': email,
        'exp': datetime.utcnow() + timedelta(hours=1)  # Token is valid for 1 hour
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_reset_token(token):
    try:
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded_token['email']
    except jwt.ExpiredSignatureError:
        return None  # Token has expired
    except jwt.InvalidTokenError:
        return None  # Invalid token