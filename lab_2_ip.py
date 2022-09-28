import argparse
import string
import math
from datetime import datetime
import random
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument("original", help="Original string", type=str)
parser.add_argument("--show-grid", help="Shows ganarated grid.", action="store_true")
parser.add_argument("--encode", help="If exist original will be encode.", action="store_true")
parser.add_argument("--decode", help="If exist original will be decode.", action="store_true")
args = parser.parse_args()

def chunks(lst, n):
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def generateGrid():
    result = list(string.printable)
    m = round(math.sqrt(len(result)))
    return __generateGrid__(m, result)

def __generateGrid__(m, result):
    random.shuffle(result)
    return list(chunks(result, m))

def encode(original, grid):
    result = []
    original = list(chunks(original, 2))
    for pair in original:
        if len(pair) == 2 and pair[0] != pair[1]:
            xy0 = findXY(pair[0], grid)
            xy1 = findXY(pair[1], grid)
            result.append(grid[xy0[0]][xy1[1]])
            result.append(grid[xy1[0]][xy0[1]])
        else:
            result.append(pair[0])
            result.append("sys")

    return result
        
def findXY(element, grid):
    for x in range(0, len(grid)):
        for y in range(0, len(grid[0])):
            if grid[x][y] == element:
                return (x, y)


def decode(original, grid):
    result = []
    original = list(chunks(original, 2))
    for pair in original:
        if pair[1] != "sys":
            xy0 = findXY(pair[0], grid)
            xy1 = findXY(pair[1], grid)
            result.append(grid[xy0[0]][xy1[1]])
            result.append(grid[xy1[0]][xy0[1]])
        else: 
            result.append(pair[0])
            result.append(pair[0])
    return result

def main():
    start_time = datetime.now()
    grid = generateGrid()
    encoded = 0
    if args.encode:
        encoded = encode(args.original, grid)
        encodedNp = np.array(encoded)
        encodedStr = "".join(encodedNp.flatten())
        print("Encoded string:\n" + encodedStr)
    if args.decode:
        print("Decoded string:\n" + "".join(decode(encoded, grid)))
    print("Delta: " + str(datetime.now() - start_time))
    if args.show_grid:
        print("")
        print("####CODE_GRID####")
        print(grid)
    

if __name__ == "__main__":
    main()