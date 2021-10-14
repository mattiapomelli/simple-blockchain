import json

class UserDB:
    db = None
    db_path = 'db/users.json'

    def __init__(self):
        f = open(self.db_path)
        self.db = json.load(f)

    def add_user(self, user):
        self.db.append(user)

        f = open(self.db_path, 'w')
        json.dump(self.db, f)

    def sign_in(self, username, password):
        return

users_db = UserDB()
