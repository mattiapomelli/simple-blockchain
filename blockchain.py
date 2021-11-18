from block import Block
from transaction import Transaction
from exceptions import OverspendingError, InvalidBlockchainError
from blocks_db import blocks_db

class Blockchain:
    """
    This class represents a blockchain, a chain of blocks.
    The blocks are linked together by having each block store the hash of
    the previous block in the chain

    difficulty: number of consecutive 0s that every hash must begin with, determines
                how complex is to mine a new block 

    reward_amount: amount of cryptocurrency that a user gets paid for mining a new block
    """

    difficulty = 3
    reward_amount = 10

    def __init__(self):
        """
        chain: stores the blocks of the blockchain
        pending_transactions: transactions that have not been inserted in a block yet.
                              they have to be included in a block to become actually official
        """
        # self.chain = []
        # self.create_genesis_block()
        
        saved_blockchain = blocks_db.db

        if len(saved_blockchain) == 0:
            self.chain = []
            self.create_genesis_block()
            print('1')
        else:
            self.chain = saved_blockchain
            print('2')

        self.pending_transactions = []

    def create_genesis_block(self):
        """
        Creates the genesis block, the first lock of the chain.
        This block doesn't store any transactions and has an arbitrary previous hash
        """
        genesis_block = Block(0, [], "000")
        self.proof_of_work(genesis_block)
        self.add_block(genesis_block)

    def add_block(self, block):
        """
        Adds a new block to the end of the chain.
        After adding the new block verifies that the chain is still valid.
        If not, throws InvalidBlockchainError
        """
        self.chain.append(block)
        blocks_db.add(block)
        
        if not self.is_chain_valid():
            raise InvalidBlockchainError
    
    def is_chain_valid(self):
        """
        Returns True if the blockchain is valid, False otherwise.
        A blockchain is valid if:
        - every block's hash is valid, so it starts with a consecutive number of 0s given by
          the blockchain's difficulty
        - the blocks are correctly chained together: for every block except the first one, the
          value of previous_hash is equal to the hash of the previous block in the chain
        """
        for index, block in enumerate(self.chain):
            hash = block.compute_hash()

            if not hash.startswith('0' * self.difficulty):
                return False
            
            if index > 0:
                previous_block = self.chain[index-1]
                if not block.previous_hash == previous_block.compute_hash():
                    return False
        
        return True

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

    def reward(self, username, reward_reason):
        """
        Creates a new reward transaction and adds it to the pending transactions.

        - username: username of the user which will receive a reward transaction
        - reward_reason: reason of the reward transaction

        A reward transaction can happen in two situations:
        - a user mines a new block and it gets rewarded for this
        - when a new user signs up gets an initial amount of money

        Reward transactions have no sender. Thus, the sender is set to None.
        """
        reward_transaction = Transaction(None, username, self.reward_amount, reward_reason)
        self.add_transaction(reward_transaction)

    def mine(self, reward_username):
        """
        reward_username: username of the user that is mining the block and that should be rewarded

        Mines a new block:
        - rewards the user for having mined a new block
        - stores the pending transactions in the block
        - computes its proof of work
        - adds it to the chain

        The new block will have:
        - index: equal to the index of the last block in the chain + 1
        - previous_hash: hash of the last block in the chain
        """
        self.reward(reward_username, "mining reward")

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
    
    def find_transaction_by_id(self, transaction_id):
        """
        Returns the transaction with the given id, if it exists in the blockchain.
        Otherwise returns None
        """
        for block in self.chain:
            for transaction in block.transactions:
                if transaction.id == transaction_id:
                    return transaction
        
        return None

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
