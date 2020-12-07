import math

from Crypto.Util import number
from hashlib import sha256
from random import getrandbits, randrange

from tools.prime import gen_prime, is_prime
from tools.utils import gcd, hex_dict_to_int

# from utils import gcd
# from prime import gen_prime, is_prime


LN_PAIRS = ((1024, 160), (2048, 224), (2048, 256), (3072, 256))
OUTLEN = 256

def hash(input):
    return int(sha256(str(input).encode()).hexdigest(), 16)

def st_random_prime(length, input_seed):
    if length < 2:
        return False, 0, 0, 0

    if length >= 33:
        status, c_0, prime_seed, prime_gen_counter = st_random_prime(math.ceil(length/2) + 1, input_seed)

        if not status:
            return False, 0, 0, 0

        iterations = math.ceil(length/OUTLEN) - 1
        old_counter = prime_gen_counter
        x = 0
        for i in range(iterations):
            x += (hash(prime_seed + i) * (1 << (i * OUTLEN)))
        prime_seed += iterations + 1
        x = (1 << (length - 1)) + x % (1 << (length - 1))
        t = math.ceil(x/(2 * c_0))

        while True:
            if (2 * t * c_0 + 1 > (1 << length)):
                t = math.ceil(((1 << (length - 1)))/(2 * c_0))
            c = 2 * t * c_0 + 1
            prime_gen_counter += 1
            a = 0
            for i in range(iterations):
                a += (hash(prime_seed + i) * (1 << (i * OUTLEN)))
            prime_seed += iterations + 1
            a = 2 + (a % (c - 3))
            z = pow(a, 2 * t, c)

            if (1 == gcd(z - 1, c)) and (1 == pow(z, c_0, c)):
                return True, c, prime_seed, prime_gen_counter

            if (prime_gen_counter >= 4 * length + old_counter):
                return False, 0, 0, 0
            t += 1

    prime_gen_counter = 0
    while True:
        c = hash(input_seed) ^ hash(input_seed + 1)
        c = (1 << (length - 1)) + (c % (1 << (length - 1)))
        c = (2 * math.floor(c/2) + 1)

        prime_gen_counter += 1
        input_seed += 2

        if is_prime(c):
            return True, c, input_seed, prime_gen_counter

        if prime_gen_counter > 4*length:
            return False, 0, 0, 0


def first_seed(N, seedlen=OUTLEN):
    status = False
    firstseed = 0

    if N not in [el[1] for el in LN_PAIRS]:
        return status, firstseed

    if(seedlen < N):
        return status, firstseed

    while firstseed < (1 << (N - 1)):
        firstseed = getrandbits(seedlen)

    return True, firstseed


def gen_pq(L, N):
    status = False
    firstseed = 0

    while True:
        fs_raw = first_seed(N)
        if fs_raw[0]:
            firstseed = fs_raw[1]
            break

    if (L, N) not in LN_PAIRS:
        return status

    status, q, qseed, qgen_counter = st_random_prime(N, firstseed)
    if not status:
        return -1, -1

    status, p_0, pseed, pgen_counter = st_random_prime(math.ceil(L/2 + 1), qseed)
    if not status:
        return -1, -1

    iterations = math.ceil(L/OUTLEN) - 1
    old_counter = pgen_counter

    x = 0
    for i in range(iterations):
        x += hash(pseed + i) * (1 << (i * OUTLEN))
    pseed += iterations + 1
    x = (1 << (L - 1)) + x % (1 << (L - 1))

    t = x//(2 * q * p_0)

    while True:
        if 2 * t * q * p_0 + 1 > (1 << L):
            t = math.ceil(((1 << (L - 1)))/(2 * q * p_0))
        p = 2 * t * q * p_0 + 1
        pgen_counter += 1

        a = 0
        for i in range(iterations):
            a += hash(pseed + i) * (1 << (i * OUTLEN))
        pseed += iterations + 1
        a = 2 + a % (p - 3)
        z = pow(a, 2 * t * q, p)

        if (1 == gcd(z - 1, p)) and (1 == pow(z, p_0, p)):
            # return True, {'p': p, 'q': q, 'pseed': pseed, 'qseed': qseed, 'pgen_counter': pgen_counter, 'qgen_counter': qgen_counter}
            return {'p': p, 'q': q, 'domain_seed': firstseed}

        if pgen_counter > 4 * L + old_counter:
            return -1, -1
        t += 1


