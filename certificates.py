from OpenSSL import crypto
from printer import Printer

class CertificationAuthority:
    """
    This class represents a certification authority. It can generate and distribute
    public key certificates to be used for asymmetric encryption.
    """

    def __init__(self):
        self.cert_ca = self.create_own_certificate()
        # self.cert_intermediate = self.create_intermediate_certificate()
    
    def create_own_certificate(self):
        """
        Creates a certificate for the certification authority
        """
        cert_file = open(f"certificates/ca-cert.cer", "r")
        cert_data = cert_file.read()
        cert_file.close()

        if (cert_data != ""):
            return crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        else:
            # Generate an RSA key pair
            k = crypto.PKey()
            k.generate_key(crypto.TYPE_RSA, 2048)

            # Create a X509 certificate and add the fields.
            cert = crypto.X509()
            cert.gmtime_adj_notBefore(0)
            cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # 1 year validity period

            cert.set_issuer(cert.get_subject())  # self-sign this certificate
            cert.set_pubkey(k)

            # Sign the certificate
            cert.sign(k, 'sha256')

            # Store the user's certificate and private key in files
            open(f"certificates/ca-cert.cer", 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
            open(f"keys/ca-private.key", 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
            
            return cert

    def create_certificate(self, username):
        """
        Creates and returns a certificate for the user with the given username.
        """
        # Generate an RSA key pair
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)

        # Create a X509 certificate and add the fields. TODO: add other fields such as country, etc..
        cert = crypto.X509()      
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(30 * 24 * 60 * 60)  # 1 month validity period

        # Set as issuer the subject of the certification authority certificate
        cert.set_issuer(self.cert_ca.get_subject()) 
        cert.set_pubkey(k)

        # Sign the certificate
        cert.sign(k, 'sha256')

        # Store the user's certificate and private key in files
        open(f"certificates/{username}-cert.cer", 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        open(f"keys/{username}-private.key", 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        return cert

    def get_certificate(self, username):
        """
        Gets and returns the certificate of the user with the given username.
        Returns None if no certificate is found.
        """
        try:
            # Get the certificate from the corresponding file
            cert_file = open(f"certificates/{username}-cert.cer", "r")
            cert_data = cert_file.read()
            cert_file.close()

            cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
            return cert
        except:
            return None

    def verify_certificate(self, cert):
        """
        Verifies a given certificate. Returns True if the certificate is valid, false otherwise.
        """
        try:
            store = crypto.X509Store()
            # Add the certification authority certificate as a trusted certificate
            store.add_cert(self.cert_ca)

            # Verify the given certificate
            ctx = crypto.X509StoreContext(store, cert)
            ctx.verify_certificate()

            # crypto.X509StoreContextError().args
            return True
        except Exception as e:
            error_message = e.args[0][2]
            if error_message == 'self signed certificate':
                Printer.info("Certificate is not verified because it hasn't been added to a real list of trusted certificates")
                return True

            return False

    def get_public_key(self, cert):
        """
        Gets and returns the public key contained in a given certificate.
        """
        pub_key = cert.get_pubkey()
        return crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key)

    def get_private_key(self, username):
        """
        Gets and returns the private key of the user with the given username
        """
        # Get the private key from the corresponding file
        key_file = open(f"keys/{username}-private.key", 'r')
        key_data = key_file.read()
        key_file.close()

        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, priv_key)

    @property
    def public_key_ca(self):
        return self.get_public_key(self.cert_ca)

    @property
    def private_key_ca(self):
        return self.get_private_key("ca")

# Certification authority that will create and distribute public key certificates for the system
CA = CertificationAuthority()
