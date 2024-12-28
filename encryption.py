from Crypto.Cipher import AES
import hashlib

class MTProtoEncryptor:
    def __init__(self, key):
        self.aes_key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, data):
        cipher = AES.new(self.aes_key, AES.MODE_CFB)
        return cipher.encrypt(data)

    def decrypt(self, data):
        cipher = AES.new(self.aes_key, AES.MODE_CFB)
        return cipher.decrypt(data)
