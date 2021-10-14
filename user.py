import uuid
import json
from transaction import Transaction
from users_db import users_db

# def add_user(user):
#     f = open('db/users.json')
#     data = json.load(f)

#     data.append(user)

#     f = open('db/users.json', 'w')
#     json.dump(data, f)

class User:
    def __init__(self, username, password):
        self.id = str(uuid.uuid4())
        self.username = username
        self.password = password # TODO: encrypt this password with AES
        users_db.add_user(self.__dict__)

    def perform_transaction(self, receiver_username, amount):
        return Transaction(self.username, receiver_username, amount)

    def __str__(self):
        return "Id: " + self.id + ", Username: " + self.username
