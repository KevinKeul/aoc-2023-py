from typing import Dict, List, Tuple, Set


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


tile_dir: Dict[str, Dict[str, str]] = {
    '/': {'D': 'L', 'L': 'D', 'U': 'R', 'R': 'U'},
    '\\': {'D': 'R', 'L': 'U', 'U': 'L', 'R': 'D'},
    '-': {'D': 'LR', 'L': 'L', 'U': 'LR', 'R': 'R'},
    '|': {'D': 'D', 'L': 'DU', 'U': 'U', 'R': 'DU'}
}


class Tile:
    def __init__(self, char: str, x: int, y: int):
        self.type = char
        self.x = x
        self.y = y
        self.neighbours: Dict[str, Tile] = dict()

    def continued_dirs(self, direction: str) -> List[str]:
        return [x for x in tile_dir[self.type][direction]]

    def distance(self, other: 'Tile'):
        return abs(other.y - self.y) + abs(other.x - self.x)

    def get_passed(self, point: Tuple[int, int]) -> Set[Tuple[int, int]]:
        start_x = self.x if self.x < point[0] else point[0]
        start_y = self.y if self.y < point[1] else point[1]
        end_x = self.x + point[0] - start_x
        end_y = self.y + point[1] - start_y
        return {(x, y) for y in range(start_y, end_y + 1) for x in range(start_x, end_x + 1)}

    def __str__(self):
        return f'{self.type}[{self.x} {self.y}]'


class Advent16(Exercise):
    def __init__(self, input_file: str):
        super().__init__(16, input_file)
        self.lines: List[str] = [line for line in reversed(self.content.split('\n')) if len(line) > 0]
        self.width = len(self.lines[0])
        self.height = len(self.lines)
        self.tiles: Dict[Tuple[int, int], Tile] = {(x, y): Tile(cell, x, y)
                                                   for y, line in enumerate(self.lines)
                                                   for x, cell in enumerate(line)
                                                   if cell != '.'}
        for y in range(self.height):
            current: Tile | None = None
            for x in range(self.width):
                other: Tile | None = self.tiles.get((x, y))
                if other:
                    if current:
                        current.neighbours['R'] = other
                        other.neighbours['L'] = current
                    current = other
        for x in range(self.width):
            current: Tile | None = None
            for y in range(self.height):
                other: Tile | None = self.tiles.get((x, y))
                if other:
                    if current:
                        current.neighbours['U'] = other
                        other.neighbours['D'] = current
                    current = other

    def calc_starting_tile(self, direction, other_axis):
        point = self.make_tuple(direction, 0 if direction in 'RU' else self.height - 1, other_axis)
        starting_tile: Tile = Tile('.', point[0], point[1])
        vals = [x for x in range(self.width) if self.make_tuple(direction, x, other_axis) in self.tiles]
        if len(vals) == 0:
            return starting_tile
        val = vals[0] if direction in 'RU' else vals[-1]
        starting_tile.neighbours[direction] = self.tiles[self.make_tuple(direction, val, other_axis)]
        return starting_tile

    @staticmethod
    def make_tuple(direction: str, value: int, other_axis: int) -> Tuple[int, int]:
        if direction in 'LR':
            return value, other_axis
        if direction in 'UD':
            return other_axis, value
        return 0, 0

    def calculate(self, direction, starting_tile) -> int:
        result: Set[Tuple[int, int]] = set()
        still_left: List[(Tile, direction)] = [(starting_tile, direction)]
        already_done: Set[(Tile, direction)] = set()
        while len(still_left) > 0:
            current = still_left.pop(0)
            current_tile = current[0]
            directions = current[1]
            for direction in directions:
                if (current_tile, direction) in already_done:
                    continue
                if direction in current_tile.neighbours:
                    next_tile = current_tile.neighbours.get(direction)
                    result.update(next_tile.get_passed((current_tile.x, current_tile.y)))
                    continued_dirs = next_tile.continued_dirs(direction)
                    for continued_dir in continued_dirs:
                        still_left.append((next_tile, continued_dir))
                        already_done.add((current_tile, direction))
                else:
                    if direction == 'L':
                        result.update(current_tile.get_passed((0, current_tile.y)))
                    if direction == 'D':
                        result.update(current_tile.get_passed((current_tile.x, 0)))
                    if direction == 'R':
                        result.update(current_tile.get_passed((self.width - 1, current_tile.y)))
                    if direction == 'U':
                        result.update(current_tile.get_passed((current_tile.x, self.height - 1)))
        output = ''
        for y in range(self.height - 1, -1, -1):
            for x in range(self.width):
                output += '#' if (x, y) in result else '-'
            output += '\n'
        # print(output)
        return len(result)

    def part_one(self) -> int:
        direction: str = 'R'
        starting_tile = self.calc_starting_tile(direction, self.height - 1)
        return self.calculate(direction, starting_tile)

    def part_two(self) -> int:
        max_value: int = 0
        for direction in 'DRUL':
            for i in range(self.height):
                starting_tile = self.calc_starting_tile(direction, i)
                current_value = self.calculate(direction, starting_tile)
                if current_value > max_value:
                    max_value = current_value
        return max_value


def main():
    exercise = Advent16('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent16('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
