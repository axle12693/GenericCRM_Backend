import falcon

class ExampleResource:
    def on_get(self, req, resp):
        resp.media = {'message': 'Hello, world!'}