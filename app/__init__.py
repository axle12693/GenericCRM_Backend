import falcon

from .resources import UserResource, LoginResource, ProtectedResource
from .auth import JWTAuthMiddleware

def create_app():
    app = falcon.App(middleware=[JWTAuthMiddleware()])
    user_resource = UserResource()
    login_resource = LoginResource()
    protected_resource = ProtectedResource()

    app.add_route('/register', user_resource)
    app.add_route('/login', login_resource)
    app.add_route('/protected', protected_resource)
    return app