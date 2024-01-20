import re
from typing import List, Tuple, Dict


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

    def __init__(self, line: str):
        match = re.match('([RDLU]) (\\d+) \\(#(\\w\\w)(\\w\\w)(\\w\\w)\\)', line)
        self.direction: str = match.group(1)
        self.length: int = int(match.group(2))
        self.r: str = match.group(3)
        self.g: str = match.group(4)
        self.b: str = match.group(5)
        self.vector: Vec2 = Line.DIRS[self.direction] * self.length
        self.position: None | Vec2 = None
        self.directions = self.direction

    def set_position(self, pos: Vec2):
        self.position = pos

    def set_opposite(self, incoming: str):
        self.directions += Line.OPPOSITE[incoming]

    def __str__(self):
        return f'{self.position} -> {self.vector} (#{self.r}{self.g}{self.b})'


class Advent18(Exercise):

    def __init__(self, input_file: str):
        super().__init__(18, input_file)
        self.lines: List[Line] = [Line(x) for x in self.content.split('\n') if len(x) > 0]
        current = Vec2(0, 0)
        min_coord = Vec2(0, 0)
        max_coord = Vec2(0, 0)
        for line in self.lines:
            current = current + line.vector
            min_coord = min_coord.min(current)
            max_coord = max_coord.max(current)
        self.max_coord = max_coord - min_coord + Vec2(1, 1)
        current = Vec2(0, 0) - min_coord
        current_direction = self.lines[-1].direction
        for line in self.lines:
            line.set_position(current)
            line.set_opposite(current_direction)
            current_direction = line.direction
            current = current + line.vector
        self.field: Dict[Tuple[int, int], str] = {(x, y): '.'
                                                  for y in range(self.max_coord.y)
                                                  for x in range(self.max_coord.x)}
        current = Vec2(0, 0) - min_coord
        for line in self.lines:
            end = current + line.vector
            self.field[current.as_tuple()] = 'U' if 'U' in line.directions else 'D'
            for between in current.get_betweens(end):
                self.field[between.as_tuple()] = '#'
            current = end
        self.fill_insides()

    def fill_insides(self):
        for y in range(self.max_coord.y):
            inside = False
            has_u = False
            has_d = False
            for x in range(self.max_coord.x):
                field = self.field[(x, y)]
                if field == '#' and has_u == has_d:
                    inside = not inside
                    has_u = not has_u
                    has_d = not has_d
                if field == 'U':
                    has_u = not has_u
                    inside = has_u and has_d
                if field == 'D':
                    has_d = not has_d
                    inside = has_u and has_d
                if field == '.' and inside:
                    self.field[(x, y)] = 'O'

    def part_one(self) -> int:
        result = 0
        for y in range(self.max_coord.y):
            for x in range(self.max_coord.x):
                if self.field[(x, y)] != '.':
                    result += 1
        return result

    def part_two(self) -> int:
        return super().part_two()


def main():
    exercise = Advent18('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent18('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
