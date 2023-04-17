from random import getrandbits
from time import time
import math

"""Module to generate pseudo random numbers using multiple methods. All methods use python's generator to be able to supply a long 
sequence without loading all of it in memory.
"""

def lcg(seed, a = 6364136223846793005, m = 2 ** 64, c = 0, min_size = None):
    """Linear congruent generator for pseudo random numbers. The maximal period is m / 4

    Defaulting m to 2 ** 65536 and c to 0 was a design choice to increase effiency at cost of some caveats,
    as explained by Knuth on The Art Of Computer Programming.

    Algorithm based on Cancian ¯\_(ツ)_/¯

    Args:
        seed (int): initial seed for the generator
        a (int, optional): multiplicative factor, increases jumps between values. Defaults to 6364136223846793005.
        m (int, optional): modulus, interacts with the period of the generator. Defaults to 2**65536.
        c (int, optional): additive factor, if it's ommited the generator is purely multiplicative. Defaults to 0.
        min_size (int, optional): minimum size of the number generated in bytes. Defaults to None.
    Yields:
        x: the next member of the sequence
    """
    state = seed

    while True:
        # The base idea is to multiply the current X by a multiplicative factor and sum it to an additive factor.
        # The module is applied to constrain the value between the [0, m] range.
        state = (a * state + c) % m
        
        x = state

        # Loop to concat smallers numbers if min_size is set
        if min_size is not None:
            while x.bit_length() <= min_size:
                state = (a * state + c) % m
                
                x = int(str(x) + str(state))

        seed = x

        yield x



def xorshift(seed, min_size = None):
    """Xorshift based generator for pseudo random numbers.

    Algorithm based on Marsaglia (https://www.jstatsoft.org/article/view/v008i14)
    
    Args:
        seed (int): initial seed for the generator
        min_size (int, optional): minimum size of the number generated in bytes. Defaults to None.

    Yields:
        x: the next member of the sequence
    """
    state = seed

    m = (2 ** 32) - 1
    
    while True:
        state ^= state << 13
        state ^= state >> 17
        state ^= state << 5
        state %= m
        
        x = state

        # Loop to concat smallers numbers if min_size is set
        if min_size is not None:
            while x.bit_length() <= min_size:
                state ^= state << 13
                state ^= state >> 17
                state ^= state << 5
                state %= m

                x = int(str(x) + str(state))
        
        seed = x

        yield x


def randlist(seed = getrandbits(32), quantity = 1, method = "lcg", min_size = None):
    match method:
        case "lcg":
            generator = lcg(seed, min_size=min_size)
        case "xor":
            generator = xorshift(seed, min_size=min_size)
    
    return [next(generator) for i in range(quantity)]


def rand_generator(seed = getrandbits(32), method = "lcg", min_size = None):
    match method:
        case "lcg":
            generator = lcg(seed, min_size=min_size)
        case "xor":
            generator = xorshift(seed, min_size=min_size)

    return generator