from auth import Auth
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain
from exceptions import InvalidBlockchainError, OverspendingError
from printer import Printer
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError
from currency import Currency
from certificates import CA
from rsa import RSACipher
from aes import AESCipher
from Crypto.Random import get_random_bytes
from base64 import b64encode
import random
import string
import os
import sys

def main():
    blockchain = Blockchain()
    auth = Auth()
    currency = Currency()

    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        for c in os.listdir("certificates"):
            if c not in ["ca-cert.cer", "blockchain-db-cert.cer", "users-db-cert.cer"]:
                os.remove(f"certificates/{c}")

        for c in os.listdir("keys"):
            if c not in ["ca-private.key", "blockchain-db-private.key", "users-db-private.key"]:
                os.remove(f"keys/{c}")

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
            "dt": "decrypt the reason of a transaction",
            "pd": "print personal data"
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
                Printer.info(f"This is your random generated password: ", end='')
                print(password)
            else:
                password = input('Enter password: ')
            
            email = input('Enter email address: ')
            phone_nr = input('Enter phone number: ')
            address = input('Enter address for correspondence: ')
            
            try:
                auth.signup(username, password, email, phone_nr, address)
                blockchain.reward(username, "initial reward")

                # Create a public key certificate for the new user
                CA.create_certificate(username)                

                Printer.success("Created new user: ", end='')
                Printer.info(username)
                Printer.success(f"Your private data has been encrypted")
                Printer.success("Created new certificate for ", end='')
                Printer.info(username)
                Printer.success(f"Signed in as ", end='')
                Printer.info(username)
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
                
        # print personal data
        elif command == 'pd':
            if not auth.is_logged():
                Printer.error("You must be logged in to see your personal data")
                continue

            key = input("Enter your password to see your personal data: ")

            try:
                personal_data = auth.decrypt_personal_data(username, key)

                Printer.info("email: ", end='')
                print(personal_data["email"])
                Printer.info("phone number: ", end='')
                print(personal_data["phone_nr"])
                Printer.info("address : ", end='')
                print(personal_data["address"])
            except: 
                Printer.error("Wrong password")

        # check logged user
        elif command == 'u':
            if auth.is_logged():
                Printer.info("Logged user: " + auth.user.username)
            else:
                Printer.info("No user is logged in")

        # check current currency exchange rate
        elif command == 'e':
            Printer.info(currency)

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

            # ---- HYBRID ENCRYPTION ----
            # Get the certificate of the receiver
            receiver_cert = CA.get_certificate(receiver_username)

            # Verify the certificate of the receiver
            CA.verify_certificate(receiver_cert)
            
            # Get the receiver public key from his/her certificate
            receiver_pub_key = CA.get_public_key(receiver_cert)

            # Generate a random session key
            session_key_bytes = get_random_bytes(16)
            # Convert it from bytes to string
            session_key = b64encode(session_key_bytes).decode("utf-8")

            # Asymmetrically encrypt the session key with the receiver's public key
            encrypted_session_key = RSACipher.encrypt(session_key, receiver_pub_key)

            # Symmetrically encrypt the reason of the transaction with the session key
            encrypted_reason = AESCipher.encrypt(reason, session_key)

            # Append the encrypted session key to the encrypted reason, so that the receiver
            # can obtain it
            stored_reason = encrypted_reason + encrypted_session_key

            transaction = Transaction(
                auth.user.username,
                receiver_username,
                int(amount),
                stored_reason,
                is_encrypted= True
            )

            try:
                blockchain.add_transaction(transaction)

                Printer.success("Transaction reason has been encrypted with public key of ", end='')
                Printer.info(receiver_username, end='')
                Printer.success(". He/She's the only one who can see it.")
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
            
            # ---- HYBRID DECRYPTION ----
            # Get private key of the logged user
            private_key = CA.get_private_key(auth.user.username)

            # Extract the encrypted session key from the stored transaction reason
            encrypted_session_key = transaction.reason[-344:]

            # Extract the encrypted reason from the stored transaction reason
            encrypted_reason = transaction.reason[:-344]

            try:
                # Asymmetrically decrypt the session key with the private key of the logged user
                decrypted_session_key = RSACipher.decrypt(encrypted_session_key, private_key)

                # Symmetrically decrypt the reason of the transaction with the obtainde session key
                decrypted_reason = AESCipher.decrypt(encrypted_reason, decrypted_session_key)
                
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
            
            try:
                blockchain.mine(auth.user.username)
                Printer.success("Block has been mined and added to the chain")
                Printer.success("You have been rewarded with " + str(blockchain.reward_amount) + "$")
            except InvalidBlockchainError as e:
                Printer.error("Invalid Blockchain: "+ str(e))
                exit()

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
