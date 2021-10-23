from time import time
from aes import AESCipher
from printer import Printer

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
        is_encrypted: wheter the reason of the transaction is encrypted or not
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
            self.is_encrypted = True
        else:
            self.reason = reason
            self.is_encrypted = False

    def __str__(self):
        colored_sender = Printer.colored(255, 209, 92, self.sender)
        colored_receiver = Printer.colored(255, 209, 92, self.receiver)
        return f"Id: {self.id} - {colored_sender} paid {colored_receiver} {self.amount}$ for reason: {self.reason}"
