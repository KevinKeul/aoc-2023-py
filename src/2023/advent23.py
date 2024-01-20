import sys
import time
from typing import List, Tuple, Dict, Set


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


sys.setrecursionlimit(5000)
Coord = Tuple[int, int]


class Advent23(Exercise):
    FORBIDDEN = {(1, 0): '<', (0, 1): '^', (-1, 0): '>', (0, -1): 'v'}
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def __init__(self, input_file: str):
        super().__init__(23, input_file)
        lines = [line for line in self.content.split('\n') if len(line) > 0]
        self.h = len(lines)
        self.w = len(lines[0])
        self.map: List[List[str]] = [[cell for cell in line] for line in lines]
        self.map[0][1] = 'S'
        self.map[self.h - 1][self.w - 2] = 'E'
        self.start = (1, 1)
        self.end = (self.w - 2, self.h - 2)
        # print('\n'.join([''.join([c for c in line]) for line in self.field]))

    def count_length(self, current: Coord, _from: Coord) -> List[Coord]:
        # print(current)
        if current == self.end:
            return [self.end]
        x, y = current
        result = []
        for delta in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            next_x, next_y = x + delta[0], y + delta[1]
            next_field = self.map[next_y][next_x]
            if delta == _from or next_field in '#SE' or next_field == self.FORBIDDEN[delta]:
                continue
            further = self.count_length((next_x, next_y), (-delta[0], -delta[1]))
            if len(further) > len(result):
                result = [current] + further
        return result

    def part_one(self) -> int:
        path = self.count_length(self.start, (0, -1))
        return len(path) + 1

    def part_two(self) -> int:
        field: List[List[str]] = [[cell if cell in '#SE' else '.' for cell in line] for line in self.map]
        crosses: List[Coord] = [(x, y)
                                for y, line in enumerate(field)
                                for x, cell in enumerate(line)
                                if cell == '.' and self.is_cross(x, y, field)]
        points: List[Coord] = [self.start] + crosses + [self.end]
        connections: Dict[Coord, Dict[Coord, int]] = self.get_connections(points, field)
        temp: Set[Tuple[Coord, Coord]] = {(s, e) if s[1] < e[1] else (e, s)
                                          for s, es in connections.items()
                                          for e in es.keys()}
        temp_str = '\n'.join([f'{a[0][0]}/{a[0][1]} <--> {a[1][0]}/{a[1][1]}'
                              for a in sorted(temp, key=lambda x: (x[1], x[0]))])
        # print(temp_str)
        return self.find_2(connections, self.start, 1, set()) + 1

    def find_2(self, connections: Dict[Coord, Dict[Coord, int]], pos: Coord, length: int, already: Set[Coord]) -> int:
        if pos == self.end:
            return length
        longest = 0
        for target, distance in connections[pos].items():
            if target not in already:
                longest = max(longest, self.find_2(connections, target, length + distance, already.union([target])))
        return longest

    @staticmethod
    def is_cross(x, y, field):
        return sum([1 for x2, y2 in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                    if field[y2][x2] == '.']) > 2

    def get_connections(self, points: List[Coord], field: List[List[str]]) -> Dict[Coord, Dict[Coord, int]]:
        result: Dict[Coord, Dict[Coord, int]] = {point: dict() for point in points}
        for point in points:
            for d in self.directions:
                pos: Coord = (point[0] + d[0], point[1] + d[1])
                pre: Coord = point
                dist: int = 1
                go_on = True
                while go_on:
                    if pos in points:
                        result[point][pos] = dist
                        break
                    if field[pos[1]][pos[0]] in '#SE':
                        break
                    go_on = False
                    for delta in self.directions:
                        next_x, next_y = pos[0] + delta[0], pos[1] + delta[1]
                        next_field = field[next_y][next_x]
                        if (next_x, next_y) != pre and next_field == '.':
                            go_on = True
                            pre = pos
                            pos = (next_x, next_y)
                            dist = dist + 1
                            break
        return result


def main():
    start = time.time()
    exercise = Advent23('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent23('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))
    print(f'Elapsed time: {time.time() - start}')


if __name__ == '__main__':
    main()
