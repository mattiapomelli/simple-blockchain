from user_controller import user_controller
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain

def main():
    current_user = None
    blockchain = Blockchain()

    while True:
        # TODO: print list of available commands
        command = input('Select a command to execute: ')

        # signup
        if command == 's':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user_controller.signup(username, password)
        
        # login
        elif command == 'l':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user_controller.signin(username, password)

        # check logged user
        elif command == 'u':
            if user_controller.current_user is None:
                print("No user is logged in")
            else:
                print("Logged user: " + user_controller.current_user.username)

        # perform a new transaction
        elif command == 't':
            if user_controller.current_user is None:
                print("You must be logged in to perform a transaction")
                continue

            receiver_username = input('Enter receiver username: ')
            receiver = users_db.find_by_username(receiver_username)

            if receiver is None:
                print("No user with username " + receiver_username + " exists")
                continue

            amount = input('Enter amount: ')

            transaction = Transaction(user_controller.current_user.username, receiver_username, amount)
            blockchain.add_transaction(transaction)
            print("Added transaction to pending transactions")
        
        elif command == 'pt':
            print("Pending transactions:")
            print(str([str(t) for t in blockchain.pending_transactions]))

        # quit application
        elif command == 'q':
            print("Quitting application...")
            return

        # invalid command
        else:
            print('Invalid command')

if __name__ == "__main__":
    main()
