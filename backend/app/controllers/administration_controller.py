from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from app.extensions import csrf, db
from app.middleware import validate_request

from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.user import User
from app.requests import UserAddPermissionRequestSchema

administration_bp = Blueprint("administration", __name__)

# Définition du Blueprint

@administration_bp.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Hello from administration Controller"})

@administration_bp.route("/create", methods=["GET"])
def create():
    return jsonify({"message": "Hello from administration Controller"})


@administration_bp.route("/add-user/permission/", methods=["POST"])
@csrf.exempt
@jwt_required()
@validate_request(UserAddPermissionRequestSchema)
def add_permission_user(validated_data):
    try:
        permissions = validated_data['permissions_id']
        id = validated_data['user_id']

        if not (permissions) :
            return jsonify({"msg":"Aucune permissions renseignée"}), 422
        
        # Recupérer toutes les permissions
        all_permissions = Permission.query.filter(Permission.id.in_(permissions)).all()
        
        user = User.query.get_or_404(ident=id, description="User not Found")

        # Récupérer les permissions déjà associées au rôle
        existing_permission_ids = {rp.id for rp in user.role.permissions}

        # Filtrer les nouvelles permissions à ajouter
        new_role_permissions = [
            RolePermission(role_id=user.role.id, permission_id=per.id)
            for per in all_permissions if per.id not in existing_permission_ids
        ]

        # Ajouter uniquement les nouvelles permissions
        if new_role_permissions:
            db.session.bulk_save_objects(new_role_permissions)
            db.session.commit()

        return jsonify({"msg": "permission ajouté avec succès"}), 200
    except Exception as ex:
        print(ex)
        return {"msg":f"Une erreur s'est produite {str(ex)}"}
