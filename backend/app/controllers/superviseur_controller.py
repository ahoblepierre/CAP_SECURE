from datetime import time
from flask import Blueprint, request, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required

from app.extensions import csrf, db
from app.models.role import Role
from app.models.user import User
from werkzeug.security import generate_password_hash

superviseur_bp = Blueprint("superviseur", __name__)


# Définition du Blueprint


@superviseur_bp.route("/", methods=["GET"])
@csrf.exempt
@jwt_required()
def index():
    try :
        # Récupérer les paramètres de pagination (page et taille par défaut)
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get(
            "per_page", 50, type=int
        )  # Par exemple, 10 agents par page

        user_id = get_jwt_identity()
        admin = User.query.filter_by(id=user_id).first()

        if not admin:
            return jsonify({"msg": "Admin non trouvé", "data": []}), 404

        # Pagination des agents créés par l'admin
        pagination = (
        db.session.query(User)
        .filter(User.id.in_([agent.id for agent in admin.created_agents]))
        .order_by(User.created_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
        )
        agents = [agent.to_dict() for agent in pagination.items]
    
        print(type( admin.created_agents))

        return (
            jsonify(
                {
                    "msg": "Liste des agents",
                    "data": agents,
                    "total": pagination.total,
                    "pages": pagination.pages,
                    "current_page": pagination.page,
                }
            ),
            200,
        )
    except Exception as ex:
        print(ex)
        return {"msg":f"Une erreur s'est produite {str(ex)}"}, 500


@superviseur_bp.route("/create", methods=["POST"])
@csrf.exempt
@jwt_required()
def create():
    try :
        user_id = get_jwt_identity()
        fields = request.json
        required_fields = ["name","lastname","username", "password", "email", "start_time", "end_time", "support", 'role']

        # Vérifier si tous les champs obligatoires sont présents
        missing_fields = [field for field in required_fields if field not in fields]

        if missing_fields:
            return (
                jsonify({"msg": f"Les champs {', '.join(missing_fields)} sont requis."}),
                422,
            )
        
        role_user = Role.query.filter_by(libelle = request.json.get("role")).first()
        if role_user : 
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
                role = role_user,
                created_by=user_id,
            )

            db.session.add(user)
            db.session.commit()
            return {"msg": "Utilisateur ajouté avec succès"}, 200
        
        return {"msg": f"Rôle {request.json.get("role")} utilisateur non trouvé"}, 400
        
    except Exception as ex :
        print(ex)
        return {"msg":"Une erreur s'est produite"}, 500


@superviseur_bp.route("/show", methods=["GET"])
def show(id: str):
    return jsonify({"message": "Hello from superviseur Controller"})


@superviseur_bp.route("/update", methods=["POST"])
def update():
    return jsonify({"message": "Hello from superviseur Controller"})


@superviseur_bp.route("/destroy", methods=["DELETE"])
def destroy(id: str):
    return jsonify({"message": "Hello from superviseur Controller"})
