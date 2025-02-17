from functools import wraps
from flask import request, jsonify
from flask_login import current_user

def admin_middleware(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user and current_user.role.name == "AGENT":
            return jsonify({"msg":"Not Authorized"}), 401
        return f(*args, **kwargs)
    return decorated_function
