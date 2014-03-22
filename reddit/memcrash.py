"""

Created by: Nathan Starkweather
Created on: 03/20/2014
Created in: PyCharm Community Edition


"""
__author__ = 'Nathan Starkweather'

from math import *
import itertools as it
def sieve(cap):
    capmax = cap + 1
    bools = [False, False]
    bools.extend(True for _ in range(2, cap + 1))
    for i in range(2, int((sqrt(cap))) + 1):
        if bools[i]:
            x = i * 2
            while x < capmax:
                bools[x] = False
                x += i
    return [i for i, b in enumerate(bools) if b]


def isPrime(n):
    if not n % 2:
       return False
    i = 3
    root = sqrt(n) + 1
    while i < root:
        if not n % i:
            return False
        i += 2
    return True

print("primes")
primes=[str(i) for i in sieve(500)]
print("combos")
combos=it.combinations(primes,4)
print("perms")
from sys import getsizeof

perms= (i for c in combos for i in it.permutations(c,2) )

# for i in range(100):
#     print(i, isPrime(i))

for i in perms:
    result = ''.join(i)
    # print(result)
    # print(isPrime(int(result)))
    if isPrime(int(result)):
        print(result)

