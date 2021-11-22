from OpenSSL import crypto

class CA:
    """
    This class represents a certification authority
    """

    @staticmethod
    def create_certificate(username):
        k = crypto.PKey()
        k.generate_key(crypto.TYPE_RSA, 2048)  # generate RSA key-pair

        print(k)

        cert = crypto.X509()
        # TODO: add other fields such as country, etc..
        cert.gmtime_adj_notBefore(0)
        cert.gmtime_adj_notAfter(10*365*24*60*60)  # 10 years expiry date
        cert.set_issuer(cert.get_subject())  # self-sign this certificate

        cert.set_pubkey(k)
        print(cert.get_pubkey())

        # print("Generated public key: ")
        # print(crypto.dump_publickey(crypto.FILETYPE_PEM, k))
        # print()

        cert.sign(k, 'sha256')

        open(f"certificates/{username}-cert.crt", 'wb').write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
        
        priv_key = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)
        # print("Generated private key: ")
        # print(priv_key)
        # print()

        open(f"keys/{username}-private.key", 'wb').write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

    @staticmethod
    def get_certificate(username):
        cert_file = open(f"certificates/{username}-cert.crt", "r")
        cert_data = cert_file.read()
        cert_file.close()

        cert = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)
        return cert

    @staticmethod
    def verify_certificate(cert):
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
        pub_key = cert.get_pubkey()
        return crypto.dump_publickey(crypto.FILETYPE_PEM, pub_key)

    @staticmethod
    def get_private_key(username):
        key_file = open(f"keys/{username}-private.key", 'r')
        key_data = key_file.read()
        key_file.close()

        priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, key_data)
        return crypto.dump_privatekey(crypto.FILETYPE_PEM, priv_key)


# create_certificate("prova")
# cert = get_certificate("prova")

# print("Obtained cert", cert)
# print()

# print("Obtained public key: ")
# print(get_public_key(cert))
# print()

# print("Obtained private key: ")
# print(get_private_key("prova"))

