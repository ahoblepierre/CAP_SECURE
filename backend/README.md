# 📌 Lara-Flask : Une Structure Flask Inspirée de Laravel

## 🚀 Introduction
**Lara-Flask** est une structure préconçue pour Flask, inspirée de Laravel, permettant un développement rapide et organisé des applications web.  
Elle inclut une architecture modulaire avec des commandes CLI pour générer automatiquement les **controllers, models, middlewares** et bien plus.  

---

## 📂 Architecture du Projet
Voici la structure du projet :  

```
lara-flask/
│── app/
│   ├── config/          # Fichiers de configuration
│   ├── controllers/     # Gestion des routes et endpoints
│   │   ├── __init__.py  # Enregistrement automatique des controllers
│   │   ├── user_controller.py
│   ├── models/          # Gestion des modèles SQLAlchemy
│   ├── __init__.py      # Enregistrement automatique des models avec la creation des migrations
│   ├── services/        # Logique métier et traitements avancés
│   ├── middleware/      # Middlewares pour sécuriser les routes
│   ├── authentication/  # Gestion de l'authentification avec Flask-Login
│   ├── extensions.py    # Fichier pour la gestion des extensions 
│── migrations/          # Migrations de base de données
│── commands/            # Commandes CLI pour automatiser la création
│── tests/               # Tests unitaires
│── app.py               # Point d'entrée de l'application
│── requirements.txt     # Dépendances du projet
│── README.md            # Documentation du projet
│── setup.py             # Fichier pour installer Lara-Flask en package
```

---

## ⚡ Fonctionnalités Principales
✅ **Architecture Modulaire** : Séparation propre entre controllers, models, services et middlewares.  
✅ **Commandes CLI** : Génération automatique de fichiers avec des commandes Flask personnalisées.  
✅ **Support de l'Authentification** : Gestion simplifiée avec `Flask-Login`.  
✅ **Protection CSRF** : Sécurité renforcée pour les routes web et API.  
✅ **Base de données avec SQLAlchemy** : ORM puissant et migrations incluses avec `Flask-Migrate`.  

---

## 🔧 Installation et Configuration

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/ahoblepierre/lara-flask
cd lara-flask
```

### 2️⃣ Créer un environnement virtuel
```bash
python -m venv venv
source venv/bin/activate  # Sur Mac/Linux
venv\Scripts\activate     # Sur Windows
```

### 3️⃣ Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4️⃣ Lancer l'application
```bash
flask run
```
L'application sera accessible sur : `http://127.0.0.1:5000/`

---

## ⚙️ Commandes Personnalisées
### 🛠 Créer un Controller et un Model en même temps
```bash
flask make:cm User
```
💡 Cela générera automatiquement :  
- `app/controllers/user_controller.py`  
- `app/models/user.py`  
- **Ajoute directement** le controller dans `__init__.py`.  

### 🛠 Créer un Middleware
```bash
flask make:middleware AuthMiddleware
```

### 🛠 Créer une migration de base de données
```bash
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

---

## 🛡 Sécurité et Authentification
Lara-Flask intègre `Flask-Login` pour la gestion des sessions utilisateur avec des middlewares de protection.  
Exemple d’utilisation :  

```python
from flask_login import login_user, logout_user, login_required

@login_required
def dashboard():
    return jsonify({"message": "Bienvenue sur votre dashboard sécurisé !"})
```

---

## 📜 License
Ce projet est sous licence **MIT**, vous pouvez l'utiliser et le modifier librement.  

---

## 💡 Contribuer
Tu veux améliorer Lara-Flask ? Forke le repo et propose une Pull Request ! 🚀  

📩 **Contact** : [Pierre AHOBLE]  

📩 **Profil** : [[Pierre AHOBLE](https://github.com/ahoblepierre)] 

---

🔥 **Lara-Flask** : La puissance de Laravel dans un projet Flask ! 🚀

