import os
from dotenv import load_dotenv

# TODO: add this into the readme
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)


class Config:
    # 'mysql://username:password@localhost/db_name' for mysql db
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    # in seconds; this depends on the configuration of the DB backend
    SQLALCHEMY_POOL_RECYCLE = 240
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')
