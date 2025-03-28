
from datetime import datetime
from app.extensions import db


class Role(db.Model):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    permissions = db.relationship('Permission', secondary='role_permissions', backref=db.backref('roles', lazy='dynamic'))


    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de mise à jour
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete (null = non supprimé)

    def soft_delete(self):
        """ Marque l'élément comme supprimé sans l'effacer réellement """
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        """ Restaure un élément supprimé """
        self.deleted_at = None
        db.session.commit()

    def is_deleted(self):
        """ Vérifie si l'élément est supprimé """
        return self.deleted_at is not None
    

    def to_dict(self) :
        return {
            "name": self.name
        }

    def __repr__(self):
        return f"<Role {self.name}>"
