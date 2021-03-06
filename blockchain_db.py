import json
from block import Block
from transaction import Transaction
from Crypto.Hash import SHA256
from printer import Printer
from rsa import RSACipher
from certificates import CA
import sys

class BlockchainDB:
    """
    This class represents a service to interact with the database storing the blockchain content.
    The database is represented by a json file.

    db_path: path to the file storing blockchain information
    db_hash_path: path to the file storing the hash of the db
    """

    db_path = 'db/blockchain.json'
    db_hash_path = 'hashes/blockchain-hash.txt'
    db_hash__signature_path = 'hashes/blockchain-hash-signature.txt'

    def get_blockchain(self):
        """
        Opens the file representing the db and returns its content
        after deserializing it.
        Also returns wheter the db file is valid or has been corrupted.
        """
        if len(sys.argv) > 1 and sys.argv[1] == "--reset":
            self.reset()

        file = open(self.db_path)
        is_format_corrupted = False # indicates wheter the db file has been corrupted in a way that cannot be parsed as JSON anymore
        is_valid = True # indicates wheter the db file is valid or has been corrupted

        # Check if a certificate for the database is already present, otherwise create it
        stored_cert = CA.get_certificate("blockchain-db")
        if stored_cert is None:
            self.cert = CA.create_certificate("blockchain-db")
        else:
            self.cert = stored_cert
        
        # try:
        try:
            data = json.load(file)
        except:
            is_format_corrupted = True
            data = file.read()

        # Compute the hash of the file content
        db_hash = SHA256.new(str(data).encode()).hexdigest()
        
        hash_file = open(self.db_hash_path, 'r')
        signature_file = open(self.db_hash__signature_path, 'r')
        
        # Get the stored hash
        stored_hash = hash_file.read()
        # Get the stored signature of the hash
        signature = signature_file.read()

        # Verify that the signature of the hash is valid, using the CA public key
        db_public_key = CA.get_public_key(self.cert)

        is_signature_valid = RSACipher.verify(stored_hash, signature, db_public_key)
        if not is_signature_valid:
            is_valid = False
            Printer.error("Blockchain database's hash or signature have been corrupted: signature is not valid")

        if db_hash != stored_hash:
            is_valid = False
            Printer.error("Blockchain database has has been corrupted: hashes don't match")

        if is_valid:
            self.save_db_hash(data)
        
        if is_format_corrupted:
            return [], False

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
        
        return blocks, is_valid

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
        self.save_db_hash(serialized_chain)
        file.close()
    
    def save_db_hash(self, serialized_chain):
        hash_file = open(self.db_hash_path, 'w')
        signature_file = open(self.db_hash__signature_path, 'w')

        db_hash = SHA256.new(str(serialized_chain).encode()).hexdigest()
        
        signed_hash = RSACipher.sign(db_hash, CA.get_private_key("blockchain-db"))
        
        hash_file.write(db_hash)
        signature_file.write(signed_hash)

    def reset(self):
        """
        Drop all the elements in the db
        """
        file = open(self.db_path, 'w')
        file.write(str([]))
        self.save_db_hash(str([]))
        file.close()

# block database controller that will be used to perform operations on the db
blocks_db = BlockchainDB()
