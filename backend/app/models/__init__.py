
from app.extensions import db

# Import de Model
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission

def init_db():
    """Initialiser la base de données et insérer des données par défaut."""
    db.create_all()

    if not Role.query.first():
        super_admin_role = Role(libelle="SUPER ADMIN")
        admin_role = Role(libelle="ADMIN")
        superviseur_role = Role(libelle="SUPERVISEUR")
        agent_role = Role(libelle="AGENT")

        db.session.add_all([super_admin_role, admin_role, superviseur_role,agent_role])
        db.session.commit()

    # Vérifier si les permissions existent déjà
    if not Permission.query.first():
        read_permission = Permission(libelle="read")
        write_permission = Permission(libelle="write")
        delete_permission = Permission(libelle="delete")
        update_permission = Permission(libelle="update")

        db.session.add_all([read_permission, write_permission,delete_permission,update_permission])
        db.session.commit()

     # Vérifier si un admin existe déjà
    if not User.query.filter_by(email="admin@capsure.com").first():
        from werkzeug.security import generate_password_hash
        super_admin_role = Role.query.filter_by(libelle="SUPER ADMIN").first()
        admin = User(
            email="admin@capsure.com",
            username="admin",
            name = "admin",
            lastname= "admin",
            password=generate_password_hash("admin"),  # Mets un vrai hash de mot de passe ici
            role=super_admin_role
        )
        db.session.add(admin)
        db.session.commit()

    print("🚀 Base de données initialisée avec des données par défaut !")