def validation_pq_st(p, q, firstseed, pseed, qseed, pgen_counter, qgen_counter):
    L = (p.bit_length() + 1, p.bit_length())[p.bit_length() % 2 == 0]
    N = (q.bit_length() + 1, q.bit_length())[q.bit_length() % 2 == 0]
    if ((L, N) not in LN_PAIRS) or (firstseed < (1 << N - 1)) or ((1 << N) <= q) or ((1 << L) <= p) or ((p - 1) % q != 0):
        return False
    status, data = gen_pq(L, N, firstseed)
    result = [status, data['p'] == p, data['q'] == q, data['pseed'] == pseed, data['qseed'] == qseed, data['pgen_counter'] == pgen_counter, data['qgen_counter'] == qgen_counter]
    
    if all(result):
        return True
    return False


def gen_g(params, index=1):
    p = params['p']
    q = params['q']
    seed = params['domain_seed']
    seedlen = seed.bit_length()
    N = q.bit_length() + 1 if  q.bit_length() % 2 else q.bit_length()
    L = p.bit_length() + 1 if  p.bit_length() % 2 else p.bit_length()
    if (seedlen < N) or (index < 1 or index.bit_length() > 8) or (index > 4 * L - 1) or ((L, N) not in LN_PAIRS):
        return False
    e = (p - 1) // q
    count = 0
    g = 1
    while g < 2:
        count += 1

        if (count == 0):
            return False

        U = str(seed) + str(int("0x6767656E", 16)) + str(index) + str(count)
        W = int(sha256(U.encode()).hexdigest(), 16)
        g = pow(W, e, p)

    return g


def gen_keys(params):
    N = params['q'].bit_length()
    if N % 2:
        N += 1
    c = getrandbits(N+64)
    x = (c % (params['q']-1)) + 1
    y = pow(params['g'],x,params['p'])
    return {'private': x, 'public': y}


def dsa_sign(message, params, private_key, k=0):
    """DSA signing operation which captures and returns k."""
    params = hex_dict_to_int(params)
    private_key = int(private_key, 16)
    p = params['p']
    q = params['q']
    g = params['g']
    n = len(number.long_to_bytes(q))
    if k == 0:
        k = randrange(1, q)
    r = pow(g, k, p) % q

    h  = number.bytes_to_long(sha256(message).digest()[:n])
    xr = private_key * r
    s  = (number.inverse(k,q) * (h + xr)) % q

    return {'r': hex(r), 's': hex(s), 'k': hex(k)}


def dsa_verify(message, signature, params, public_key):
    """DSA signature verification."""
    signature = hex_dict_to_int(signature)
    params = hex_dict_to_int(params)
    public_key = int(public_key, 16)
    p = params['p']
    q = params['q']
    g = params['g']
    r = signature['r']
    s = signature['s']
    if r >= q or s >= q:
        return False
    w  = number.inverse(s,q) % q
    H  = number.bytes_to_long(sha256(message).digest())
    u1 = (H * w) % q
    u2 = (r * w) % q
    v  = ((pow(g, u1, p) * pow(public_key, u2, p)) % p) % q
    return v == r


def gen_params_dsa(L=2048, N=256):
    params = gen_pq(L, N)
    g = gen_g(params)
    params['g'] = g
    keys = gen_keys(params)
    params.pop('domain_seed')

    # large ints convert to hex
    for key, value in params.items():
        params[key] = hex(value)
    for key, value in keys.items():
        keys[key] = hex(value)

    return {'params': params, 'keys': keys}

