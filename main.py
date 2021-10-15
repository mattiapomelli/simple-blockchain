from blockchain import Blockchain
from users_db import users_db

def main():
    command = input('Select a command to execute: ')

    if command == 's':
        username = input('Enter username: ')
        password = input('Enter password: ')
        user = users_db.create_user(username, password)
    
    else:
        print('Invalid command')

if __name__ == "__main__":
    main()
