from user_controller import user_controller
from users_db import users_db
from transaction import Transaction
from blockchain import Blockchain
from exceptions import OverspendingError

def main():
    current_user = None
    blockchain = Blockchain()

    while True:
        # TODO: print list of available commands, i can do it ^^
        print(" list of commands:\n s - signup\n l - login\n u - check logged in account\n "
              "commands available after login in:\n t - perform transaction\n pt - print pending transaction\n m - mine the block\n b - print blockcain\n ba - print user ballance\n q - quit")

        command = input('Select a command to execute: ')

        # signup
        if command == 's':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user_controller.signup(username, password)
            blockchain.reward(username)
        
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

            if receiver_username == user_controller.current_user.username:
                print("You can't send money to yourself")
                continue

            receiver = users_db.find_by_username(receiver_username)

            if receiver is None:
                print("No user with username " + receiver_username + " exists")
                continue

            # TODO: check that amount is a number
            amount = input('Enter amount: ')
            reason = input('Enter reason: ')

            transaction = Transaction(user_controller.current_user.username, receiver_username, int(amount), reason)

            try:
                blockchain.add_transaction(transaction)
                print("Added transaction to pending transactions")
            except OverspendingError:
                print("You don't have enough money to perform this transaction")
        
        # print pending transactions
        elif command == 'pt':
            print("Pending transactions:")
            print(str([str(t) for t in blockchain.pending_transactions]))

        # mine a new block
        elif command == 'm':
            if user_controller.current_user is None:
                print("You must be logged to mine a block")
                continue

            print("Mining a new block with pending transactions...")
            blockchain.mine(user_controller.current_user.username)
            print("You have been rewarded with " + str(blockchain.reward_amount) + "$")

        # print the blockchain
        elif command == 'b':
            print(blockchain)

        # check logged user's balance
        elif command == 'ba':
            if user_controller.current_user is None:
                print("You must be logged to check you balance")
                continue
            
            print("Your balance is: " + str(blockchain.calculate_balance(user_controller.current_user.username)))

        # quit application
        elif command == 'q':
            print("Quitting application...")
            return

        # invalid command
        else:
            print('Invalid command')

if __name__ == "__main__":
    main()
