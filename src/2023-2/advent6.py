import itertools
import math
import re

ts, ds = (re.findall(r'\d+', s) for s in open('data/06.txt'))
wins = lambda t, d: t - 2 * len(list(itertools.takewhile(lambda x: x * (t - x) <= d, range(t)))) + 1
print(math.prod([wins(int(t), int(d)) for t, d in zip(ts, ds)]))
print(wins(int(''.join(ts)), int(''.join(ds))))
