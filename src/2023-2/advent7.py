from collections import Counter

values = {k.translate(str.maketrans('AKQJT', 'fedcb')): int(v)
          for k, v in map(str.split, open('data/07.txt'))}
strength = lambda x: sum(map(x.count, x))
print(sum((i + 1) * values[v] for i, v in enumerate(sorted(values.keys(), key=lambda x: (strength(x), x)))))
values = {k.replace('c', '0'): v for k, v in values.items()}
replace_j = lambda x: x.replace('0', Counter(x.replace('0', '') if x != '00000' else x).most_common(1)[0][0])
print(sum((i + 1) * values[v] for i, v in enumerate(sorted(values.keys(), key=lambda x: (strength(replace_j(x)), x)))))
