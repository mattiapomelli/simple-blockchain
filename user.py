import uuid
from transaction import Transaction

class User:
    def __init__(self, username):
        self.id = uuid.uuid4()
        self.username = username

    def perform_transaction(self, receiver_username, amount):
        return Transaction(self.username, receiver_username, amount)

    def __str__(self):
        return "Id: " + str(self.id) + ", Username: " + self.username
