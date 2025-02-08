import os

class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
