from flask import Flask
from app.controllers.agent_controller import agent_bp
from app.controllers.user_controller import user_bp

def register_blueprints(app: Flask):
   app.register_blueprint(agent_bp, url_prefix='/api/agent')
   # Home controller route login_superviseur
   app.register_blueprint(user_bp, url_prefix="/api/user")
