import itertools

lines = [list(map(int, x.split())) for x in open('data/09.txt')]
exf = lambda vs: vs[-1] + (0 if set(vs) == {0} else exf([y - x for x, y in itertools.pairwise(vs)]))
exb = lambda vs: vs[0] - (0 if set(vs) == {0} else exb([y - x for x, y in itertools.pairwise(vs)]))
print(sum(exf(x) for x in lines))
print(sum(exb(x) for x in lines))
