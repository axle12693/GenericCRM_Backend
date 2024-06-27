import falcon

from .resources import UserResource, LoginResource, ProtectedResource, CheckResource
from .auth import JWTAuthMiddleware
from .config import Config


def create_app():
    app = falcon.App(middleware=[JWTAuthMiddleware()])
    config = Config()
    user_resource = UserResource(config)
    login_resource = LoginResource(config)
    protected_resource = ProtectedResource(config)
    check_resource = CheckResource(config)
    app.add_route("/check", check_resource)
    app.add_route('/register', user_resource)
    app.add_route('/login', login_resource)
    app.add_route('/protected', protected_resource)
    return app
