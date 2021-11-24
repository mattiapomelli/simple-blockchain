class User:
    """
    This class represents an user of the system.
    Users can perform transactions, that is sending money to other users,
    and receive money for mining blocks
    """

    def __init__(self, username, password, email, phone_nr, address):    
        """
        id: unique identifier of the user
        username: username of the user, is also unique
        password: password of the user
        """
        self.username = username
        self.password = password
        self.email = email
        self.phone_nr  = phone_nr
        self.address = address
        
    def __str__(self):
        return (
            f"\Username: {self.username}"
            f"\Email: {self.password}"
            f"\Phone number: {self.phone_nr}"
            f"\Address: {self.address}"
        )
