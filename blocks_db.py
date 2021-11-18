import json
from block import Block
from transaction import Transaction

class BlockDB:
    db = None
    db_path = 'db/blockchain.json'

    def __init__(self):
        """
        Opens the file representing the db and stores its content in the db attribute.
        If there is an error opening the file, it resets the db to be empty.
        """
        file = open(self.db_path)
        
        try:
            data = json.load(file)
            blocks = []

            for b in data:
                transactions = []
                for t in b['transactions']:
                    transaction = Transaction(
                        t['sender'],
                        t['receiver'],
                        t['amount'],
                        t['reason'],
                        t['is_encrypted']
                    )
                    transaction.timestamp = t['timestamp']
                    transactions.append(transaction)

                block = Block(
                    b["index"],
                    transactions,
                    b["previous_hash"]
                )

                block.timestamp = b['timestamp']
                blocks.append(block)

            self.db = blocks
            print(self.db)

        except Exception as e:
            print(e)
            self.reset()

    def add(self, block):
        """
        Creates a new user and adds it to the database (writes the new list of users to the file)
        Returns the created user
        """
        self.db.append(block)

        file = open(self.db_path, 'w')
        serialized_db = [b.__dict__ for b in self.db]
        serialized_db = []

        for b in self.db:
            serialized_block = dict(b.__dict__)
            serialized_transactions = []
            
            for t in b.transactions:
                serialized_transactions.append(t.__dict__)

            serialized_block['transactions'] = serialized_transactions
            serialized_db.append(serialized_block)

        json.dump(serialized_db, file, indent=4)

    def reset(self):
        """
        Drop all the elements in the db
        """
        file = open(self.db_path, 'w')
        file.write(str([]))
        self.db = []

    def __str__(self):
        res = ""
        for user in self.db:
            res += str(user)
        return res

# block database controller that will be used to perform operations on the db
blocks_db = BlockDB()
