import uuid

class User:
    def __init__(self, username):
        self.id = uuid.uuid4()
        self.username = username

    def __str__(self):
        return "Id: " + str(self.id) + ", Username: " + self.username
