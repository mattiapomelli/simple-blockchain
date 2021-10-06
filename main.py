from blockchain import Blockchain
from block import Block
from transaction import Transaction

blockchain = Blockchain()

t1 = Transaction('Bob', 'Billy', 30)
t2 = Transaction('Carl', 'Bob', 20)
t3 = Transaction('Billy', 'Pol', 45)

blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.add_transaction(t3)
blockchain.mine()

print(blockchain)