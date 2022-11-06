import argparse
import string
import math
from datetime import datetime
import random
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("original", help="Original string", type=str)
parser.add_argument("a", type=int)
parser.add_argument("u", type=int)
parser.add_argument("m", type=int)
parser.add_argument("Y0", type=int)
parser.add_argument("--encode", help="If exist original will be encode.", action="store_true")
parser.add_argument("--decode", help="If exist original will be decode.", action="store_true")
args = parser.parse_args()

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def getGamma(length, a, u, m, Y0):
    result = []
    result.append(Y0)
    for i in range(0, length):
        result.append((a*result[i-1] + u) % m)
    return result


def encode(original, a, u, m, Y0):
    result = []
    original = list(chunks(original, 8))
    gammaBuffer = [Y0]
    for elements in original:
        firstY = gammaBuffer[len(gammaBuffer) - 1]
        gammaBuffer = getGamma(len(elements), a, u, m, firstY)
        counter = len(elements) - 1
        for element in elements:
            code = ord(element)
            result.append(chr(code ^ gammaBuffer[counter]))
    return result
    

def decode(original, a, u, m, Y0):
    result = []
    original = list(chunks(original, 8))
    gammaBuffer = [Y0]
    for elements in original:
        firstY = gammaBuffer[len(gammaBuffer) - 1]
        gammaBuffer = getGamma(len(elements), a, u, m, firstY)
        counter = len(elements) - 1
        for element in elements:
            code = ord(element)
            result.append(chr(code ^ gammaBuffer[counter]))
    return result

def main():
    encoded = 0
    a = args.a
    u = args.u
    m = args.m
    Y0 = args.Y0
    if args.encode:
        encoded = encode(args.original, a, u, m, Y0)
        encoded_str = "".join(encoded)
        print("Encoded string:\n" + encoded_str)
    if args.decode:
        decoded = decode(encoded, a, u, m, Y0)
        decoded_str = "".join(decoded)
        print("Decoded string:\n" + decoded_str)
    

if __name__ == "__main__":
    start_time = datetime.now()
    main()
    end_time = datetime.now()
    print("Delta: " + str((end_time - start_time).microseconds))