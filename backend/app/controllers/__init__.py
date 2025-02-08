from flask import Flask
from app.controllers.home_controller import home_bp
from app.controllers.produit_controller import produit_bp
from app.controllers.user_controller import user_bp

def register_blueprints(app: Flask):
   # Home controller route
   app.register_blueprint(home_bp, url_prefix='/api/home')
   app.register_blueprint(produit_bp, url_prefix='/api/produit')
   app.register_blueprint(user_bp, url_prefix="/api/user")
