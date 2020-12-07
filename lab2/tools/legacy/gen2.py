#  Copyright 2011 Sybren A. Stüvel <sybren@stuvel.eu>
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""Numerical functions related to primes.
Implementation based on the book Algorithm Design by Michael T. Goodrich and
Roberto Tamassia, 2002.
"""

import rsa.common
import rsa.randnum

__all__ = ['getprime', 'are_relatively_prime']


def gcd(p: int, q: int) -> int:
    """Returns the greatest common divisor of p and q"""

    while q != 0:
        (p, q) = (q, p % q)
    return p


def get_primality_testing_rounds(number):
    """Returns minimum number of rounds for Miller-Rabing primality testing,
      * p, q bitsize: 512; rounds: 7
      * p, q bitsize: 1024; rounds: 4
      * p, q bitsize: 1536; rounds: 3
    """

    bitsize = rsa.common.bit_size(number)
    if bitsize >= 1536:
        return 3
    if bitsize >= 1024:
        return 4
    if bitsize >= 512:
        return 7
    return 10


def miller_rabin_primality_testing(n, k):
    """Calculates whether n is composite (which is always correct) or prime
    (which theoretically is incorrect with error probability 4**-k), by
    applying Miller-Rabin primality testing.
    :param n: Integer to be tested for primality.
    :type n: int
    :param k: Number of rounds (witnesses) of Miller-Rabin testing.
    :type k: int
    :return: False if the number is composite, True if it's probably prime.
    :rtype: bool
    """

    if n < 2:
        return False

    # Decompose (n - 1) to write it as (2 ** r) * d
    # While d is even, divide it by 2 and increase the exponent.
    d = n - 1
    r = 0

    while not (d & 1):
        r += 1
        d >>= 1

    for _ in range(k):
        a = rsa.randnum.randint(n - 3) + 1

        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue

        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == 1:
                return False
            if x == n - 1:
                break
        else:
            return False

    return True


def is_prime(number: int) -> bool:
    """Returns True if the number is prime, and False otherwise."""

    if number < 10:
        return number in {2, 3, 5, 7}

    if not (number & 1):
        return False

    k = get_primality_testing_rounds(number)

    return miller_rabin_primality_testing(number, k + 1)


def getprime(nbits=1024):
    """Returns a prime number that can be stored in 'nbits' bits."""

    if nbits < 128:
        return 0

    while True:
        integer = rsa.randnum.read_random_odd_int(nbits)
        if is_prime(integer):
            return integer


def are_relatively_prime(a: int, b: int) -> bool:
    """
    Returns True if a and b are relatively prime, and False if they
    are not.
    """

    d = gcd(a, b)
    return d == 1