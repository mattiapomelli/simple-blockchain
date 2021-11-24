from OpenSSL import crypto

class CA:
    """
    This class represents a certification authority. It can generate and distribute
    public key certificates to be used for asymmetric encryption.
    """

    @staticmethod
    def create_certificate(username):
        """
        Creates a certificate for the user with the given username.
        """
        # Generate an RSA key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # Create a X509 certificate and add the fields. TODO: add other fields such as country, etc..
        cert = crypto.X509()
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)  # 10 years expiry date
        cert.set_issuer(cert.get_subject())  # self-sign this certificate
        cert.set_pubkey(k)

        # Sign the certificate
        cert.sign(k, 'sha256')

        # Store the user's certificate and private key in files
        open(f"certificates/{username}-cert.crt", 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(f"keys/{username}-private.key", 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    @staticmethod
    def get_certificate(username):
        """
        Gets and returns the certificate of the user with the given username.
        """
        # Get the certificate from the corresponding file
        cert_file = open(f"certificates/{username}-cert.crt", "r")
        cert_data = cert_file.read()
        cert_file.close()

        print(cert_data)

        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        return cert

    @staticmethod
    def verify_certificate(cert):
        """
        Verifies a given certificate. Returns True if the certificate is valid, false otherwise.
        """
        try:
            store = crypto.X509Store()
            store.add_cert(cert)
            ctx = crypto.X509StoreContext(store, cert)
            ctx.verify_certificate()
            return True
        except:
            return False

    @staticmethod
    def get_public_key(cert):
        """
        Gets and returns the public key contained in a given certificate.
        """
        pub_key = cert.get_pubkey()
        return crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key)

    @staticmethod
    def get_private_key(username):
        """
        Gets and returns the private key of the user with the given username
        """
        # Get the private key from the corresponding file
        key_file = open(f"keys/{username}-private.key", 'r')
        key_data = key_file.read()
        key_file.close()

        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, priv_key)
