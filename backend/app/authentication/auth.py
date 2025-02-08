
from werkzeug.security import  check_password_hash

from flask_login import login_user, logout_user, current_user

from app.models.user import User


class Auth():

    # Authenticate user
    @staticmethod
    def attempt(email: str, password : str) -> bool :

        """
        Tentative de connexion d'un utilisateur avec son email et son mot de passe
            Args :
                :email (str) : email de l'utilisateur 
                :password (str) : mot de passe de l'utilisateur
            Returns :
                user (User) || None   
        """

        # Rechercher l'utilisateur par son email
        user = User.query.filter_by(email= email).first()

        if  user and check_password_hash(pwhash=user.password, password=password) :
            login_user(user=user)
            return True
        
        # Retourner None si l'utilisateur n'existe pas
        return False
    
    @staticmethod
    def logout():
        """
            Déconnecte l'utilisateur et supprime la session.
        """
        logout_user()

    
    @staticmethod
    def check() -> bool:
        """
        Vérifie si un utilisateur est actuellement connecté.
        
        :return: True si un utilisateur est connecté, False sinon
        """
        return current_user.is_authenticated
    

    @staticmethod
    def user() -> User | None:
        """
        Retourne l'utilisateur actuellement connecté.
        
        :return: Instance de l'utilisateur ou None si aucun utilisateur n'est connecté
        """
        return current_user if current_user.is_authenticated else None
    





