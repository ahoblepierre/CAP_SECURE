from flask import Flask, send_from_directory, request
import os
from app.models.user import User
from app.config.development import DevelopmentConfig
from app.controllers import register_blueprints
from app.extensions import  db, migrate, login_manager

from app.models import init_db  # Import des modèles

from app.extensions import jwt

from app.extensions import csrf


from flask_talisman import Talisman

from flask_cors import CORS


from .commands import register_commands

import logging

def create_app():
    app = Flask(__name__)


    # Configuration de CORS
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:4200"}})

    @app.before_request
    def handle_options():
        if request.method == "OPTIONS":
            return '', 200




    #jwt configuration
    app.config["JWT_SECRET_KEY"] = "super-secret-key"
    jwt.init_app(app)



    csrf.init_app(app)  # Active la protection CSRF

    Talisman(app, force_https=False, content_security_policy={"script-src": ["'self'", "'unsafe-inline'"]}) # 🔥 Active les protections HTTP sécurisées



    # Charger la configuration selon l'environnement
    env = os.getenv("FLASK_ENV", "development")
    if env == "development":
        app.config.from_object("app.config.development.DevelopmentConfig")
    else:
        app.config.from_object("app.config.production.ProductionConfig")


    # Initialiser SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)  # Ajout de Migrate
    login_manager.init_app(app) # Initiation de login Manager


    @login_manager.user_loader
    def load_user(user_id):
        """Charge un utilisateur à partir de son ID pour Flask-Login"""
        return User.query.get(int(user_id))



    # Initialiser la base de données (création des tables)
    with app.app_context():
        init_db()

    
    # Enregistrer les routes
    register_blueprints(app)



    # Enregistrer les commandes personnalisées
    register_commands(app)



    logging.basicConfig(level=logging.DEBUG)



    return app
