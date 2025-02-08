from flask import request, jsonify
from flask_login import current_user
from functools import wraps

def auth_required(f):
    """Middleware : Vérifie si l'utilisateur est authentifié"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({"error": "Vous devez être connecté"}), 401
        return f(*args, **kwargs)
    return decorated_function
