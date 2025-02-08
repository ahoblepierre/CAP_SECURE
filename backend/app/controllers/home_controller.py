from flask import Blueprint, request, jsonify

home_bp = Blueprint("home", __name__)

@home_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello from Home Controller"})

@home_bp.route("/create", methods=["GET"])
def create():
    return jsonify({"message": "Hello from Home Controller"})

@home_bp.route("/show", methods=["GET"])
def show(id:str):
    return jsonify({"message": "Hello from Home Controller"})

@home_bp.route("/update", methods=["POST"])
def update():
    return jsonify({"message": "Hello from Home Controller"})

@home_bp.route("/destroy", methods=["DELETE"])
def destroy(id:str):
    return jsonify({"message": "Hello from Home Controller"})
