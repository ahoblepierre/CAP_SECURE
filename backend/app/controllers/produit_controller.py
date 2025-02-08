from flask import Blueprint, request, jsonify

produit_bp = Blueprint("produit", __name__)

@produit_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello from produit Controller"})

@produit_bp.route("/create", methods=["GET"])
def create():
    return jsonify({"message": "Hello from produit Controller"})

@produit_bp.route("/show", methods=["GET"])
def show(id:str):
    return jsonify({"message": "Hello from produit Controller"})

@produit_bp.route("/update", methods=["POST"])
def update():
    return jsonify({"message": "Hello from produit Controller"})

@produit_bp.route("/destroy", methods=["DELETE"])
def destroy(id:str):
    return jsonify({"message": "Hello from produit Controller"})
