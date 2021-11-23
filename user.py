class User:
    """
    This class represents an user of the system.
    Users can perform transactions, that is sending money to other users,
    and receive money for mining blocks
    """

    def __init__(self, username, password, email):    
        """
        id: unique identifier of the user
        username: username of the user, is also unique
        password: password of the user
        """
        self.username = username
        self.password = password
        self.email = email
        #self.address_country = address_country
        #self.address_city = address_city
        
        

    def __str__(self):
        return "Id: " + self.id + ", Username: " + self.username + "\n"
