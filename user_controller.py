from users_db import users_db
from hashlib import sha256

class UserController:
    def __init__(self):
        self.current_user = None

    def signup(self, username, password):
        existing_user = users_db.find_by_username(username)

        if existing_user is not None:
            print("Username is taken")
            return

        hashed_password = sha256(password.encode()).hexdigest()

        self.current_user = users_db.create(username, hashed_password)
        print("Created new user: " + username)
        print("Signed in as " + username)

    def signin(self, username, password):
        user = users_db.find_by_username(username)
        
        if user is None:
            print("No user exists with the provided username")
            return

        hashed_password = sha256(password.encode()).hexdigest()
        
        if user.password == hashed_password:
            self.current_user = user
            print("Signed in as " + username)
        else:
            print("Password is not correct")

user_controller = UserController()
