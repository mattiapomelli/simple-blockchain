from block import Block

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        return Block(0, [], "000")

    def add_block(self, block):
        self.chain.append(block)

    def proof_of_work(self, block):
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)

    def mine(self):
        # TODO: add mining reward: create transaction to miner and add it to pending transactions
        new_block = Block(
            index=self.last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=self.last_block.compute_hash()
        )

        self.proof_of_work(new_block)
        self.add_block(new_block)

    @property
    def last_block(self):
        return self.chain[-1]

    def __str__(self):
        res = ""
        for block in self.chain:
            res += str(block)
        return res
