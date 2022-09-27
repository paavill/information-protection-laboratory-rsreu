import argparse
from datetime import datetime
import random
import numpy as np
import collections
parser = argparse.ArgumentParser()
parser.add_argument("original", help="Original string", type=str)
parser.add_argument("m", type=int)
parser.add_argument("k", type=int)
parser.add_argument("--show-grid", help="Shows ganarated grid.", action="store_true")
parser.add_argument("--encode", help="If exist original will be encode.", action="store_true")
parser.add_argument("--decode", help="If exist original will be decode.", action="store_true")
args = parser.parse_args()

def generateGrid(m, k):
    result = []*2*k
    for i in range(2*k):
        result.append([])
        for j in range(2*m):
            result[i].append(True)
    size = m*k
    maxI = 2*k - 1
    maxJ = 2*m - 1
    while size > 0:
        i = random.randint(0, maxI)
        j = random.randint(0, maxJ)
        j180 = maxJ - j
        i360 = maxI - i
        j540 = maxJ - j180
        if result[i][j] and result[i][j180] and result[i360][j180] and result[i360][j540]:
            result[i][j] = False
            size = size - 1
    return result

def encode(original, grid, m, k):
    result = []*2*k
    for i in range(2*k):
        result.append([])
        for j in range(2*m):
            result[i].append(' ')

    originalList = list(original)
    counter = 0
    ind = 0
    maxI = 2*k - 1
    maxJ = 2*m - 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not(grid[i][j]) and counter <= len(originalList) and ind <= m*k:
                j180 = maxJ - j
                i360 = maxI - i
                j540 = maxJ - j180
                if ind < len(originalList):
                    result[i][j] = originalList[ind]
                    counter = counter + 1
                    if ind + m*k < len(originalList):
                        result[i][j180] = originalList[ind + m*k]
                        counter = counter + 1
                        if ind + 2*m*k < len(originalList):
                            result[i360][j180] = originalList[ind + 2*m*k]
                            counter = counter + 1
                            if ind + 3*m*k < len(originalList):
                                result[i360][j540] = originalList[ind + 3*m*k]
                                counter = counter + 1
                ind = ind + 1
    return result

def split(list_a, chunk_size):

  for i in range(0, len(list_a), chunk_size):
    yield list_a[i:i + chunk_size]

def decode(original, grid, m, k):
    result = {}
    originalList = original
    counter = 0
    ind = 0
    maxI = 2*k - 1
    maxJ = 2*m - 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if not(grid[i][j]) and ind <= m*k:
                j180 = maxJ - j
                i360 = maxI - i
                j540 = maxJ - j180
                #if originalList[i][j] != "sys":
                result[ind] = originalList[i][j]
                #if originalList[i][j180] != "sys":
                result[ind + m*k] = originalList[i][j180]
                #if originalList[i360][j180] != "sys":
                result[ind + 2*m*k] = originalList[i360][j180]
                #if originalList[i360][j540] != "sys":
                result[ind + 3*m*k] = originalList[i360][j540]
                ind = ind + 1
    sortedResult = collections.OrderedDict(sorted(result.items()))
    result = list(sortedResult.values())
    return result

def main():
    start_time = datetime.now()
    grid = generateGrid(args.m, args.k)
    encoded = 0
    if args.encode:
        encoded = encode(args.original, grid, args.m, args.k)
        gfg = np.array(encoded)
        flat_gfg = "".join(gfg.flatten())
        print("Encoded string: " + flat_gfg)
    if args.decode:
        print("Decoded string: " + "".join(decode(encoded, grid, args.m, args.k)))
    if args.show_grid:
        print("")
        print("####CODE_GRID####")
        print(grid)
    print("Delta: " + str(datetime.now() - start_time))

if __name__ == "__main__":
    main()