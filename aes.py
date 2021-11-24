from Crypto.Cipher import AES
from Crypto.Util import Counter
from base64 import b64encode, b64decode

class AESCipher:
    """
    This class represents an AES cipher
    """

    @staticmethod
    def encrypt(message, key):
        """
        Encryptes a message with AES using the given key and CTR operation mode.
        Returns the encrypted message.
        """
        # Add padding to the message
        message = AESCipher.pad(message)

        # Create a counter with the same size of the blocks
        counter = Counter.new(AES.block_size * 8)

        # Add padding to the key to make sure that has the same length as the block size
        padded_key = AESCipher.pad(key)

        # Create a new AES cipher from the given key and the created counter
        cipher = AES.new(padded_key.encode(), AES.MODE_CTR, counter=counter)

        # Encrypt the message, after converting it from string to bytes
        encrypted_message = cipher.encrypt(message.encode())

        return b64encode(encrypted_message).decode("utf-8")
    

    @staticmethod
    def decrypt(encrypted_message, key):
        """
        Decryptes the received encrypted message with the given key and returns the plain message.
        Returns the original message.
        """
        # Convert the encrypted message to bytes
        encrypted_message = b64decode(encrypted_message)

        # Create a counter with the same size of the blocks
        counter = Counter.new(AES.block_size * 8)

        # Add padding to the key to make sure that has the same length as the block size
        padded_key = AESCipher.pad(key)

        # Crate a new AES cipher from the given key and the created counter
        cipher = AES.new(padded_key.encode(), AES.MODE_CTR, counter=counter)

        # Decrypt the encrypted message, and convert it from bytes to string
        decrypted_message = cipher.decrypt(encrypted_message).decode("utf-8")

        # Remove the padding from the decrypted message
        return AESCipher.unpad(decrypted_message)

    @staticmethod
    def pad(message):
        """
        Receives a message and adds extra bytes to make the length of the
        message a multiple of the block size.
        Returns the padded message.
        
        Every padding byte will be the same, and will correspond to the unicode string of
        the number of padding bytes.
        In this way, it will be easier to understand how many bytes should be removed in order
        to unpad the message.
        """
        # Get number of extra bytes needed for the padding
        padding_bytes_num = AES.block_size - len(message) % AES.block_size
        
        # Calculate the character to use for padding
        padding_char = chr(padding_bytes_num)

        # Generate the padding
        padding = padding_bytes_num * padding_char
        
        # Add padding to the message
        padded_message = message + padding

        return padded_message

    @staticmethod
    def unpad(message):
        """
        Receives a decrypted message and removes all the extra characters added as padding.
        Returns the unpadded message.
        """
        # Extract last character of the message, that corresponds to the character used for padding
        last_character = message[len(message) - 1:]

        # Calculate the number of bytes to remove
        bytes_to_remove = ord(last_character)

        # Remove padding from the message
        unpadded_message = message[:-bytes_to_remove]

        return unpadded_message
