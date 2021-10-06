from hashlib import sha256
from time import time

class Block:
    def __init__(self, index, transactions, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.nonce = 0
    
    def compute_hash(self):
        hash = sha256()
        hash.update(
            str(self.transactions).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )

        return hash.hexdigest()

    def __str__(self):
        return (
            "\nIndex: " + str(self.index) +
            "\nTimestamp: " + str(self.timestamp) +
            "\nTransactions: " + str([str(t) for t in self.transactions]) +
            "\nPrevious Hash: " + str(self.previous_hash) +
            "\nHash: " + str(self.compute_hash()) +
            "\n----------"
        )
