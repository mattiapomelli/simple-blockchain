from block import Block

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "000")

    def add_block(self, block):
        block.previous_hash = self.chain[-1].compute_hash()
        self.proof_of_work(block)
        self.chain.append(block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def __str__(self):
        res = ""
        for block in self.chain:
            res += str(block)
        return res
