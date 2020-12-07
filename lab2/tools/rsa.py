from hashlib import sha1

from Crypto.Util import number

from tools.exceptions import SignatureError
from tools.prime import gen_prime
from tools.utils import extended_gcd, hex_dict_to_int


def sign_rsa(message, priv):
    priv = hex_dict_to_int(priv)
    k    = (priv['n'].bit_length() + 7) // 8
    em   = emsa_pkcs15_encode(message, k)
    m    = number.bytes_to_long(em)
    s    = RSASP1(m, priv)
    return number.long_to_bytes(s)


def RSASP1(m, priv):
    if 0 <= m < priv['n']:
        return pow(m, priv['d'], priv['n'])
    raise SignatureError('message representative out of range')


def verify_rsa(message, signature, pub):
    pub = hex_dict_to_int(pub)
    k        = len(number.long_to_bytes(pub['n']))
    
    if len(signature) != k:
        raise SignatureError("invalid signature")

    s        = number.bytes_to_long(signature)
    m        = RSAVP1(s, pub)
    em       = number.long_to_bytes(m, k)
    em_prime = emsa_pkcs15_encode(message, k)
    return em_prime == em
    
def RSAVP1(s, pub):
    if 0 <= s < pub['n']:
        return pow(s, pub['e'], pub['n'])
    raise SignatureError('signature representative out of range')
        

def emsa_pkcs15_encode(message, emLen):
    """
    EMSA-PKCS1.5-ENCODE
    Returns the encoded message.
    """
    H    = sha1(message).digest()
    der  = b'\x30\x21\x30\x09\x06\x05\x2b\x0e\x03\x02\x1a\x05\x00\x04\x14'
    T    = der + H
    tLen = len(T)

    if emLen < tLen + 11:
        raise SignatureError('message length too short')

    ps = b'\xff' * (emLen - tLen - 3)
    return b'\x00\x01' + ps + b'\x00' + T


def gen_rsa_keys():
    e = 65537
    p = gen_prime()
    q = gen_prime()
    while q == p:
        q = gen_prime()

    n = p * q
    euler = (p - 1) * (q - 1)
    d = extended_gcd(e, euler)[1]

    return {
        'public': {
            'n': hex(n),
            'e': hex(e)
        },
        'private': {
            'n': hex(n),
            'd': hex(d)
        }
    }




