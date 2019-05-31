from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

def getKey(password):
    hasher = SHA256.new(password)
    return hasher.digest()

with open('enim_msg.txt', 'r') as f:
    c = f.read()

filesize = int(c[:16])
print("filesize: %d" % filesize)
iv = c[16:32]
print("IV: %s" % iv)
key = getKey("sahay")
cipher = AES.new(key, AES.MODE_CBC, iv )
print cipher.decrypt(c[32:])
