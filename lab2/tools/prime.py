from random import randrange, getrandbits


def is_prime(candidate, num_tests=15):
    """
    Miller-Rabin primality testing for num_tests times
    recommended num_tests for 1024 is 7
    recommended num_tests for 1536 is 4
    """

    if candidate == 2 or candidate == 3:
        return True
    if candidate <= 1 or candidate % 2 == 0:
        return False

    r = candidate - 1
    s = 0
    
    # Decompose (n - 1) to write it as (2 ** s) * r
    # While r is even, divide it by 2 and increase the exponent.
    while not(r & 1):
        s += 1
        r //= 2
    
    # Miller-Rabin primality testing
    for _ in range(num_tests):
        a = randrange(2, candidate - 1)
        x = pow(a, r, candidate)
        if x != 1 and x != candidate - 1:
            j = 1
            while j < s and x != candidate - 1:
                x = pow(x, 2, candidate)
                if x == 1:
                    return False
                j += 1
            if x != candidate - 1:
                return False
    return True


def generate_prime_candidate(bitlen):
    candidate = getrandbits(bitlen)
    candidate |= (1 << bitlen - 1) | 1
    return candidate


def gen_prime(bitlen=1024):
    candidate = generate_prime_candidate(bitlen)
    while not is_prime(candidate):
        candidate = generate_prime_candidate(bitlen)
    return candidate
