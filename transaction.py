from time import time

class Transaction:
    def __init__(self, sender, receiver, amount):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time()

    def __str__(self):
        return f"{self.sender} paid {self.receiver} {self.amount}$"