import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
###################
class Cryptor:
    def __init__(self, encrypt_cypher, key="qBC-KGT-FiTS-JkV"):
      self.encrypt_code = key
      self.encrypt_cypher = encrypt_cypher
      self.SECRET_KEY = str(key).encode("utf-8")
      self.BLOCK_SIZE = 32 # Bytes
      self.CIPHER = AES.new(self.SECRET_KEY, AES.MODE_ECB) # never use ECB in strong systems obviously 
    def encrypt(self, text):
       text = str(text).encode("utf-8")
       return base64.b64encode(self.CIPHER.encrypt(pad(text, self.BLOCK_SIZE))).decode("utf-8")
    
    def decrypt(self, encoded_text):
       self.CIPHER = AES.new(self.SECRET_KEY, AES.MODE_ECB)
       return unpad(self.CIPHER.decrypt(base64.b64decode(encoded_text)), self.BLOCK_SIZE).decode("utf-8")
       
# cryptor = Cryptor()
# text = 14
# text = cryptor.encrypt(text)
# print(text)
# print(cryptor.decrypt(text))
