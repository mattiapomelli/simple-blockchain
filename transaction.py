from time import time
from Crypto.Hash import SHA256
from rsa import RSACipher
from printer import Printer
from certificates import CA

class Transaction:
    """
    This class represents a transaction of the cryptocurrency.
    Transactions have to be stored inside a block in the chain to be considered official.
    Transactions are signed with the private key of the sender, creator of the transaction, to 
    prove their authorship and integrity.
    
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
        signature: signature of the transaction
        """
        self.id = Transaction.next_id
        Transaction.next_id += 1
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.reason = reason
        self.timestamp = round(time() * 1000)
        self.is_encrypted = is_encrypted
        self.signature = None

    def is_reward_transaction(self):
        """
        Returns True if the transaction is a reward transaction, False otherwise.
        Reward transactions are identified by the fact that they don't have a sender.
        """
        return self.sender is None

    def compute_hash(self):
        """
        Computes the hash of the transaction, hashing with SHA256 the transaction information
        """
        hash = SHA256.new(
            str(self.id).encode() + 
            self.sender.encode() +
            self.receiver.encode() +
            str(self.amount).encode() +
            str(self.timestamp).encode()
        )
        
        return hash.hexdigest()

    def sign(self):
        """
        Signs the transaction (after having computed its hash) with the private key of the sender
        """
        # Get the private key of the sender of the transaction
        sender_private_key = CA.get_private_key(self.sender)

        # Compute the hash of the transaction
        hash = self.compute_hash()

        # Sign the hash with the sender's private key
        self.signature = RSACipher.sign(hash, sender_private_key)

    def is_valid(self):
        """
        Verifies that the transaction is valid by verifying its signature.
        Reward transactions are not signed so this verification can't happen
        """
        # If is a reward transaction don't verify the signature
        if self.is_reward_transaction():
            return True

        # If the transaction is not signed then it's not valid
        if self.signature is None:
            return False
        
        # Get certificate of sender
        sender_cert = CA.get_certificate(self.sender)
        # Get the public key of sender from his/her certificate
        sender_public_key = CA.get_public_key(sender_cert)

        # Verify the signature of the transaction with the sender's public key
        is_valid = RSACipher.verify(self.compute_hash(), self.signature, sender_public_key)
        return is_valid

    def __str__(self):
        colored_receiver = Printer.get_info(self.receiver)
        
        if self.sender is None:
            main_text = f"{colored_receiver} received"
        else:
            colored_sender = Printer.get_info(self.sender)
            main_text = f"{colored_sender} paid {colored_receiver}"

        return f"Id: {self.id} - {main_text} {self.amount}$, reason: {self.reason}, Signature: {self.signature}"
