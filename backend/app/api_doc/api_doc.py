
from marshmallow import Schema, fields

class AgentFieldSchema(Schema):
    required_fields = ["name","lastname","username", "password", "email", "start_time", "end_time", "support"]
    name = fields.Str(required=True, description="Nom de l'agent")
    lastname = fields.Str(required=True, description="Prenom de l'agent")
    username = fields.Str(required=True, description="Prenom de l'agent")
    password = fields.Str(required=True, description="Mot de passe")
    email = fields.Str(required=True, description="Email de l'agent")
    start_time = fields.Str(required=True, description="heure debut de travail")
    end_time = fields.Str(required=True, description="heure fin de travail")
    support = fields.Str(required=True, description="Support télephonique")


class AgentResponseSchema(Schema):
    message = fields.Str(description="Message de succès ou d'erreur")

# Définition du schéma pour chaque élément dans "data"
class AgentDataSchema(Schema):
    id = fields.Int(description="ID de l'agent")
    name = fields.Str(description="Nom de l'agent")
    username = fields.Str(description="Username de l'agent")
    email = fields.Str(description="Email de l'agent")
    lastname = fields.Str(description="lastname de l'agent")

class AgentResponseForDataSchema(Schema):
    message = fields.Str(description="Message de succès ou d'erreur")
    data = fields.List(fields.Nested(AgentDataSchema))




