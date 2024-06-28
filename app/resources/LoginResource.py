from .Resource import Resource
import falcon
from ..models import authenticate_user

class LoginResource(Resource):
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