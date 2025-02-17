from flask import Flask
from app.controllers.administration_controller import administration_bp
from app.controllers.superviseur_controller import superviseur_bp
from app.controllers.authentication_controller import authentication_bp
from app.controllers.agent_controller import agent_bp, create as createAgent, index as indexAgent
from app.controllers.user_controller import user_bp, create as createUser, login_superviseur

from app.controllers.agent_controller import agent_bp
from app.controllers.user_controller import user_bp

def register_blueprints(app: Flask):
   app.register_blueprint(administration_bp, url_prefix='/api/administration')
   app.register_blueprint(superviseur_bp, url_prefix='/api/superviseur')
   app.register_blueprint(authentication_bp, url_prefix='/api/authentication')
   app.register_blueprint(agent_bp, url_prefix='/api/agent')
   # Home controller route login_superviseur
   app.register_blueprint(user_bp, url_prefix="/api/user")
