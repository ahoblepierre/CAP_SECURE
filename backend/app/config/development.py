

from app.config.base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://kth:Root#123@localhost/cap_secure"  # SQLite pour le dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False
