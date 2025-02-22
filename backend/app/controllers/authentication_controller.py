from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app.extensions import csrf, db
from app.authentication.auth import Auth
from datetime import time, timedelta

from app.models.user import User

from app.extensions import csrf, db
from flask_cors import cross_origin

authentication_bp = Blueprint("authentication", __name__)

# Définition du Blueprint


@authentication_bp.route("/", methods=["POST","OPTIONS"],strict_slashes=False)
@cross_origin("http://localhost:4200")
@csrf.exempt
def login():
    fields = request.json
    required_fields = ["password", "email"]
    # Vérifier si tous les champs obligatoires sont présents
    missing_fields = [field for field in required_fields if field not in fields]

    if missing_fields:
        return (
            jsonify({"msg": f"Les champs {', '.join(missing_fields)} sont requis."}),
            422,
        )

    email = request.json.get("email")
    password = request.json.get("password")

    if Auth.attempt(email=email, password=password):
        auth = Auth.user()
        access_token = create_access_token(
            identity=str(auth.id), expires_delta=timedelta(hours=24)
        )
        user = User.query.get_or_404(ident=auth.id, description="Agent not found")
        return {
            "msg": "Connexion réussi",
            "data": access_token,
            "user": user.to_dict(),
        }, 200

    return {"msg": "Email ou mot de passe incorrecte"}, 400
