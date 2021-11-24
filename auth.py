from users_db import users_db
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
from aes import AESCipher
from exceptions import ConflictError, NotFoundError, InvalidCredentialsError

class Auth:
    """
    This class handles user authentication. 
    """

    def __init__(self):
        """
        user: user that is currently logged in, or None when no user is logged in
        """
        self.user = None

    def signup(self, username, password, email, phone_nr, address):
        """
        Creates a new user with the given username and password. Password is hashed with SHA256.
        Raises ConflictError if the username is already taken
        """
        existing_user = users_db.find_by_username(username)

        if existing_user is not None:
            raise ConflictError

        # Encrypt user's private data with AES, using its password as a key
        encrypted_email = AESCipher.encrypt(email, password)
        encrypted_phone_nr = AESCipher.encrypt(phone_nr, password)
        encrypted_adress = AESCipher.encrypt(address, password)

        # Generate a random salt
        salt = get_random_bytes(16)

        # Hash the password with PBKDF2 and the generated salt
        hashed_password_bytes = PBKDF2(password.encode(), salt, 64, count=1000000, hmac_hash_module=SHA256)

        # Convert the hashed password from bytes to string, after appending the salt at the end
        hashed_password = b64encode(hashed_password_bytes + salt).decode("utf-8")

        self.user = users_db.create(username, hashed_password, encrypted_email, encrypted_phone_nr, encrypted_adress)

    def signin(self, username, password):
        """
        Signs in the user with the given username.
        Raises NotFoundError if no user is found with the given username.
        Raises InvalidCredentialsError if the given password doesn't correspond
        with the user's password.
        Since the password in the db is stored as hashed, the given password
        must also be hashed with the same algorithm before comparing it with the stored one.
        """
        user = users_db.find_by_username(username)
        
        if user is None:
            raise NotFoundError

        # Convert the stored password from string to bytes
        stored_password_bytes = b64decode(user.password)

        # Get the salt from the stored password by extxracting the last 16 bytes
        salt = stored_password_bytes[-16:]

        # Hash the provided password with PBKDF2 and the obtained salt
        hashed_password_bytes = PBKDF2(password.encode(), salt, 64, count=1000000, hmac_hash_module=SHA256)

        # Convert the hashed password from bytes to string
        hashed_password = b64encode(hashed_password_bytes  + salt).decode("utf-8")

        # Compare the result with the stored password
        if hashed_password != user.password:
            raise InvalidCredentialsError
        
        self.user = user
    
    def is_logged(self):
        """
        Returns True if a user is logged in, False otherwise
        """
        return self.user != None

    def decrypt_personal_data(self, username, key):
        """
        Decrypts the data of the user with the given username, using the given key
        """
        user = users_db.find_by_username(username)

        # Decrypt user's private data with AES
        email = AESCipher.decrypt(user.email, key)
        phone_nr = AESCipher.decrypt(user.phone_nr, key)
        address = AESCipher.decrypt(user.address, key)

        return {
            "email": email,
            "phone_nr": phone_nr,
            "address": address
        }
