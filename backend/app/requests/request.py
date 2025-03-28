from marshmallow import Schema, fields, ValidationError

class UserAddPermissionRequestSchema(Schema):
    user_id = fields.Integer(required= True, error_messages={"required": "Le champ user_id est obligatoire."})
    permissions_id = fields.List(fields.Integer(),required= True, error_messages={"required": "Le champ permissions_id est obligatoire et doit être un tableau d'entier."})

