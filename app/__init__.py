import falcon

from .resources import ExampleResource

def create_app():
    app = falcon.App()
    example = ExampleResource()
    app.add_route('/example', example)
    return app