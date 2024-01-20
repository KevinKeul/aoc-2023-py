import re
from functools import cache


@cache
def arrs(s: str, gs):
    if len(gs) == 0:
        return '#' not in s
    if s.count('#') + s.count('?') < sum(gs):
        return 0
    not_matching = 0 if s[0] == '#' else arrs(s[1:], gs)
    matching = 0 if '.' in s[0:gs[0]] or (len(s) > gs[0] and s[gs[0]] == '#') else arrs(s[gs[0] + 1:], gs[1:])
    return not_matching + matching


lines = [re.split(r'[, ]', x.strip()) for x in open('data/12.txt')]
print(sum([arrs(x[0], tuple([int(y) for y in x[1:]])) for x in lines]))
print(sum([arrs('?'.join([x[0]] * 5), tuple([int(y) for y in x[1:]] * 5)) for x in lines]))
