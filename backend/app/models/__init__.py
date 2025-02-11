
from app.extensions import db

# Import de Model
from app.models.user import User
from app.models.role import Role
from app.models.permission import Permission
from app.models.agentuser import AgentUser

def init_db():
    db.create_all()
