from auth import Auth
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain
from exceptions import OverspendingError
from aes import AESCipher
from printer import Printer
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError
from currency import Currency
from certificates import CA
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import random
import string
import ast

def main():
    blockchain = Blockchain()
    auth = Auth()
    currency = Currency()

    def print_list_of_commands():
        commands = {
            "s": "signup",
            "l": "login",
            "u": "check logged user",
            "c": "print list of commands",
            "e": "check currency exchange rate",
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
            Printer.info(key, end=' - ')
            print(value)
        
        print("Commands available after login: ")
        for key, value in commands_after_login.items():
            Printer.info(key, end=' - ')
            print(value)
    
    Printer.info(currency.__str__())
    print_list_of_commands()

    while True:
        Printer.cyan(">>> Select a command to execute: ", end="")
        command = input()

        # print list of commands:
        if command == 'c':
            print_list_of_commands()

        # signup
        elif command == 's':
            username = input('Enter username: ')
            set_rand_pass = input('Do you want to set a random password? (y/n) ')
        
            if set_rand_pass == 'y':
                password = ''.join(random.choices(string.ascii_lowercase + string.digits, k = 10))
                Printer.success(f"This is your random generated password: {password}")
            else:
                password = input('Enter password: ')
            
            aes = AESCipher(password)
            email = aes.encrypt(input('type email address: '))

            
            try:
                auth.signup(username, password, email)
                
                

                blockchain.reward(username, "initial reward")

                CA.create_certificate(username)                

                Printer.success(f"Created new user: {username}")
                Printer.success(f"Created new certificate for {username}")
                Printer.success(f"Signed in as {username}")
            except ConflictError:
                Printer.error("Username is taken")
        
        # login
        elif command == 'l':
            username = input('Enter username: ')
            password = input('Enter password: ')
            try:
                auth.signin(username, password)
                Printer.success(f"Signed in as {username}")
            except NotFoundError:
                Printer.error(f"No user exists with username {username}")
            except InvalidCredentialsError:
                Printer.error("Password is not correct")
                
        #print email
        elif command == 'email':
            key = input("enter password to decrypt email: ")
            if key==password:
                aes = AESCipher(key)
                decrypted_email = aes.decrypt(auth.user.email)
                Printer.info("email:  ", end="")
                print(decrypted_email)
            else: 
                Printer.error("wrong password")
                Printer.error("crypted mail look like this: ")
                print(auth.user.email)
            
            


        # check current currency exchange rate
        elif command == 'e':
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

            if to_encrypt == 'y':
                # Get the certificate of the receiver
                receiver_cert = CA.get_certificate(receiver_username)

                # TODO: verify cert

                # Get the receiver public key from his/her certificate
                receiver_pub_key = CA.get_public_key(receiver_cert)

                # Create a new RSA cipher from the receiver's public key
                key = RSA.importKey(extern_key=receiver_pub_key)
                cipher = PKCS1_OAEP.new(key)

                # Encrypt the reason of the transaction
                encrypted_reason = cipher.encrypt(reason.encode())

                # Convert from bytes to string to make JSON serializable
                reason = str(encrypted_reason)

            transaction = Transaction(
                auth.user.username,
                receiver_username,
                int(amount),
                reason,
                is_encrypted= True if to_encrypt == 'y' else False
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
            
            # Get private key of the logged user
            private_key = CA.get_private_key(auth.user.username)

            # Create a new RSA cipher from the logged user's private key
            key = RSA.importKey(extern_key=private_key)
            cipher = PKCS1_OAEP.new(key)

            try:
                # Convert from string to bytes
                encrypted_reason = ast.literal_eval(transaction.reason)

                # Decrypt the reason of the transaction and convert from btyes to string
                decrypted_reason = cipher.decrypt(encrypted_reason).decode()
                
                Printer.info("Reason of the transaction: ", end="")
                print(decrypted_reason)
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
