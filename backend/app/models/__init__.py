from app.extensions import db

# Import de Model
from app.models.user import User
from app.models.role import Role

def init_db():
    db.create_all()
