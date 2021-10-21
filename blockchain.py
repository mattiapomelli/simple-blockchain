from block import Block
from transaction import Transaction
from exceptions import OverspendingError

class Blockchain:
    """
    This class represents a blockchain, a chain of blocks.
    The blocks are linked together by having each block store the hash of
    the previous block in the chain

    difficulty: number of consecutive 0s that every hash must begin with, determines
                how complex is to mine a new block 

    reward: amount of cryptocurrency that a user gets paid for mining a new block
    """

    difficulty = 2
    reward = 10

    def __init__(self):
        """
        chain: stores the blocks of the blockchain
        pending_transactions: transactions that have not been inserted in a block yet.
                              they have to be included in a block to become actually official
        """
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        """
        Creates the genesis block, the first lock of the chain.
        This block doesn't store any transactions and has an arbitrary previous hash
        """
        return Block(0, [], "000")

    def add_block(self, block):
        """
        Adds a new block to the end of the chain
        """
        # TODO: check that the block is valid
        self.chain.append(block)

    def proof_of_work(self, block):
        """
        Performs the proof of work process for the given block:
        Increases the block's nonce by 1 until the block hash is valid, that is
        it starts with the number of consecutive 0s determined by the difficulty
        """
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    def add_transaction(self, transaction):
        """
        Adds a new transactions to the pending transactions.
        Before adding the new transaction, checks if it's not an overspending transaction:
        the sender has enough money to perform the transaction, so his balance is at least as much
        as the transaction amount.
        If the transaction is overspending, raises OverspendingError.
        If the transaction has no sender, it means that it is a mining reward transaction, and so
        no balance should be checked.
        """
        sender_username = transaction.sender

        if sender_username:
            # it's not a mining reward transaction
            sender_balance = self.calculate_balance(sender_username)

            if sender_balance < transaction.amount:
                raise OverspendingError

        self.pending_transactions.append(transaction)

    def mine(self, reward_username):
        """
        reward_username: username of the user that is mining the block and that should be rewarded

        Mines a new block:
        - creates a new transaction for rewarding the user mining the block. This particular transaction
          has no sender so it's simply indicated by an empty string
        - adds the mining reward transaction to the pending transactions
        - stores the pending transactions in the block
        - computes its proof of work
        - adds it to the chain

        The new block will have:
        - index: equal to the index of the last block in the chain + 1
        - previous_hash: hash of the last block in the chain
        """
        reward_transaction = Transaction('', reward_username, self.reward)
        self.add_transaction(reward_transaction)

        # TODO: check maximum number of transactions in a block 
        new_block = Block(
            index=self.last_block.index + 1,
            transactions=self.pending_transactions,
            previous_hash=self.last_block.compute_hash()
        )

        self.proof_of_work(new_block)
        self.add_block(new_block)
        self.pending_transactions = []

    def calculate_balance(self, username):
        """
        Calculates the amount of cryptocurrency owned by the user with the given username.
        A cryptocurrency is essentialy an history of transactions.
        So the only way to know an user's balance is to iterate over all the blocks and
        check the full history of transactions that involved the user.
        """
        balance = 0

        for block in self.chain:
            for transaction in block.transactions:
                if transaction.receiver == username:
                    balance += transaction.amount
                elif transaction.sender == username:
                    balance -= transaction.amount
        
        return balance

    @property
    def last_block(self):
        """
        Returns the last block in the chain
        """
        return self.chain[-1]

    def __str__(self):
        res = ""
        for block in self.chain:
            res += str(block)
        return res
