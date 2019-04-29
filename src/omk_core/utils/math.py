from fractions import Fraction as Frac
import itertools
import math

def pow2_floor_frac(x):
    return Frac(2**math.floor(math.log2(x)))

def primes(start):
    return (x for x in itertools.count(start) if all(
                x % y != 0 for y in range(2, int(x ** 0.5) + 1)
            ))

def is_pow2(x):
    return math.log2(x).is_integer()