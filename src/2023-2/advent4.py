import re


def part_two(nums):
    wins = [0 for _ in nums]
    for i, num in enumerate(reversed(nums)):
        wins[i] = 1 + sum(wins[i - num: i])
    return sum(wins)


def get_wins(line):
    return len(set.intersection(*[set(re.findall(r'\d+', x)) for x in line.split(':')[1].split('|')]))


games = [get_wins(line) for line in open('data/04.txt')]
print(sum(pow(2, x - 1) for x in games if x > 0))
print(part_two(games))
