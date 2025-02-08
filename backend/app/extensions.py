from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate

from flask_jwt_extended import JWTManager

from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager

db = SQLAlchemy()

migrate = Migrate()  # Ajout de Flask-Migrate


jwt = JWTManager() # jwt


csrf = CSRFProtect() # CSRF


# Initialiser le gestionnaire de sessions
login_manager = LoginManager()


