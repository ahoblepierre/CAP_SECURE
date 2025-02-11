from datetime import time, timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token

from app.authentication.auth import Auth
from app.models.role import Role
from app.models.user import User

from ..middleware import auth_required

from app.extensions import csrf

from app.extensions import db
from werkzeug.security import generate_password_hash



user_bp = Blueprint("user", __name__)
@csrf.exempt
@user_bp.route("/", methods=["GET"])
# @auth_required
def get_users():
    users = User.query.all()
    users_serialized = [user.to_dict() for user in users]
    return jsonify({"msg": "Liste des utilisateurs", "users": users_serialized})


@user_bp.route("/create", methods=["POST"])
@csrf.exempt
def create():
    fields = request.json
    required_fields = ["name","lastname","username", "password", "email", "start_time", "end_time", "support"]

    # Vérifier si tous les champs obligatoires sont présents
    missing_fields = [field for field in required_fields if field not in fields]

    if missing_fields:
        return (
            jsonify({"msg": f"Les champs {', '.join(missing_fields)} sont requis."}),
            422,
        )
    
    try:
        user = User.query.filter_by(email =request.json.get("email")).first()
        if user :
            return {"msg": "Utilisateur existe déjâ"}, 409
        
        role_agent = Role.query.filter_by(libelle = "AGENT").first()
        hashed_password = generate_password_hash(request.json.get("password"), method='pbkdf2:sha256', salt_length=20)
        agent = User(
            email=request.json.get("email"),
            username=request.json.get("username"),
            password= hashed_password,
            start_time = time.fromisoformat(request.json.get("start_time")),
            end_time = time.fromisoformat(request.json.get("end_time")),
            support = request.json.get("support"),
            name = request.json.get("name"),
            lastname = request.json.get("lastname"),
            role = role_agent
        )

        db.session.add(agent)
        db.session.commit()
        return jsonify({"msg": "Agent ajouté avec succès"}), 200
    except Exception as ex:
        return jsonify({"msg": f"{str(ex)}"}), 500




@user_bp.route("/login", methods=["POST"])
@csrf.exempt
def login_superviseur():
    fields = request.json
    required_fields = ["password", "email"]
    # Vérifier si tous les champs obligatoires sont présents
    missing_fields = [field for field in required_fields if field not in fields]

    if missing_fields:
        return (
            jsonify({"msg": f"Les champs {', '.join(missing_fields)} sont requis."}),
            422,
        )
    
    email=request.json.get("email")
    password=request.json.get("password")
    
    if Auth.attempt(email=email, password=password):
        user = Auth.user()
        access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(hours=24))
        return {"msg":"Connexion réussi", "data" :access_token}, 200
    
    return {"msg":"Email ou mot de passe incorrecte"},400
 
