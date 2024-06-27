import bcrypt
import jwt
import datetime

# Mock database
users_db = {}

SECRET_KEY = 'your_secret_key'

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def create_user(username, password):
    if username in users_db:
        raise ValueError('User already exists')
    users_db[username] = {
        'username': username,
        'password': hash_password(password)
    }

def authenticate_user(username, password):
    user = users_db.get(username)
    if not user or not verify_password(password, user['password']):
        raise ValueError('Invalid username or password')
    return generate_token(username)

def generate_token(username):
    payload = {
        'sub': username,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm='HS256')

def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['sub']
    except jwt.ExpiredSignatureError:
        raise falcon.HTTPUnauthorized('Token expired')
    except jwt.InvalidTokenError:
        raise falcon.HTTPUnauthorized('Invalid token')