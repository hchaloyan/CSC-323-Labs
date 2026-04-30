
# CONSTANTS

# w: word size (in number of bits)
# n: degree of recurrence
# m: middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
# r: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w - 1
# a: coefficients of the rational normal form twist matrix
# b, c: TGFSR(R) tempering bitmasks
# s, t: TGFSR(R) tempering bit shifts
# u, d, l: additional Mersenne Twister tempering bit shifts/masks

class MT19937:

    def __init__(self, seed):

        # Initialize constants and state array

        # (w, n, m, r)
        self.w = 32
        self.n = 624
        self.m = 397
        self.r = 31

        # (a)
        self.a = 0x9908B0DF

        # (u, d)
        self.u = 11
        self.d = 0xFFFFFFFF

        # (s, b)
        self.s = 7
        self.b = 0x9D2C5680

        # (t, c)
        self.t = 15
        self.c = 0xEFC60000

        # (l)
        self.l = 18

        # Initialization constant
        self.f = 1812433253

        # BITMASKS
        self.lower_mask = (1 << self.r) - 1
        self.upper_mask = (~self.lower_mask) & 0xFFFFFFFF

        # State array & index tracker
        self.mt = [0] * self.n
        self.index = self.n

        # Accept bytes seed (e.g. os.urandom(4)) or integer
        if isinstance(seed, (bytes, bytearray)):
            seed = int.from_bytes(seed, byteorder='big')

        seed = seed & 0xFFFFFFFF
        self.mt[0] = seed

        for i in range(1, self.n):
            # Keep bottom 32 bits to match pseudocode
            self.mt[i] = (self.f * (self.mt[i-1] ^ (self.mt[i-1] >> (self.w - 2))) + i) & 0xFFFFFFFF


    def extract_number(self):

        if self.index >= self.n:
            self.twist()

        y = self.mt[self.index]

        # Tempering
        y ^= (y >> self.u) & self.d
        y ^= (y << self.s) & self.b
        y ^= (y << self.t) & self.c
        y ^= (y >> self.l)

        self.index += 1

        return y & 0xFFFFFFFF


    def twist(self):

        for i in range(self.n):
            x = (self.mt[i] & self.upper_mask) + (self.mt[(i + 1) % self.n] & self.lower_mask)
            xA = x >> 1

            if x % 2 != 0:
                xA ^= self.a

            self.mt[i] = self.mt[(i + self.m) % self.n] ^ xA

        self.index = 0
