import uuid
from transaction import Transaction

class User:
    def __init__(self, username, password):
        self.id = uuid.uuid4()
        self.username = username
        self.password = password # TODO: encrypt this password

    def perform_transaction(self, receiver_username, amount):
        return Transaction(self.username, receiver_username, amount)

    def __str__(self):
        return "Id: " + str(self.id) + ", Username: " + self.username
