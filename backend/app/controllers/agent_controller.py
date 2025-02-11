from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.api_doc.api_doc import AgentFieldSchema, AgentResponseForDataSchema, AgentResponseSchema
from app.models.role import Role
from app.models.user import User

from datetime import time

from werkzeug.security import generate_password_hash

from app.extensions import csrf, db

from flask_apispec import use_kwargs, marshal_with, doc

agent_bp = Blueprint("agent", __name__)

# Définition du Blueprint

@agent_bp.route("/", methods=["GET"])
@doc(description="Liste des agents", tags=["Agent"])
@marshal_with(AgentResponseForDataSchema)
@jwt_required()
@jwt_required()
def index():

    try :
        user_id = get_jwt_identity()
        superviseur = User.query.filter_by(id =user_id).first()
       

        if not superviseur:
            return jsonify({"msg": "Superviseur non trouvé","data":[]}), 404
        
        agents = [agent.to_dict() for agent in superviseur.created_agents]
        
        print(agents)

        return jsonify({"msg": "Liste des agents", "data": agents}), 200
    except Exception as ex :
        print(ex)
        return {"msg": f"Une erreur s'est produite  {str(ex)} "}, 500


@csrf.exempt # delete  Cross
@agent_bp.route("/create", methods=["POST"])
@doc(description="Ajouter un  agent", tags=["Agent"])
@use_kwargs(AgentFieldSchema,location="json")
@marshal_with(AgentResponseSchema)
@jwt_required() # Jwt required
def create():
    user_id = get_jwt_identity()

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
        
        role_superviseur = Role.query.filter_by(libelle = "SUPERVISEUR").first()
        hashed_password = generate_password_hash(request.json.get("password"), method='pbkdf2:sha256', salt_length=20)
        user = User(
            email=request.json.get("email"),
            username=request.json.get("username"),
            password= hashed_password,
            start_time = time.fromisoformat(request.json.get("start_time")),
            end_time = time.fromisoformat(request.json.get("end_time")),
            support = request.json.get("support"),
            name = request.json.get("name"),
            lastname = request.json.get("lastname"),
            role = role_superviseur,
            created_by=user_id
        )

        db.session.add(user)
        db.session.commit()
        return jsonify({"msg": "Agent ajouté avec succès"}), 200
    except Exception as ex:
        return jsonify({"msg": f"{str(ex)}"}), 500

@agent_bp.route("/show", methods=["GET"])
def show(id:str):
    return jsonify({"message": "Hello from Agent Controller"})

@agent_bp.route("/update", methods=["POST"])
def update():
    return jsonify({"message": "Hello from Agent Controller"})

@agent_bp.route("/destroy", methods=["DELETE"])
def destroy(id:str):
    return jsonify({"message": "Hello from Agent Controller"})
