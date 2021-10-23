from time import time
from aes import AESCipher

class Transaction:
    next_id = 0

    """
    This class represents a transaction of the cryptocurrency.
    Transactions have to be stored inside a block in the chain to be considered official.
    """

    def __init__(self, sender, receiver, amount, reason, encryption_key = None):
        """
        sender: username of the user which is sending the money
        receiver: username of the user who is receiving the money
        amount: amount of money sent
        timestamp: time at which the transaction was made
        reason: reason of the transaction.
        encryption_key: key that is gonna be used to encrypt the reason of the transaction. If is None
                        then the reason will not be ecnrypted 
        """
        self.id = Transaction.next_id
        Transaction.next_id += 1
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.timestamp = time()

        if encryption_key is not None:
            aes = AESCipher(encryption_key)
            self.reason = aes.encrypt(reason)
        else:
            self.reason = reason

    def __str__(self):
        return f"Id: {self.id} - {self.sender} paid {self.receiver} {self.amount}$ for reason: {self.reason}"
