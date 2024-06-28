from .Resource import Resource
import falcon
from ..models import create_user


class UserResource(Resource):
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