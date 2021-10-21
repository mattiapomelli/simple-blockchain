from time import time
from aes import AESCipher

class Transaction:
    """
    This class represents a transaction of the cryptocurrency.
    Transactions have to be stored inside a block in the chain to be considered official.
    """

    def __init__(self, sender, receiver, amount, reason, encryption_key):
        """
        sender: username of the user which is sending the money
        receiver: username of the user who is receiving the money
        amount: amount of money sent
        timestamp: time at which the transaction was made
        reason: 
        """
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time()

        aes = AESCipher(encryption_key)
        self.reason = aes.encrypt(reason)

    def __str__(self):
        return f"{self.sender} paid {self.receiver} {self.amount}$ for {self.reason}"
