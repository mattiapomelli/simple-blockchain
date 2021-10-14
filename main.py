from blockchain import Blockchain
from block import Block
from transaction import Transaction
from user import User

user1 = User('mattia')
user2 = User('julian')
user3 = User('lukas')
print(user1)
print(user2)
print(user3)

blockchain = Blockchain()

t1 = Transaction(user1.username, user2.username, 30)
t2 = Transaction(user2.username, user3.username, 20)
t3 = Transaction(user3.username, user1.username, 45)

blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.add_transaction(t3)
blockchain.mine()

print(blockchain)
