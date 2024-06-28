from .Resource import Resource
import falcon

class ProtectedResource(Resource):
    def on_get(self, req, resp):
        user = req.context.get('user')
        if not user:
            raise falcon.HTTPUnauthorized(description='Authentication required')

        resp.media = {'message': f'Hello, {user}!'}