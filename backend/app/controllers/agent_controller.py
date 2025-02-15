from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.models.role import Role
from app.models.user import User

from datetime import datetime, time

from werkzeug.security import generate_password_hash

from app.extensions import csrf, db


agent_bp = Blueprint("agent", __name__)

# Définition du Blueprint

@agent_bp.route("/", methods=["GET"])
@csrf.exempt
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
        
        role_agent = Role.query.filter_by(libelle = "AGENT").first()
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
            role = role_agent,
            created_by=user_id
        )

        db.session.add(user)
        db.session.commit()
        return {"msg": "Agent ajouté avec succès"}, 200
    except Exception as ex:
        return {"msg": f"{str(ex)}"}, 500

@agent_bp.route("/show/<string:id>", methods=["GET"])
@jwt_required()
def show(id:str):
    try :
        agent = User.query.get_or_404(ident=id)
        return {"message": "Agent found", "data":agent.to_dict()}, 200
    except Exception as ex:
        return {"msg":f"Une erreur s'est produite {str(ex)}","data":None}, 500

@agent_bp.route("/update/<string:id>", methods=["POST"])
@csrf.exempt 
@jwt_required()
def update(id:str):
    try :

        fields = request.json
        required_fields = ["name","lastname","username","email", "start_time", "end_time"]

        # Vérifier si tous les champs obligatoires sont présents
        missing_fields = [field for field in required_fields if field not in fields]

        if missing_fields:
            return (
                jsonify({"msg": f"Les champs {', '.join(missing_fields)} sont requis."}),
                422,
            )
    

        agent = User.query.get_or_404(ident=id, description="Agent not found")



        agent.username = request.json.get("username")
        agent.name = request.json.get('name')
        agent.start_time = time.fromisoformat(request.json.get('start_time'))
        agent.end_time = time.fromisoformat(request.json.get('end_time'))
        agent.email = request.json.get('email')
        agent.updated_at = datetime.now()

        if request.json.get('password'):
            agent.password = generate_password_hash(request.json.get("password"), method='pbkdf2:sha256', salt_length=20)
           
        
        # db.session.add(agent)
        db.session.commit()

        return jsonify({"message": "Agent update  with successfully"}), 200
    except Exception as ex :
        return jsonify({"msg":f"Une erreur s'est produite {str(ex)}"}), 500

@agent_bp.route("/destroy/<string:id>", methods=["DELETE"])
@csrf.exempt 
@jwt_required()
def destroy(id:str):
    try :
        agent = User.query.get_or_404(ident=id, description="Agent not found")
        db.session.delete(agent)
        db.session.commit()
        return jsonify({"message": "Agent supprimé avec succés"}), 200
    except Exception as ex:
        return {"msg":f"Une erreur s'est produite {str(ex)}"}, 500
