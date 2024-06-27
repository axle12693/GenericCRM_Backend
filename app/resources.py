import json

import falcon
from .models import create_user, authenticate_user
import subprocess
import psycopg2
from psycopg2 import OperationalError


class Resource:
    def __init__(self, config):
        self.config = config


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


class ProtectedResource(Resource):
    def on_get(self, req, resp):
        user = req.context.get('user')
        if not user:
            raise falcon.HTTPUnauthorized(description='Authentication required')

        resp.media = {'message': f'Hello, {user}!'}

class CheckResource(Resource):
    @staticmethod
    def check_postgres_installed():
        try:
            result = subprocess.run(['psql', '--version'], capture_output=True, text=True)
            if result.returncode == 0:
                return True
            else:
                return False
        except FileNotFoundError:
            return False

    def check_db_access(self):
        try:
            connection = psycopg2.connect(
                host=self.config.db_host,
                database=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password,
                port=self.config.db_port
            )
            connection.close()
            return True
        except OperationalError as e:
            return str(e)
    def on_get(self, req, resp):
        checks = {"postgres installed": self.check_postgres_installed(),
                  "db_accessible": self.check_db_access()}
        resp.media = json.dumps(checks)


