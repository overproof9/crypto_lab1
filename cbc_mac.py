import blowfish

BLOCK_SIZE = 8

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])


def encrypt_block_cbc(block, key, iv):
    cipher = blowfish.Cipher(key)

    block_length = len(block)
    if block_length < BLOCK_SIZE:
        block += bytearray(BLOCK_SIZE - block_length)

    block = byte_xor(block, iv)

    cipher_block = cipher.encrypt_block(block)
    return cipher_block


def swap_blocks(blocks):
    length = len(blocks)
    blocks[length - 2], blocks[length - 1] = \
        blocks[length - 1], blocks[length - 2]
    return blocks


def encrypt_cbc(plain_text, key):
    iv = bytes(BLOCK_SIZE)

    text_length = len(plain_text)
    plain_blocks = [plain_text[i:i+BLOCK_SIZE]
                    for i in range(0, text_length, BLOCK_SIZE)]
    cipher_blocks = []

    for block in plain_blocks:
        cipher_block = encrypt_block_cbc(block, key, iv)
        iv = cipher_block
        cipher_blocks.append(cipher_block)

    if text_length % 16 != 0:
        cipher_blocks = swap_blocks(cipher_blocks)

    cypher_text = bytearray(0)
    for block in cipher_blocks:
        cypher_text += block

    cypher_text = cypher_text[:text_length]

    return cypher_text.hex()