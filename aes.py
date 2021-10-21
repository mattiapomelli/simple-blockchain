from Crypto import Random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode

class AESCipher:
    """
    This class represents an AES cipher
    """

    def __init__(self, key):
        """
        block_size: size of each block, in AES is 128 bits
        key: encryption key
        """
        self.block_size = AES.block_size
        self.key = key

    def encrypt(self, message):
        """
        Receives a plain text message and returns the message encrypted with AES
        In order to encrypt the text it:
        - adds padding to the message
        - generates a random initialization vector with the same size of a block
        """
        message = self.pad(message)
        iv = Random.new().read(self.block_size)

        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(message.encode()) # encrypts the message converted to bits 

        return b64encode(iv + encrypted_text).decode("utf-8")
    
    def decrypt(self, encrypted_message):
        """
        Decryptes the received encrypted message and returns the plain message
        """
        encrypted_message = b64decode(encrypted_message)
        iv = encrypted_message[:self.block_size]

        cipher = AES.new(self.key.encode(), AES.MODE_CBC, iv)
        message = cipher.decrypt(encrypted_message[self.block_size:]).decode("utf-8")

        return self.unpad(message)

    def pad(self, message):
        """
        Receives the message be encrypted and adds extra bytes to make the length
        of the message a multiple of the block size.
        Every padding byte will be the same, and will correspond to the unicode string of
        the number of padding bytes.
        In this way, it will be easier to understand how many bytes should be removed in the
        unpad method
        """
        padding_bytes = self.block_size - len(message) % self.block_size # number of extra bytes
        # TODO: understand which is the proper padding character
        padding_char = chr(padding_bytes)
        padding = padding_bytes * padding_char
        
        return message + padding

    def unpad(self, message):
        """
        Receives the decrypted message and removes all the extra characters added as padding
        in the pad method.
        """
        last_character = message[len(message) - 1:]
        bytes_to_remove = ord(last_character)
        return message[:-bytes_to_remove]
