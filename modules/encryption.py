import rsa
from rsa import PublicKey


class Encrypter:
    const = 65537

    def __init__(self):
        (self.my_public, self.my_private) = rsa.newkeys(512)  # 512  bits длина ключа
        self.partner_public = None

    def decrypt(self, chipher):
        return rsa.decrypt(chipher.encode('latin1'), self.my_private).decode('utf8')

    def encrypt(self, message):
        return rsa.encrypt(message.encode('utf8'), self.partner_public).decode('latin1')

    def save_partner_public(self, partner_public):
        self.partner_public = PublicKey(int(partner_public), self.const)
