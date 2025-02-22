import uuid

def generate_matricule():
    """Génère un matricule unique de 6 caractères alphanumériques en majuscules."""
    return uuid.uuid4().hex[:6].upper()