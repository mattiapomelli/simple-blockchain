import json
from block import Block
from transaction import Transaction

class BlockDB:
    db_path = 'db/blockchain.json'

    def get_blockchain(self):
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
                    transaction.signature = t['signature']
                    transactions.append(transaction)

                block = Block(
                    b["index"],
                    transactions,
                    b["previous_hash"],
                    b["nonce"]
                )

                block.timestamp = b['timestamp']
                blocks.append(block)
            
            return blocks
        except Exception:
            self.reset()
            return []
        finally:
            file.close()

    def write_blockchain(self, chain):
        """
        Writes the blockchain to the database (file)
        """
        file = open(self.db_path, 'w')
        serialized_chain = []

        for b in chain:
            serialized_block = dict(b.__dict__)
            serialized_transactions = []
            
            for t in b.transactions:
                serialized_transactions.append(t.__dict__)

            serialized_block['transactions'] = serialized_transactions
            serialized_chain.append(serialized_block)

        json.dump(serialized_chain, file, indent=4)
        file.close()

    def reset(self):
        """
        Drop all the elements in the db
        """
        file = open(self.db_path, 'w')
        file.write(str([]))
        file.close()

# block database controller that will be used to perform operations on the db
blocks_db = BlockDB()
