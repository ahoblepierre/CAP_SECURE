from datetime import time
from flask import Blueprint, jsonify, request

from app.models.user import User

from ..middleware import auth_required

from app.extensions import csrf

from app.extensions import db

user_bp = Blueprint("user", __name__)


@user_bp.route("/", methods=["GET"])
# @auth_required
def get_users():
    users = User.query.all()
    users_serialized = [user.to_dict() for user in users]
    return jsonify({"message": "Liste des utilisateurs", "users": users_serialized})


@user_bp.route("/create", methods=["POST"])
@csrf.exempt
def create():
    fields = request.json
    required_fields = ["name","lastname","username", "password", "email", "start_time", "end_time", "support"]

    # Vérifier si tous les champs obligatoires sont présents
    missing_fields = [field for field in required_fields if field not in fields]

    if missing_fields:
        return (
            jsonify({"error": f"Les champs {', '.join(missing_fields)} sont requis."}),
            422,
        )
    

    try:
        user = User(
            email=request.json.get("email"),
            username=request.json.get("username"),
            password=request.json.get("password"),
            start_time = time.fromisoformat(request.json.get("start_time")),
            end_time = time.fromisoformat(request.json.get("end_time")),
            support = request.json.get("support"),
            name = request.json.get("name"),
            lastname = request.json.get("lastname")
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Utilisateur ajouté avec succès"}), 200
    except Exception as ex:
        return jsonify({"message": f"{str(ex)}"}), 500
