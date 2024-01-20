import itertools


def distances(factor):
    return [(sum(1 if x in single_x else factor for x in range(x1, x2, 1 if x2 > x1 else -1)) +
             sum(1 if y in single_y else factor for y in range(y1, y2, 1 if y2 > y1 else -1)))
            for (x1, y1), (x2, y2) in (list(itertools.combinations(gs, 2)))]


gs = [(x, y) for y, l in enumerate(open('data/11.txt')) for x, c in enumerate(l.strip()) if c == '#']
single_x = {x for x, _ in gs}
single_y = {y for _, y in gs}
print(sum(distances(2)))
print(sum(distances(1000000)))
