from flask import Flask, render_template, request, jsonify

from hashlib import sha256
import json
import time

class Block:
    def __init__(self, index, transactions, timestamp, previous_hash):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys = True)
        return sha256(block_string.encode()).hexdigest()

class Blockchain:
    difficulty = 2

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], time.time(), "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    def last_block(self):
        return self.chain[-1]
    
    def new_transaction(self, new_transaction):
        self.unconfirmed_transactions.append(new_transaction)

    def mine(self):
        if not len(self.unconfirmed_transactions):
            return False

        last_block = self.last_block()

        new_block = Block(index = last_block.index + 1, 
                          transactions = self.unconfirmed_transactions,
                          timestamp = time.time(),
                          previous_hash = last_block.hash)

        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return new_block.index

    def add_block(self, new_block, proof):
        blockchain_previous_hash = self.last_block().hash

        if blockchain_previous_hash != new_block.previous_hash:
            return False
        
        if not self.is_valid(new_block, proof):
            return False
        
        new_block.hash = proof
        self.chain.append(new_block)
        return True
        
    def is_valid(self, new_block, proof):
        return (proof.startswith('0' * self.difficulty) and 
                proof == new_block.compute_hash()) 
        
    def proof_of_work(self, block):
        block.nonce = 0

        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash
    
blockchain = Blockchain()

print(blockchain.last_block().__dict__)

blockchain.new_transaction({'author' : 'Eto', 'content' : 'qwe'})

blockchain.mine()

print(blockchain.last_block().__dict__)

blockchain.new_transaction({'author' : 'Eto', 'content' : 'pizdec'})

blockchain.mine()

print(blockchain.last_block().__dict__)

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test():
    data = request.get_json()
    print(data)
    return jsonify(data), 201

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    data = request.get_json()
    
    blockchain.new_transaction(data)

    return {'desc' : 'new transaction is added'}, 200

@app.route('/mine', methods=['GET'])
def mine():
    blockchain.mine()

    return {'desc' : 'minig is comlete'}, 201

@app.route('/chains', methods=['GET'])
def chains():
    data = []

    for block in blockchain.chain:
        data.append(block.__dict__)

    return jsonify(data), 203

@app.route('/transactions', methods=['GET'])
def transactions():
    data = blockchain.unconfirmed_transactions

    return jsonify(data), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)