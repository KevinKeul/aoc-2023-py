import re
from typing import Dict


class Rang:
    def __init__(self, s: int, to_add: int, right_start: int):
        self.left_start = s
        self.left_end = self.left_start + to_add
        self.right_start = right_start
        self.right_end = right_start + to_add

    def includes(self, num) -> bool:
        return self.left_start <= num < self.left_end

    def includes_back(self, num) -> bool:
        return self.right_start <= num < self.right_end

    def convert(self, num) -> int:
        return num - self.left_start + self.right_start

    def convert_back(self, num) -> int:
        return num - self.right_start + self.left_start


class Map:
    def __init__(self, part: str):
        lines = part.split('\n')
        title = re.match('(\\w+)-to-(\\w+) map:', lines.pop(0))
        self.left = title.group(1)
        self.right = title.group(2)
        self.ranges: list[Rang] = []
        for line in lines:
            destination, source, length = tuple(line.split(' '))
            self.ranges.append(Rang(int(source), int(length), int(destination)))

    def get(self, left_value):
        for rang in self.ranges:
            if rang.includes(left_value):
                return rang.convert(left_value)
        return left_value

    def get_back(self, right_value):
        for rang in self.ranges:
            if rang.includes_back(right_value):
                return rang.convert_back(right_value)
        return right_value


class Almanac:
    def __init__(self, text: str):
        parts = text.split('\n\n')
        seeds_str = re.match('seeds: ([\\d ]+)', parts.pop(0)).group(1).split(' ')
        self.seeds = [int(x) for x in seeds_str]
        maps = [Map(x) for x in parts]
        self.maps: Dict[str, Map] = {x.left: x for x in maps}
        self.maps_back: Dict[str, Map] = {x.right: x for x in maps}

    def get_location(self, seed):
        current_left = 'seed'
        current_value = seed
        while current_left != 'location':
            current_map = self.maps[current_left]
            current_left = current_map.right
            current_value = current_map.get(current_value)
        return current_value

    def get_possible_seed(self, start, current_right):
        current_value = start
        while current_right != 'seed':
            current_map = self.maps_back[current_right]
            current_right = current_map.left
            current_value = current_map.get_back(current_value)
        return current_value

    def get_possible_seeds(self):
        result = []
        for right, map_back in self.maps_back.items():
            result.append(self.get_possible_seed(0, right))
            for rang in map_back.ranges:
                result.append(self.get_possible_seed(rang.right_start, right))
                result.append(self.get_possible_seed(rang.right_end + 1, right))
        return result


def part_one(almanac):
    return [almanac.get_location(x) for x in almanac.seeds]


def part_two(almanac):
    seeds = almanac.seeds
    minimum = 4000000000
    possible_seeds = almanac.get_possible_seeds()
    for i in range(0, len(almanac.seeds), 2):
        print('Range: {}-{}'.format(seeds[i], seeds[i] + seeds[i + 1]))
        for j in [x for x in possible_seeds if seeds[i] <= x <= seeds[i] + seeds[i + 1]]:
            location = almanac.get_location(j)
            if location < minimum:
                print('New minimum ' + str(location))
                minimum = location
    return [minimum]


def main():
    result = 0
    with open('data/advent5.input.txt') as file:
        almanac = Almanac(file.read())
        locations = part_two(almanac)
        result = min(locations)
    print(result)


if __name__ == '__main__':
    main()
