import falcon
from .models import User


class JWTAuthMiddleware:

    def __init__(self, config):
        self.config = config

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        if token is None:
            return
        token = token.split(' ')[1]
        try:
            req.context['user'] = User(self.config).decode_token(token)
        except falcon.HTTPUnauthorized as ex:
            return
