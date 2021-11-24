from time import time
from printer import Printer

class Transaction:
    """
    This class represents a transaction of the cryptocurrency.
    Transactions have to be stored inside a block in the chain to be considered official.
    
    next_id: incremented every time a new transaction is created to get a new id
    """
    next_id = 0

    def __init__(self, sender, receiver, amount, reason, is_encrypted = False):
        """
        id: id of the transaction
        sender: username of the user which is sending the money.
                Is None if the transaction has no sender (this happens for reward transactions)
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
        self.reason = reason
        self.timestamp = time()
        self.is_encrypted = is_encrypted

    def __str__(self):
        colored_receiver = Printer.get_info(self.receiver)
        
        if self.sender is None:
            main_text = f"{colored_receiver} received"
        else:
            colored_sender = Printer.get_info(self.sender)
            main_text = f"{colored_sender} paid {colored_receiver}"

        return f"Id: {self.id} - {main_text} {self.amount}$, reason: {self.reason}"
