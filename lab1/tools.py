from hmac import encrypt_hmac
from cbc_mac import encrypt_cbc
from poly_aes import encrypt_polyaes

CIPHERS = {
    'hmac': encrypt_hmac,
    'cbcmac': encrypt_cbc,
    'polyaes': encrypt_polyaes,
}

def encrypt(data):
    _hasher = data.get('hasher')
    hasher = CIPHERS.get(_hasher)
    if not hasher:
        return False
    key = data.get('key').encode()
    message = data.get('message').encode()
    return hasher(key, message)
    
    