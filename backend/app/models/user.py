
from datetime import datetime, time
from app.extensions import db
import uuid

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(200), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), unique=True, nullable=False)
    lastname = db.Column(db.String(80), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    support  = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.Time(), nullable=True, default=time(6, 30, 0))
    end_time = db.Column(db.Time(), nullable=True, default=time(18, 0, 0))



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


    def __repr__(self):
        return f"<User {self.username}>"
    
    def to_dict(self):
        return {
            "id": self.id,
            "uid": self.uid,
            "email": self.email,
            "username" : self.username
        }
