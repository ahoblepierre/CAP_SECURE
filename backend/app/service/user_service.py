from app.models.user import User
from app.extensions import db

def get_user_by_username(username):
    """Récupère un utilisateur par son nom d'utilisateur."""
    return User.query.filter_by(username=username).first()

def create_user(username, email, password):
    """Crée un nouvel utilisateur."""
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()
    return new_user
