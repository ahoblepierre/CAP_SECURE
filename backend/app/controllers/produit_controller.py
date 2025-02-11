from flask import Blueprint, request, jsonify
from flask_apispec import use_kwargs, marshal_with, doc

from marshmallow import Schema, fields


produit_bp = Blueprint("produit", __name__)



# 📌 Schéma pour la documentation des paramètres
class ProduitInputSchema(Schema):
    name = fields.Str(required=True, description="Nom du produit")
    price = fields.Float(required=True, description="Prix du produit")

# 📌 Schéma pour la réponse
class ProduitSchema(Schema):
    message = fields.Str()

# Définition du Blueprint

@produit_bp.route("/", methods=["GET"])
@use_kwargs(ProduitInputSchema, location="json")
@doc(description="Controlleur des produits", tags=["Produit"])
@marshal_with(ProduitSchema)
def index():
    return jsonify({"message": "Hello from produit Controller"})

@produit_bp.route("/create", methods=["GET"])
def create():
    return jsonify({"message": "Hello from produit Controller"})


