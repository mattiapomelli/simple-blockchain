from hashlib import sha256
from time import time

class Block:
    def __init__(self, index, data, previous_hash):
        self.index = index
        self.data = data
        self.timestamp = time()
        self.previous_hash = previous_hash
        self.nonce = 0
    
    def hash(self):
        h = sha256()
        h.update(
            str(self.data).encode('utf-8') +
            str(self.timestamp).encode('utf-8') +
            str(self.previous_hash).encode('utf-8') +
            str(self.nonce).encode('utf-8')
        )

        return h.hexdigest()

    def __str__(self):
        return (
            "Index: " + str(self.index) +
            "\nTimestamp: " + str(self.timestamp) +
            "\nData: " + str(self.data) +
            "\nPrevious Hash: " + str(self.previous_hash) +
            "\nHash: " + str(self.hash()) +
            "\n----------"
        )

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "000")

    def add_block(self, block):
        self.chain.append(block)
