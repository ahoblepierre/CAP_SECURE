import os
from flask import Flask
import click


CONTROLLER_INIT_FILE = "app/controllers/__init__.py"

def register_commands(app: Flask):
    """Enregistre les commandes Flask personnalisées."""

    @app.cli.command("make:controller")
    @click.argument("name")
    def make_controller(name):
        """Crée un contrôleur à la volée."""
        file_name = name.lower()
        controller_path = f"app/controllers/{file_name}_controller.py"
        content = f"""from flask import Blueprint, request, jsonify

{file_name}_bp = Blueprint("{file_name}", __name__)

# Définition du Blueprint

@{file_name}_bp.route("/", methods=["GET"])
def index():
    return jsonify({{"message": "Hello from {name} Controller"}})

@{file_name}_bp.route("/create", methods=["GET"])
def create():
    return jsonify({{"message": "Hello from {name} Controller"}})

@{file_name}_bp.route("/show", methods=["GET"])
def show(id:str):
    return jsonify({{"message": "Hello from {name} Controller"}})

@{file_name}_bp.route("/update", methods=["POST"])
def update():
    return jsonify({{"message": "Hello from {name} Controller"}})

@{file_name}_bp.route("/destroy", methods=["DELETE"])
def destroy(id:str):
    return jsonify({{"message": "Hello from {name} Controller"}})
"""

        create_file(controller_path, content)
        update_controllers_init(name)
        click.echo(f" ✅ Contrôleur '{name}' ...................... créé avec succès!")

    @app.cli.command("make:model")
    @click.argument("name")
    def make_model(name):
        """Crée un modèle à la volée."""
        models_dir = "app/models"
        model_path = f"{models_dir}/{name.lower()}.py"
        init_file = f"{models_dir}/__init__.py"
        content = f"""from app.extensions import db
from datetime import datetime

class {name}(db.Model):
    __tablename__ = "{name.lower()}s"
    id = db.Column(db.Integer, primary_key=True)


    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Date de création
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)  # Date de mise à jour
    deleted_at = db.Column(db.DateTime, nullable=True)  # Soft delete (null = non supprimé)


    def soft_delete(self):
        #Marque l'élément comme supprimé sans l'effacer réellement
        self.deleted_at = datetime.utcnow()
        db.session.commit()

    def restore(self):
        #Restaure un élément supprimé
        self.deleted_at = None
        db.session.commit()

    def is_deleted(self):
        #Vérifie si l'élément est supprimé
        return self.deleted_at is not None
"""
        create_file(model_path, content)

        # Ajouter l'import dans __init__.py en haut du fichier
        model_import = f"from app.models.{name.lower()} import {name}\n"

        if not os.path.exists(init_file):
            # Si le fichier n'existe pas, le créer avec l'import directement
            with open(init_file, "w") as f:
                f.write(model_import)
                f.write("\n\ndef init_db():\n    db.create_all()\n")
        else:
            with open(init_file, "r") as f:
                lines = f.readlines()

            # Vérifier si l'import existe déjà
            if model_import not in lines:
                # Insérer l'import en haut du fichier
                with open(init_file, "w") as f:
                    f.write(model_import)
                    f.writelines(lines)  # Réécrire le reste du fichier sans modifications

        click.echo(f" ✅  Modèle '{name}' ...................... créé avec succès!")

    @app.cli.command("make:middleware")
    @click.argument("name")
    def make_middleware(name):
        """Crée un middleware à la volée."""
        middleware_path = f"app/middleware/{name.lower()}.py"
        content = f"""from functools import wraps
from flask import request, jsonify

def {name.lower()}(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Middleware logique ici
        return f(*args, **kwargs)
    return decorated_function
"""
        create_file(middleware_path, content)
        click.echo(f" ✅ Middleware '{name}' ...................... créé avec succès!")


    @app.cli.command("make:cm")
    @click.argument("name")
    def make_cm(name):
        """Crée un contrôleur et un modèle à la fois."""
        
        # Création du modèle
        model_path = f"app/models/{name.lower()}.py"
        model_content = f"""from app.extensions import db

class {name}(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
"""
        create_file(model_path, model_content)
        click.echo(f" ✅ Modèle '{name}' ...................... créé avec succès!")

        # Création du contrôleur
        controller_path = f"app/controllers/{name.lower()}_controller.py"
        controller_content = f"""from flask import Blueprint, request, jsonify
from app.models.{name.lower()} import {name}

{name}_bp = Blueprint("{name}", __name__)

@{name}_bp.route("/", methods=["GET"])
def index():
    return jsonify({{"message": "Hello from {name} Controller"}})
"""
        create_file(controller_path, controller_content)
        update_controllers_init(name)
        click.echo(f" ✅ Contrôleur '{name}' ...................... créé avec succès!")

def create_file(path, content):
    """Crée un fichier avec le contenu donné s'il n'existe pas."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write(content)
    else:
        click.echo(f" ⚠️ Le fichier '{path}' existe déjà!")


def update_controllers_init(name):
    """Ajoute automatiquement l'enregistrement du contrôleur à `app/controllers/__init__.py`."""
    blueprint_import = f"from app.controllers.{name.lower()}_controller import {name.lower()}_bp"
    register_code = f"   app.register_blueprint({name.lower()}_bp, url_prefix='/api/{name.lower()}')"
    commenter_code =f"# Route {name.lower()} Controller "

    # Vérifier si le fichier __init__.py existe, sinon le créer
    if not os.path.exists(CONTROLLER_INIT_FILE):
        with open(CONTROLLER_INIT_FILE, "w") as f:
            f.write("from flask import Flask\n\n")
            f.write("def register_blueprints(app: Flask):\n    pass\n")

    # Lire le contenu actuel
    with open(CONTROLLER_INIT_FILE, "r") as f:
        lines = f.readlines()

    # Vérifier si le contrôleur est déjà importé
    if blueprint_import in lines:
        click.echo(f"⚠️ `{name}_controller.py` est déjà dans `__init__.py`.")
    else:
        # Insérer l'import au début
        lines.insert(1, blueprint_import + "\n")

    # Vérifier si la fonction register_blueprints existe déjà
    found_register_function = False
    for i, line in enumerate(lines):
        if "def register_blueprints" in line:
            found_register_function = True
            # Vérifier si le "pass" est trouvé dans la fonction
            if "pass" in lines[i + 1]:
                lines[i + 1] = register_code + "\n"
            else:
                # Ajouter l'enregistrement du blueprint à la fin de la fonction si nécessaire
                lines.insert(i + 1, register_code + "\n")
            break

    # Si la fonction register_blueprints n'existe pas, on l'ajoute à la fin
    if not found_register_function:
        lines.append("\n\ndef register_blueprints(app: Flask):\n")
        lines.append(f"    {register_code}\n")

    # Réécrire le fichier avec les modifications
    with open(CONTROLLER_INIT_FILE, "w") as f:
        f.writelines(lines)

    click.echo(f" ============================================================================ !")
    click.echo(f" ✅ `{name}_controller.py` ....................... ajouté dans `__init__.py` !")