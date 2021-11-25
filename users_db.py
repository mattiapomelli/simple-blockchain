import json
from user import User
from Crypto.Hash import SHA256
from printer import Printer

class UserDB:
    """
    This class represents a service to interact with the database of the users.
    The database is represented by a json file.

    db: list of all the users of the system
    db_path: path to the file storing user information
    db_hash_path: path to the file storing the hash of the db
    """

    db = None
    db_path = 'db/users.json'
    db_hash_path = 'db/users-hash.txt'

    def __init__(self):
        """
        Opens the file representing the db and stores its content in the db attribute.
        If there is an error opening the file, it resets the db to be empty.
        """
        file = open(self.db_path)
        
        try:
            data = json.load(file)
            db_hash = SHA256.new(str(data).encode()).hexdigest()
            
            hash_file = open(self.db_hash_path, 'r')
            stored_hash = hash_file.read()

            if (db_hash != stored_hash):
                Printer.error("User database has has been corrupted: hashes don't match")
                raise SystemExit

            # convert the users from json to User objects
            self.db = [User(u['username'], u['password'], u['email'], u['phone_nr'], u['address']) for u in data]
            self.save_db_hash()
        except SystemExit:
            exit()
        except:
            self.reset()

    def create(self, username, password, email, phone_nr, address):
        """
        Creates a new user and adds it to the database (writes the new list of users to the file)
        Returns the created user
        """
        new_user = User(username, password, email, phone_nr, address)

        self.db.append(new_user)

        # TODO: omptimization: don't rewrite the whole file, but just apped the new user
        # convert the users from User objects to json serializable dictionaries
        file = open(self.db_path, 'w')
        # serialized_db = [u.__dict__ for u in self.db]
        json.dump(self.serialized_db, file, indent=4)

        self.save_db_hash()

        return new_user

    def find_by_username(self, username):
        """
        Finds an user by username. Returns the user if exists, None otherwise
        """
        return next((u for u in self.db if u.username == username), None)

    def reset(self):
        """
        Drop all the elements in the db
        """
        file = open(self.db_path, 'w')
        file.write(str([]))
        self.db = []
        self.save_db_hash()

    def save_db_hash(self):
        file = open(self.db_hash_path, 'w')
        db_hash = SHA256.new(str(self.serialized_db).encode()).hexdigest()
        
        file.write(db_hash)

    @property
    def serialized_db(self):
        """
        Returns the db content in a format writable to a file
        """
        return [u.__dict__ for u in self.db]

    def __str__(self):
        res = ""
        for user in self.db:
            res += str(user)
        return res

# user database controller that will be used to perform operations on the db
users_db = UserDB()
