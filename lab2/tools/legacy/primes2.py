from random import randrange, getrandbits

class PrimeGenerator:
    def __init__(self, length=1024, tests=128):
        self.length = length
        self.tests = tests
        self.candidate = 4

    def _is_prime(self):
        if self.candidate == 2 or self.candidate == 3:
            return True
        if self.candidate <= 1 or self.candidate % 2 == 0:
            return False
        s = 0
        r = self.candidate - 1
        while r & 1 == 0:
            s += 1
            r //= 2
        for _ in range(self.tests):
            a = randrange(2, self.candidate - 1)
            x = pow(a, r, self.candidate)
            if x != 1 and x != self.candidate - 1:
                j = 1
                while j < s and x != self.candidate - 1:
                    x = pow(x, 2, self.candidate)
                    if x == 1:
                        return False
                    j += 1
                if x != self.candidate - 1:
                    return False    
        return True

    def _generate_prime_candidate(self):
        candidate = getrandbits(self.length)
        candidate |= (1 << self.length - 1) | 1    
        self.candidate = candidate

    def find(self):
        while not self._is_prime():
            self._generate_prime_candidate()
        return self.candidate

    def hex(self):
        n = self.find()
        print('------------')
        bn = n.to_bytes((n.bit_length() + 7) // 8, 'big')
        hn = hex(n)
        print(type(bn))
        print(type(hn))
        print('BN >> ')
        try:
            decoded = bytes.fromhex(hn[2:])
        except TypeError as e:
            print('cant decode ')
            print(e)
        else:
            print(decoded)
            print(type(decoded))
        print('------------')

        
        return n
