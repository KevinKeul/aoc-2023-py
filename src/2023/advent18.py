import re
from typing import List, Tuple, Match


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Vec2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __add__(self, other: 'Vec2'):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: 'Vec2'):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other: int):
        return Vec2(self.x * other, self.y * other)

    def min(self, other: 'Vec2'):
        return Vec2(self.x if self.x < other.x else other.x, self.y if self.y < other.y else other.y)

    def max(self, other: 'Vec2'):
        return Vec2(self.x if self.x > other.x else other.x, self.y if self.y > other.y else other.y)

    def as_tuple(self):
        return self.x, self.y

    def get_betweens(self, other: 'Vec2') -> List['Vec2']:
        start = self.min(other)
        end = self.max(other)
        return [Vec2(x, y)
                for x in range(start.x, end.x + 1)
                for y in range(start.y, end.y + 1)
                if (x != start.x and x != end.x) or (y != start.y and y != end.y)]

    def __str__(self):
        return f'Vec2({self.x}, {self.y})'


class Line:
    DIRS = {'R': Vec2(1, 0), 'D': Vec2(0, 1), 'L': Vec2(-1, 0), 'U': Vec2(0, -1)}
    OPPOSITE = {'R': 'L', 'D': 'U', 'L': 'R', 'U': 'D'}

    def __init__(self, direction: str, length: int):
        self.direction: str = direction
        self.length: int = length
        self.position: None | Vec2 = None
        self.end: None | Vec2 = None
        self.directions = self.direction
        self.ud: str = ''
        self.vector: Vec2 = Line.DIRS[self.direction] * self.length

    def set_position(self, pos: Vec2):
        self.position = pos
        self.end = pos + self.vector

    def set_opposite(self, incoming: str):
        self.directions += Line.OPPOSITE[incoming]
        self.ud = 'U' if 'U' in self.directions else 'D'

    def __str__(self):
        return f'{self.position} {self.length} {self.direction} {self.directions}'


class Advent18(Exercise):

    def __init__(self, input_file: str):
        super().__init__(18, input_file)
        self.rows: List[str] = [x for x in self.content.split('\n') if len(x) > 0]

    @staticmethod
    def position_lines(lines) -> Vec2:
        current = Vec2(0, 0)
        min_coord = Vec2(0, 0)
        max_coord = Vec2(0, 0)
        for line in lines:
            current = current + line.vector
            min_coord = min_coord.min(current)
            max_coord = max_coord.max(current)
        max_coord = max_coord - min_coord + Vec2(1, 1)
        current = Vec2(0, 0) - min_coord
        current_direction = lines[-1].direction
        for line in lines:
            line.set_position(current)
            line.set_opposite(current_direction)
            current_direction = line.direction
            current = current + line.vector
        return max_coord

    @staticmethod
    def get_rows(lines, max_coord):
        rows: List[List[Tuple[int, str]]] = [[] for y in range(max_coord.y)]
        for line in lines:
            if line.direction in 'UD':
                rows[line.position.y].append((line.position.x, line.ud))
                start = line.position.min(line.end)
                end = line.position.max(line.end)
                for y in range(start.y + 1, end.y):
                    rows[y].append((line.position.x, '|'))
            else:
                rows[line.position.y].append((line.position.x, line.ud))
        return rows

    def count(self, row: List[Tuple[int, str]]):
        result = 0
        inside = False
        has_u = False
        has_d = False
        prev = 0
        for (x, field) in row:
            if inside or has_u or has_d:
                result += x - prev - 1
            if field == '|':
                inside = not inside
                has_u = not has_u
                has_d = not has_d
            if field == 'U':
                has_u = not has_u
                inside = has_u and has_d
            if field == 'D':
                has_d = not has_d
                inside = has_u and has_d
            prev = x
        return result + len(row)

    def count_fields(self, lines):
        cache = dict()
        result = 0
        max_coord = self.position_lines(lines)
        rows = self.get_rows(lines, max_coord)
        for row in rows:
            key = tuple(row)
            if key in cache:
                result += cache[key]
            else:
                print(key)
                cache[key] = self.count(sorted(row))
                result += cache[key]
        return result

    def part_one(self) -> int:
        matches: List[Match[str]] = [re.match('^([RDLU]) (\\d+)', x) for x in self.rows]
        lines = [Line(x.group(1), int(x.group(2))) for x in matches]
        return self.count_fields(lines)

    def part_two(self) -> int:
        str_directions = 'RDLU'
        matches: List[Match[str]] = [re.match('.*\\(#(\\w+)(\\d)\\)', x) for x in self.rows]
        lines = [Line(str_directions[int(x.group(2))], int(x.group(1), 16)) for x in matches]
        return self.count_fields(lines)


def main():
    exercise = Advent18('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent18('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
