import dotenv
import os

class Config:
    def __init__(self):
        dotenv.load_dotenv()
        self.db_host = os.getenv("DB_HOST")
        self.db_name = os.getenv("DB_NAME")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASSWORD")
        self.db_port = os.getenv("DB_PORT")
        self.secret_key = os.getenv("SECRET_KEY")