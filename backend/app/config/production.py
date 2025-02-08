

from app.config.base_config import BaseConfig


class ProductionConfig(BaseConfig):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql://user:password@localhost/prod_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
