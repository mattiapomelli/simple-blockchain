from auth import Auth
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain
from exceptions import OverspendingError
from aes import AESCipher
from printer import Printer
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError
from currency import Currency
import random
import string

def main():
    blockchain = Blockchain()
    auth = Auth()
    currency = Currency()
    print(currency)
    commands = {
        "s": "signup",
        "l": "login",
        "u": "check logged user",
        "c": "check current exchange rate",
        "q": "quit application"
    }

    commands_after_login = {
        "t": "perform transaction",
        "pt": "print pending transactions",
        "m": "mine a block",
        "b": "print blockchain",
        "ba": "print user balance",
        "dt": "decrypt the reason of a transaction"
    }
    
    print("List of commands: ")
    for key, value in commands.items():
        colored_key = Printer.colored(245, 185, 66, key)
        colored_value = Printer.colored(200, 200, 200, value)
        print(f"{colored_key} - {colored_value}")
    
    print("Commands available after login: ")
    for key, value in commands_after_login.items():
        colored_key = Printer.colored(245, 185, 66, key)
        colored_value = Printer.colored(200, 200, 200, value)
        print(f"{colored_key} - {colored_value}")
    
    while True:
        text = '>>> Select a command to execute: '
        colored_text = Printer.colored(135, 185, 199, text)
        command = input(colored_text)

        # signup
        if command == 's':
            username = input('Enter username: ')
            set_rand_pass = input('do you want to set a rand password (y/n)')
        
            if set_rand_pass == 'y':
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 32))
                Printer.success(f"random generated password: {password}")
            else:
                password = input('Enter password: ')
            try:
                auth.signup(username, password)
                blockchain.reward(username, "initial reward")
                Printer.success(f"Created new user: {username}")
                Printer.success(f"Signed in as {username}")
            except ConflictError:
                Printer.error("Username is taken")
        
        # login
        elif command == 'l':
            username = input('Enter username: ')
            password = input('Enter password: ')
            try:
                auth.signin(username, password)
                Printer.success(f"Signed is as {username}")
            except NotFoundError:
                Printer.error(f"No user exists with username {username}")
            except InvalidCredentialsError:
                Printer.error("Password is not correct")
        #check current currency
        elif command == 'c':
            Printer.info(currency)

        # check logged user
        elif command == 'u':
            if auth.is_logged():
                Printer.info("Logged user: " + auth.user.username)
            else:
                Printer.info("No user is logged in")

        # perform a new transaction
        elif command == 't':
            if not auth.is_logged():
                Printer.error("You must be logged in to perform a transaction")
                continue

            receiver_username = input('Enter receiver username: ')

            if receiver_username == auth.user.username:
                Printer.error("You can't send money to yourself")
                continue

            receiver = users_db.find_by_username(receiver_username)

            if receiver is None:
                Printer.error("No user with username " + receiver_username + " exists")
                continue

            amount = input('Enter amount: ')
            if not amount.isdigit() or int(amount) <= 0:
                Printer.error("Amount must be a positive integer")
                continue

            reason = input('Enter reason: ')
            to_encrypt = input("Do you want to encrypt the reason of the transaction? (y/n) ")
            key = None

            if to_encrypt == 'y':
                key = input('Enter a key for encrypting the transiction reason: ')

            transaction = Transaction(
                auth.user.username,
                receiver_username,
                int(amount),
                reason,
                encryption_key=key
            )

            try:
                blockchain.add_transaction(transaction)
                Printer.success("Added transaction to pending transactions")
            except OverspendingError:
                Printer.error("You don't have enough money to perform this transaction")
        
        # print pending transactions
        elif command == 'pt':
            Printer.info("Pending transactions: [", end="")
            if len(blockchain.pending_transactions) > 0:
                print()

            for t in blockchain.pending_transactions:
                print(f"   {str(t)}")

            Printer.info("]")

        # decrypt reason of a transaction
        elif command == 'dt':
            if not auth.is_logged():
                Printer.error("You must be logged in to decrypt a transaction")
                continue

            transaction_id = input("Enter transaction id: ")
            transaction = blockchain.find_transaction_by_id(int(transaction_id))

            if transaction is None:
                Printer.error(f"No transaction found with id {transaction_id}")
                continue
            
            Printer.info("Transaction: ", end="")
            print(transaction)
            
            if not transaction.is_encrypted:
                Printer.error("The transaction is not encrypted")
                continue
            
            key = input("Enter key to decrypt transaction reason: ")
            aes = AESCipher(key)

            try:
                reason = aes.decrypt(transaction.reason)
                Printer.info("Reason of the transaction: ", end="")
                print(reason)
            except:
                Printer.error("Invalid key")

        # mine a new block
        elif command == 'm':
            if not auth.is_logged():
                Printer.error("You must be logged to mine a block")
                continue

            Printer.info("Mining a new block with pending transactions...")
            blockchain.mine(auth.user.username)
            Printer.success("Block has been mined and added to the chain")
            Printer.success("You have been rewarded with " + str(blockchain.reward_amount) + "$")

        # print the blockchain
        elif command == 'b':
            Printer.info("Blockchain:")
            print(blockchain)

        # check logged user's balance
        elif command == 'ba':
            if not auth.is_logged():
                Printer.error("You must be logged to check you balance")
                continue
            
            Printer.info("Your balance is: ", end="")
            print(f"{str(blockchain.calculate_balance(auth.user.username))}$")

        # quit application
        elif command == 'q':
            Printer.info("Quitting application...")
            return

        # invalid command
        else:
            Printer.error('Invalid command')

if __name__ == "__main__":
    main()
