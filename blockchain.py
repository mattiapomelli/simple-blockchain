from block import Block

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, "Genesis", "000")

    def add_block(self, block):
        self.chain.append(block)

    def __str__(self):
        res = ""
        for block in self.chain:
            res += str(block)
        
        return res
