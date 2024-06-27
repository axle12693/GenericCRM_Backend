import falcon
from .models import decode_token


class JWTAuthMiddleware:
    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        if token is None:
            return
        token = token.split(' ')[1]
        try:
            req.context['user'] = decode_token(token)
        except falcon.HTTPUnauthorized as ex:
            return
