from blockchain import Blockchain
from user import User

user1 = User('mattia')
user2 = User('julian')
user3 = User('lukas')
print(user1)
print(user2)
print(user3)

blockchain = Blockchain()

t1 = user1.perform_transaction(user2.username, 30)
t2 = user2.perform_transaction(user3.username, 20)
t3 = user3.perform_transaction(user1.username, 45)

blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.add_transaction(t3)
blockchain.mine()

print(blockchain)
