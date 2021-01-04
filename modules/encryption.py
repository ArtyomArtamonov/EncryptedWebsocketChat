import rsa
from rsa import PublicKey


class Encrypter:
    const = 65537 # IDK what that constant do, just let it here
    key_length = 2048 # 1024 bits key length

    def __init__(self):
        (self.my_public, self.my_private) = rsa.newkeys(self.key_length) # Generate new pair of keys
        self.partner_public = None

    def decrypt(self, chipher): # Decrypt message
        try:
            return rsa.decrypt(chipher.encode('latin1'), self.my_private).decode('utf8')
        except rsa.DecryptionError:
            return chipher

    def encrypt(self, message): # Encrypt Message
        return rsa.encrypt(message.encode('utf8'), self.partner_public).decode('latin1')

    def save_partner_public(self, partner_public): # Save Partner's public key
        self.partner_public = PublicKey(int(partner_public), self.const)
