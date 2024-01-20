import itertools
import math
import re


def calc_steps(current):
    for i, inst in enumerate(itertools.cycle(insts), start=1):
        current = network[current][inst == 'R']
        if current.endswith('Z'):
            return i


insts, _, *network = [x.strip() for x in open('data/08.txt')]
network = {k: (l, r) for k, l, r in [re.findall(r'\w+', x) for x in network]}
print(calc_steps('AAA'))
print(math.lcm(*[calc_steps(x) for x in network.keys() if x.endswith('A')]))
