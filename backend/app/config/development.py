

from app.config.base_config import BaseConfig


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///dev.db"  # SQLite pour le dev
    SQLALCHEMY_TRACK_MODIFICATIONS = False
