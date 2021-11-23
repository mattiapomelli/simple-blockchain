from users_db import users_db
from hashlib import sha256
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError

class Auth:
    """
    This class handles user authentication. 
    """

    def __init__(self):
        """
        user: user that is currently logged in, or None when no user is logged in
        """
        self.user = None

    def signup(self, username, password, email):
        """
        Creates a new user with the given username and password. Password is hashed with SHA256.
        Raises ConflictError if the username is already taken
        """
        existing_user = users_db.find_by_username(username)

        if existing_user is not None:
            raise ConflictError

        hashed_password = sha256(password.encode()).hexdigest()
        self.user = users_db.create(username, hashed_password, email)

    def signin(self, username, password):
        """
        Signs in the user with the given username.
        Raises NotFoundError if no user is found with the given username.
        Raises InvalidCredentialsError if the given password doesn't correspond
        with the user's password.
        Since the password in the db is stored as hashed, the given password
        must also be hashed with the same algorithm before comparing it with the stored one.
        """
        user = users_db.find_by_username(username)
        
        if user is None:
            raise NotFoundError

        hashed_password = sha256(password.encode()).hexdigest()
        
        if user.password != hashed_password:
            raise InvalidCredentialsError
        
        self.user = user
    
    def is_logged(self):
        """
        Returns True if a user is logged in, False otherwise
        """
        return self.user != None
