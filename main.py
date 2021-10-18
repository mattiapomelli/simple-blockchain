from user_controller import user_controller 

def main():
    current_user = None

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

        elif command == 'u':
            if user_controller.current_user is None:
                print("No user is logged in")
            else:
                print("Logged user: " + user_controller.current_user.username)    

        elif command == 'q':
            print("Quitting application...")
            return

        else:
            print('Invalid command')

if __name__ == "__main__":
    main()
