import hashlib
from sympy import *
import random
import math


def nBitRandom(n):
   
    # Returns a random number
    # between 2**(n-1)+1 and 2**n-1'''
    return(random.randrange(2**(n-1)+1, 2**n-1))

def nBitPrime(n):
    q = nBitRandom(160)
    while not isprime(q):
        q = nBitRandom(160)
    return q

def getP(q, n):
    p = nBitPrime(n)
    while not((p - 1) % q == 0 and math.pow(2, n - 1) < p and p < math.pow(2, n)):
        p = nBitPrime(n)
    return p


def main():
    m = "test text"
    H = hashlib.sha1()
    H.update(str.encode(m))
    q = nBitPrime(160)
    p = getP(q, 160)
    print("------")
    print(q)
    print(p)
    print(H.hexdigest())

if "__main__" == __name__:
    main()