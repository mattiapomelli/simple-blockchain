from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15
from base64 import b64encode, b64decode

class RSACipher:
    """
    This class represents an RSA cipher
    """

    @staticmethod
    def encrypt(message, public_key):
        # Create a new RSA cipher from the receiver's public key
        rsa_key = RSA.importKey(extern_key=public_key)
        cipher = PKCS1_OAEP.new(rsa_key)

        # Encrypt the message, after converting it from a string to bytes
        encrypted_message = cipher.encrypt(message.encode())

        # Convert from bytes to a base64 string
        return b64encode(encrypted_message).decode("utf-8")

    @staticmethod
    def decrypt(encrypted_message, private_key):
        # Create a new RSA cipher from the logged user's private key
        rsa_key = RSA.importKey(extern_key=private_key)
        cipher = PKCS1_OAEP.new(rsa_key)

        # Convert encrypted message from a base64 string to bytes
        encrypted_message_bytes = b64decode(encrypted_message)
        
        # Decrypt the ecrypted message, and convert it from btyes to string
        decrypted_message = cipher.decrypt(encrypted_message_bytes).decode()
        
        return decrypted_message


    @staticmethod    
    def sign(message, private_key):
        # Create a new RSA cipher from the private key
        rsa_key = RSA.importKey(extern_key=private_key)

        # Compute the hash of the message to be signed
        hash = SHA256.new(message.encode())

        # Sign the hash of the message
        signature = pkcs1_15.new(rsa_key).sign(hash)

        # Convert the signature from bytes to an hex string 
        hex_signature = signature.hex()

        return hex_signature
    
    @staticmethod
    def verify(message, signature, public_key):
        # Create a new RSA cipher from the public key
        rsa_key = RSA.importKey(extern_key=public_key)

        # Compute the hash of the message
        hash = SHA256.new(message.encode())

        # Convert signature from an hex string to bytes
        signature_bytes = bytes.fromhex(signature)

        try:
            pkcs1_15.new(rsa_key).verify(hash, signature_bytes)
            return True
        except:
            return False
