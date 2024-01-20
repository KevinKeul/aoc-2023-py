from typing import List

ds = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
ws = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']


def num(s: str, lits: List[str], left: bool):
    indexes = [((ws.index(x) + 1) if x in ws else int(x), s.find(x) if left else s.rfind(x)) for x in lits if x in s]
    return sorted(indexes, key=lambda x: x[1], reverse=not left)[0][0]


print(sum([num(x, ds, True) * 10 + num(x, ds, False) for x in open('data/01.txt')]))
print(sum([num(x, ds + ws, True) * 10 + num(x, ds + ws, False) for x in open('data/01.txt')]))
