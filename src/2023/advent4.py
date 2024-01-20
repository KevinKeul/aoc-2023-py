import re


def part_one(nums):
    result = 0
    for num in nums:
        result += pow(2, num - 1) if num > 0 else 0
    return result


def part_two(nums):
    wins = [0 for _ in nums]
    for i, num in enumerate(reversed(nums)):
        added = 1
        for j in range(i - 1, i - 1 - num, -1):
            added += wins[j]
        wins[i] = added
    result = 0
    for num in wins:
        result += num
    return result


def get_wins(line):
    match = re.match('Card +(\\d+): (.*) \\| (.*)', line)
    lefts = [int(x) for x in match.group(2).split(' ') if len(x) > 0]
    rights = [int(x) for x in match.group(3).split(' ') if len(x) > 0]
    count = 0
    for right in rights:
        if right in lefts:
            count += 1
    return count


def main():
    result = 0
    with open('data/advent4.input.txt') as file:
        nums = [get_wins(line) for line in file.readlines()]
        result = part_two(nums)
    print(result)


if __name__ == '__main__':
    main()
