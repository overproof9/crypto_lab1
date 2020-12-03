from Crypto.Cipher import AES
from Crypto.Hash import Poly1305

def extend_key(key, length=32):
    add = [0x00] * (length - len(key))
    extended = add + list(key)
    return bytes(extended[:length])

def encrypt_polyaes(key, message):
    extended_key = extend_key(key)
    hasher = Poly1305.new(key=extended_key, cipher=AES)
    result = hasher.update(message)
    return result.hexdigest()
