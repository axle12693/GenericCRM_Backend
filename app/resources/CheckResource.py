from .Resource import Resource
import subprocess
import psycopg2
from psycopg2 import OperationalError
import json

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