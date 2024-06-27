import falcon
from .models import create_user, authenticate_user


class UserResource:
    def on_post(self, req, resp):
        data = req.media
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise falcon.HTTPBadRequest(description='Username and password are required')

        try:
            create_user(username, password)
            resp.status = falcon.HTTP_201
            resp.media = {'message': 'User created successfully'}
        except ValueError as ex:
            raise falcon.HTTPConflict(description=str(ex))


class LoginResource:
    def on_post(self, req, resp):
        data = req.media
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise falcon.HTTPBadRequest(description='Username and password are required')

        try:
            token = authenticate_user(username, password)
            resp.media = {'token': token}
        except ValueError as ex:
            raise falcon.HTTPUnauthorized(description=str(ex))


class ProtectedResource:
    def on_get(self, req, resp):
        user = req.context.get('user')
        if not user:
            raise falcon.HTTPUnauthorized(description='Authentication required')

        resp.media = {'message': f'Hello, {user}!'}
