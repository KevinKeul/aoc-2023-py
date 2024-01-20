import math
import re
from functools import reduce


def nec(line: str):
    def update(current, x): current[x.group(2)] = max(int(x.group(1)), current[x.group(2)]); return current

    balls = [re.match(' (\\d+) ([rgb])', x) for x in line.split(':')[1].replace(';', ',').split(',')]
    return reduce(update, balls, {'r': 0, 'g': 0, 'b': 0})


def part_one(line):
    return nec(line)['r'] <= 12 and nec(line)['g'] <= 13 and nec(line)['b'] <= 14


print(sum([i + 1 for i, x in enumerate(open('data/02.txt')) if part_one(x)]))
print(sum([math.prod(nec(x).values()) for x in open('data/02.txt')]))
