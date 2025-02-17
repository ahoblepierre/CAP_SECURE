from flask import request, jsonify
from functools import wraps
from marshmallow import Schema, fields, ValidationError

def validate_request(schema):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                # Charger et valider les données de la requête
                data = schema().load(request.json)
            except ValidationError as err:
                return jsonify({"message": "Données invalides", "errors": err.messages}), 422
            
            return f(data, *args, **kwargs)  # Passer les données validées à la fonction
        return wrapper
    return decorator
