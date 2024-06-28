import bcrypt
import jwt
import datetime
import falcon

# Mock database
users_db = {}

class User:

    def __init__(self, config):
        self.config = config

    @staticmethod
    def hash_password(password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password, hashed):
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

    def create_user(self, username, password):
        if username in users_db:
            raise ValueError('User already exists')
        users_db[username] = {
            'username': username,
            'password': self.hash_password(password)
        }


    def authenticate_user(self, username, password):
        user = users_db.get(username)
        if not user or not self.verify_password(password, user['password']):
            raise ValueError('Invalid username or password')
        return self.generate_token(username)


    def generate_token(self, username):
        payload = {
            'sub': username,
            'iat': datetime.datetime.utcnow(),
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        return jwt.encode(payload, self.config.secret_key, algorithm='HS256')


    def decode_token(self, token):
        try:
            payload = jwt.decode(token, self.config.secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise falcon.HTTPUnauthorized('Token expired')
        except jwt.InvalidTokenError:
            raise falcon.HTTPUnauthorized('Invalid token')
