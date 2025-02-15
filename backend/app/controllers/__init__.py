from flask import Flask
from app.controllers.authentication_controller import authentication_bp
from app.controllers.agent_controller import agent_bp, create as createAgent, index as indexAgent
from app.controllers.user_controller import user_bp, create as createUser, login_superviseur

from app.extensions import docs

def register_blueprints(app: Flask):
   app.register_blueprint(authentication_bp, url_prefix='/api/authentication')
   app.register_blueprint(agent_bp, url_prefix='/api/agent')
   # Home controller route login_superviseur
   app.register_blueprint(user_bp, url_prefix="/api/user")


   docs.register(createAgent, blueprint="agent")
   docs.register(indexAgent, blueprint="agent")


   docs.register(createUser, blueprint="user")
   docs.register(login_superviseur, blueprint="user")
