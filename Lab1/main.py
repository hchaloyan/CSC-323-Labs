import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import utility
import numpy as numPy

# CONSTANTS

# w: word size (in number of bits)
# n: degree of recurrence
# m: middle word, an offset used in the recurrence relation defining the series x, 1 ≤ m < n
# r: separation point of one word, or the number of bits of the lower bitmask, 0 ≤ r ≤ w - 1
# a: coefficients of the rational normal form twist matrix
# b, c: TGFSR(R) tempering bitmasks
# s, t: TGFSR(R) tempering bit shifts
# u, d, l: additional Mersenne Twister tempering bit shifts/masks

class mersenneTwister:
    
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
        f = 1812433253


        # BITMASKS
        self.UMASK = (0xffffffff << self.r) & 0xffffffff
        self.LMASK = 0xffffffff >> (self.w - self.r)

        # State array & index tracker
        self.state = [0] * 624
        self.stateIdx = 0

        self.state[0] = seed

        for i in range(1, self.n):
            seed = f * (seed ^ (seed >> (self.w-2))) + i
            self.state[i] = seed


    # uint32_t y = x ^ (x >> u);       // tempering 
    #          y = y ^ ((y << s) & b);
    #          y = y ^ ((y << t) & c);
    # uint32_t z = y ^ (y >> l);

    def temper(self, x) -> numPy.uint32:
        y = x ^ (x >> self.u)
        y = y ^ ((y << self.s) & self.b)
        y = y ^ ((y << self.t) & self.c)

        z = y ^ (y >> self.l)

        return z



    def twister(self) -> numPy.uint32:

        k = self.stateIdx


        j = k - (self.n-1)

        if j < 0:
            j += self.n
        

        x = (self.state[k] & self.UMASK) | (self.state[j] & self.LMASK)

        xA = x >> 1

        if (x & 0x00000001):
            xA ^= self.a

        j = k - (self.n - self.m)
        
        if (j < 0):
            j += self.n
        

        # Next value in state
        x = self.state[j] ^ xA

        k += 1
        self.state[k] = x

        if (k >= self.n):
            k = 0

        self.stateIdx = k

        z = self.temper(x)
        return z

def task1():

    # 5489 is the default seed
    seed = 5489

    mt = mersenneTwister(seed)
    print(mt.twister())

    mt2 = mersenneTwister(seed)

    print(mt.twister())


def main():
    
    task1()
    #task2()


if __name__=="__main__":
    main()