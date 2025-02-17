from app.extensions import db
from datetime import datetime

class RolePermission(db.Model):
    __tablename__ = "role_permissions"
    # id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk_role_permission'), primary_key=True,nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey('permissions.id', name='fk_permission_role'),primary_key=True, nullable=False)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de mise à jour
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete (null = non supprimé)


    def soft_delete(self):
        #Marque l'élément comme supprimé sans l'effacer réellement
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        #Restaure un élément supprimé
        self.deleted_at = None
        db.session.commit()

    def is_deleted(self):
        #Vérifie si l'élément est supprimé
        return self.deleted_at is not None
