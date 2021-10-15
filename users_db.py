import json
from user import User

class UserDB:
    """
    This class represents a service to interact with the database of the users.
    The database is represented by a json file.

    db: list of all the users of the system
    db_path: path to the file storing user information
    """

    db = None
    db_path = 'db/users.json'

    def __init__(self):
        """
        Opens the file representing the db and stores its content in the db attribute
        """
        # TODO: if file is empty create an empty db with "[]"
        f = open(self.db_path)
        self.db = json.load(f)

    def create_user(self, username, password):
        """
        Creates a new user and adds it to the database (writes the new list of users to the file)
        Returns the created user
        """
        # TODO: encrypt this password with AES
        new_user = User(username, password)

        # TODO: check that the username doesn't exist already
        self.db.append(new_user.__dict__)

        # TODO: omptimization: don't rewrite the whole file, but just apped the new user
        f = open(self.db_path, 'w')
        json.dump(self.db, f)

        return new_user

    def sign_in(self, username, password):
        return

# user database controller that will be used to perform operations on the db
users_db = UserDB()
