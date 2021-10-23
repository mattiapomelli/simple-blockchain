from hashlib import sha256
from time import time

class Block:
    """
    This class represents a block in the chain.
    Blocks store information about transactions that have been executed.
    Every block is identified by an hash, computed hashing the block's
    information with an hashing function.
    """

    def __init__(self, index, transactions, previous_hash):
        """
        index: index of the block in the chain
        transactions: transactions stored in the block
        timestamp: time at which the block was created
        previous_hash: hash of the previous block in the chain
        nonce: nonce for computing the proof of work
        """
        self.index = index
        self.transactions = transactions 
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.nonce = 0
    
    def compute_hash(self):
        """
        Computes the hash of the block, hashing with SHA256
        the block data (transactions), the hash of the previous block,
        the timestamp and the nonce
        """
        hash = sha256()
        hash.update(
            str(self.transactions).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )

        return hash.hexdigest()

    def __str__(self):
        transactions_str = "["
        for t in self.transactions:
            transactions_str += f"\n   {str(t)}"
        
        if len(self.transactions) > 0:
            transactions_str += "\n"

        transactions_str += "]"

        return (
            f"\nIndex: {str(self.index)}"
            f"\nTimestamp: {str(self.timestamp)}"
            f"\nTransactions: {transactions_str}"
            f"\nPrevious Hash: {str(self.previous_hash)}"
            f"\nHash: {str(self.compute_hash())}"
            "\n----------"
        )
