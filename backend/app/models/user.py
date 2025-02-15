
from datetime import datetime, time
from app.extensions import db
import uuid

class User(db.Model):
    __tablename__ = "users"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    uid = db.Column(db.String(200), unique=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(80), nullable=False)
    lastname = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    support  = db.Column(db.String(200), nullable=True)
    start_time = db.Column(db.Time(), nullable=True, default=time(6, 30, 0))
    end_time = db.Column(db.Time(), nullable=True, default=time(18, 0, 0))
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk_user_role'), nullable=False)
    role = db.relationship('Role', backref=db.backref('users', lazy=True))

    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Référence à l'admin qui a créé l'agent
    creator = db.relationship('User', backref=db.backref('created_agents', lazy=True), remote_side=[id])



    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de mise à jour
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete (null = non supprimé)


    def is_active(self):
        return self.active

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

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
            "name" : self.name,
            "email": self.email,
            "username" : self.username,
            "lastname" : self.username,
            "role": self.role.to_dict()
        }
