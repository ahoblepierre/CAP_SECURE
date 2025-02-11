from flask import Flask
from app.controllers.produit_controller import index,create, produit_bp
from app.controllers.agent_controller import agent_bp, create as createAgent, index as indexAgent
from app.controllers.user_controller import user_bp

from app.extensions import docs

def register_blueprints(app: Flask):
   app.register_blueprint(produit_bp, url_prefix='/api/produit')
   app.register_blueprint(agent_bp, url_prefix='/api/agent')
   # Home controller route
   app.register_blueprint(user_bp, url_prefix="/api/user")


   # Ajouter les routes de Flask-APISpec
   docs.register(index, blueprint="produit")
   docs.register(create, blueprint="produit")

   docs.register(createAgent, blueprint="agent")
   docs.register(indexAgent, blueprint="agent")
