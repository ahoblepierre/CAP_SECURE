from flask import Flask
from app.controllers.user_controller import user_bp

def register_blueprints(app: Flask):
   # Home controller route
   app.register_blueprint(user_bp, url_prefix="/api/user")
