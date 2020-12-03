import math

def rotate(x, y):
    x &= 0xFFFFFFFF
    return ((x<<y) | (x>>(32-y))) & 0xFFFFFFFF

def md5(message):
    k = [int(abs(math.sin(i+1)) * 2**32) for i  in range(0, 64)]
    var = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476]
    r =  [
        7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,
        5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,
        4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,
        6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21
    ]
    block_size = 64
    message = bytearray(message)
    original_length_bit_message = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80) 
    while len(message) % block_size != 56:
        message.append(0)
    message += original_length_bit_message.to_bytes(8, byteorder='little')

    messageA = var[0]
    messageB = var[1]
    messageC = var[2]
    messageD = var[3]

    for i in range(0, len(message), block_size):
        a = messageA
        b = messageB
        c = messageC
        d = messageD
        w = message[i : i + block_size]
        for j in range(block_size):
            if (0 <= j | j < 16):
                f = ((b & c) | (~b & d))
                g = j
            elif (j >= 16 | j < 32):
                f = ((d & b) | (~d & c))
                g = (5 * j + 1) % 16
            elif (j >= 32 | j < 48):
                f = (b ^ c ^ d)
                g = (3 * j + 5) % 16
            elif (j >= 48 | j < 64):
                f = (c ^ (b | (~d)))
                g = (7 * j) % 16
            tmp = (b + rotate(a + f + k[j] + int.from_bytes(w[4 * g : 4 * g + 4], byteorder='little'), r[j])) & 0xFFFFFFFF
            a, b, c, d = d, tmp, b, c
        messageA += a
        messageA &= 0xFFFFFFFF
        messageB += b
        messageB &= 0xFFFFFFFF
        messageC += c
        messageC &= 0xFFFFFFFF
        messageD += d
        messageD &= 0xFFFFFFFF
    x = messageA + (messageB << 32) + (messageC << 64) + (messageD << 96)

    return x.to_bytes(16, byteorder='little')


class HMAC:
    def __init__(self, key, message, hash_h=md5):
        self.i_key_pad = bytearray()
        self.o_key_pad = bytearray()
        self.key = key
        self.message = message
        self.blocksize = 64
        self.hash_h = hash_h
        self.init_flag = False

    def init_pads(self):
        for i in range(self.blocksize):
            self.i_key_pad.append(0x36 ^ self.key[i])
            self.o_key_pad.append(0x5c ^ self.key[i])

    def init_key(self):
        if len(self.key) > self.blocksize:
            self.key = bytearray(md5(key).digest())
        elif len(self.key) < self.blocksize:
            i = len(self.key)
            while i < self.blocksize:
                self.key += b"\x00"
                i += 1

    def digest(self):
        if self.init_flag == False:
            self.init_key()
            self.init_pads()
            self.init_flag = True
        return self.hash_h(bytes(self.o_key_pad)+self.hash_h(bytes(self.i_key_pad)+self.message))


    def hex(self):
        if self.init_flag == False:
            self.init_key()
            self.init_pads()
            self.init_flag = True
        return self.hash_h(bytes(self.o_key_pad)+self.hash_h(bytes(self.i_key_pad)+self.message)).hex()


def encrypt_hmac(key, message):
    hash = HMAC(key, message)
    return hash.hex()
