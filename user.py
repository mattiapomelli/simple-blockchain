import json
from transaction import Transaction

class User:
    """
    This class represents an user of the system.
    Users can perform transactions, that is sending money to other users,
    and receive money for mining blocks
    """

    def __init__(self, id, username, password):
        """
        id: unique identifier of the user
        username: username of the user, is also unique
        password: password of the user
        """
        self.id = id
        self.username = username
        self.password = password

    def perform_transaction(self, receiver_username, amount):
        """
        Performs a new transaction:
        - receiver_username: username of the user to send the money to
        - amount: amount of money to be sent
        """
        return Transaction(self.username, receiver_username, amount)

    def __str__(self):
        return "Id: " + self.id + ", Username: " + self.username
