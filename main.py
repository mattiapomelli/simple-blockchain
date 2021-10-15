from blockchain import Blockchain
from users_db import users_db

def main():
    current_user = None

    while True:
        command = input('Select a command to execute: ')

        # signup
        if command == 's':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user = users_db.create(username, password)

        # login
        elif command == 'l':
            username = input('Enter username: ')
            password = input('Enter password: ')
            user = users_db.find_by_username(username)

            if user is None:
                print("No user exists with the provided username")
                continue
            
            if user.password == password:
                print("Signed in as " + username)
                current_user = user

            else:
                print("Password is not correct")

        elif command == 'q':
            return

        else:
            print('Invalid command')

if __name__ == "__main__":
    main()
