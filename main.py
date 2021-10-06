from blockchain import Blockchain
from block import Block

blockchain = Blockchain()
b1 = Block(1, 'some data', '111')

blockchain.add_block(b1)

print(blockchain.chain)