from blockchain import Blockchain
from users_db import users_db

users_db.reset()

user1 = users_db.create_user('mattia', '12345678')
user2 = users_db.create_user('julian', 'test_test')
user3 = users_db.create_user('lukas', 'strong_password')

blockchain = Blockchain()

t1 = user1.perform_transaction(user2.username, 30)
t2 = user2.perform_transaction(user3.username, 20)
t3 = user3.perform_transaction(user1.username, 45)

blockchain.add_transaction(t1)
blockchain.add_transaction(t2)
blockchain.add_transaction(t3)
blockchain.mine()

print(blockchain)
