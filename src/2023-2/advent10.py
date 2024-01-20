import itertools

from HUtils import D, R, U, L, search_stack, Vec2i, inv_dir

symbols = {'L': {R, D}, 'F': {R, U}, 'J': {L, D}, '7': {L, U}, '|': {U, D}, '-': {R, L}, 'S': {R, L, U, D}, '.': {}}
m = {Vec2i(x, y): symbols[c] for y, l in enumerate(open('data/10.txt')) for x, c in enumerate(l.strip())}
s = [k for k, v in m.items() if len(v) == 4][0]
m[s] = {c for c in m[s] if s.add(c) in m and inv_dir[c] in m[s.add(c)]}
g = {k: {k.add(c) for c in v} for k, v in m.items()}
path2 = set(search_stack(s, lambda v, p: v == s and p,
                         lambda v, p: [x for x in g[v] if x != p],
                         done=lambda v, p: (v, p), return_history=True))
print(len(path2) // 2)
ups = {y: sorted([e.x for e in path2 if e.y == y and U in m[Vec2i(e.x, y)]]) for y in
       sorted(list(({e.y for e in path2})))}
ins = [len([x for x in range(l, r) if Vec2i(x, y) not in path2]) for y, xs in ups.items() for l, r in
       itertools.batched(xs, 2)]
print(sum(ins))
