import re
from functools import reduce


def run_map(v, m):
    for t, s, l in m[1:]:
        if s <= v < s + l:
            return t - s + v
    return v


seeds, *mappings = [[[int(x) for x in re.findall(r'\d+', line)] for line in block.split('\n')]
                    for block in open('data/05.txt').read().split('\n\n')]
print(min(reduce(run_map, mappings, s) for s in seeds[0]))

rev_mappings = list(reversed([[(s, t, l) for t, s, l in m[1:]] for m in mappings]))
min_edges = {(i, s + e * l) for i, m in enumerate(mappings) for _, s, l in m[1:] + [[0, 0, 0]] for e in [0, 1]}
possible_seeds = [reduce(run_map, rev_mappings[len(rev_mappings) - k:], v) for k, v in min_edges]
to_check = [x for x in possible_seeds for s, e in zip(seeds[0][0::2], seeds[0][1::2]) if s <= x < s + e]
print(min(reduce(run_map, mappings, s) for s in to_check))
