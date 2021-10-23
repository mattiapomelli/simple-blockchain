from users_db import users_db
from hashlib import sha256
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError

class Auth:
    def __init__(self):
        self.user = None

    def signup(self, username, password):
        existing_user = users_db.find_by_username(username)

        if existing_user is not None:
            raise ConflictError

        hashed_password = sha256(password.encode()).hexdigest()

        self.user = users_db.create(username, hashed_password)

    def signin(self, username, password):
        user = users_db.find_by_username(username)
        
        if user is None:
            raise NotFoundError

        hashed_password = sha256(password.encode()).hexdigest()
        
        if user.password != hashed_password:
            raise InvalidCredentialsError
        
        self.user = user
