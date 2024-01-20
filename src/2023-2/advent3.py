import math
import re
from itertools import product


def get_match_coords(pattern):
    return {(j, i): match
            for j, line in enumerate(open('data/03.txt'))
            for match in re.finditer(pattern, line)
            for i in range(match.start(1), match.end(1))}


nums = get_match_coords(r'(\d+)')
parts = get_match_coords(r'([^0-9.\s])')
gears = {k: x for k, x in parts.items() if x.group(1) == '*'}
print(sum(int(m.group(1)) for m in
          {nums[k] for j, i in parts.keys() for k in product(range(j - 1, j + 2), range(i - 1, i + 2)) if k in nums}))
print(sum(math.prod([int(m.group(1)) for m in gear_numbers]) for gear_numbers in
          [{nums[k] for k in product(range(j - 1, j + 2), range(i - 1, i + 2)) if k in nums} for j, i in gears.keys()]
          if len(gear_numbers) == 2))
