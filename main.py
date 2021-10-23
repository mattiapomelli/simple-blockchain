from auth import Auth
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain
from exceptions import OverspendingError
from aes import AESCipher
from printer import Printer

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{}\033[38;2;255;255;255m".format(r, g, b, text)

def main():
    blockchain = Blockchain()
    auth = Auth()

    commands = {
        "s": "signup",
        "l": "login",
        "u": "check logged user",
        "q": "quit application"
    }

    commands_after_login = {
        "t": "perform transaction",
        "pt": "print pending transactions",
        "m": "mine a block",
        "b": "print blockchain",
        "ba": "print user balance",
    }
    
    print("List of commands: ")
    for key, value in commands.items():
        print(f"{colored(245, 185, 66, key)} - {colored(190, 210, 210, value)}")
    
    print("Commands available after login: ")
    for key, value in commands_after_login.items():
        print(f"{colored(245, 185, 66, key)} - {colored(190, 210, 210, value)}")
    
    while True:
        text = 'Select a command to execute: '
        colored_text = colored(245, 245, 66, text)

        command = input(colored_text)

        # signup
        if command == 's':
            username = input('Enter username: ')
            password = input('Enter password: ')
            auth.signup(username, password)
            blockchain.reward(username)
        
        # login
        elif command == 'l':
            username = input('Enter username: ')
            password = input('Enter password: ')
            auth.signin(username, password)

        # check logged user
        elif command == 'u':
            if auth.current_user is None:
                print("No user is logged in")
            else:
                print("Logged user: " + auth.current_user.username)

        # perform a new transaction
        elif command == 't':
            if auth.current_user is None:
                Printer.error("You must be logged in to perform a transaction")
                continue

            receiver_username = input('Enter receiver username: ')

            if receiver_username == auth.current_user.username:
                Printer.error("You can't send money to yourself")
                continue

            receiver = users_db.find_by_username(receiver_username)

            if receiver is None:
                Printer.error("No user with username " + receiver_username + " exists")
                continue

            # TODO: check that amount is a number
            amount = input('Enter amount: ')
            reason = input('Enter reason: ')
            key = input('Enter a key for encrypting the transiction reason: ')

            transaction = Transaction(
                auth.current_user.username,
                receiver_username,
                int(amount),
                reason,
                key
            )

            try:
                blockchain.add_transaction(transaction)
                Printer.success("Added transaction to pending transactions")
            except OverspendingError:
                Printer.error("You don't have enough money to perform this transaction")
        
        # print pending transactions
        elif command == 'pt':
            print("Pending transactions:")
            print(str([str(t) for t in blockchain.pending_transactions]))

        # decrypt reason of a transaction
        elif command == 'dt':
            transaction_id = input("Enter transaction id: ")
            transaction = blockchain.find_transaction_by_id(int(transaction_id))

            if transaction is None:
                Printer.error(f"No transaction found with id {transaction_id}")
                continue
            
            print(transaction)
            key = input("Enter key to decrypt transaction reason: ")
            aes = AESCipher(key)

            try:
                reason = aes.decrypt(transaction.reason)
                print(f"Reason of the transaction: {reason}")
            except:
                Printer.error("Invalid key")

        # mine a new block
        elif command == 'm':
            if auth.current_user is None:
                Printer.error("You must be logged to mine a block")
                continue

            print("Mining a new block with pending transactions...")
            blockchain.mine(auth.current_user.username)
            Printer.success("You have been rewarded with " + str(blockchain.reward_amount) + "$")

        # print the blockchain
        elif command == 'b':
            print("Blockchain:")
            print(blockchain)

        # check logged user's balance
        elif command == 'ba':
            if auth.current_user is None:
                Printer.error("You must be logged to check you balance")
                continue
            
            print("Your balance is: " + str(blockchain.calculate_balance(auth.current_user.username)))

        # quit application
        elif command == 'q':
            print("Quitting application...")
            return

        # invalid command
        else:
            print('Invalid command')

if __name__ == "__main__":
    main()
