import re
from typing import List


def is_possible(line):
    games = line[line.find(":") + 1:].split(";")
    for game in games:
        if get_num(game, "red") > 12 or get_num(game, "green") > 13 or get_num(game, "blue") > 14:
            return False
    return True


def get_num(game, color) -> int:
    match = re.match('.* (\\d+) ' + color, game)
    return int(match.group(1)) if match else 0


def get_id(line):
    match = re.match("^Game (\\d+):", line)
    return int(match.group(1))


def part_one(line):
    if is_possible(line):
        return get_id(line)
    return 0


def min_game(line) -> List[int]:
    games = line[line.find(":") + 1:].split(";")
    current = [0, 0, 0]
    for game in games:
        current[0] = max(current[0], get_num(game, "red"))
        current[1] = max(current[1], get_num(game, "green"))
        current[2] = max(current[2], get_num(game, "blue"))
    return current


def power(mins: List[int]) -> int:
    return mins[0] * mins[1] * mins[2]


def part_two(line):
    result = power(min_game(line))
    print(result)
    return result


def main():
    result = 0
    with open('data/advent2.input.txt') as file:
        for line in file.readlines():
            result += part_two(line)
    print(result)


if __name__ == '__main__':
    main()
