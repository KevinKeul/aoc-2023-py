import re
from functools import total_ordering
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


Coord = Tuple[int, int, int]


@total_ordering
class Brick:
    brick_counter = 1

    def __init__(self, line: str):
        m = re.match('(\\d+),(\\d+),(\\d+)~(\\d+),(\\d+),(\\d+)', line)
        x1, y1, z1 = int(m.group(1)), int(m.group(2)), int(m.group(3))
        x2, y2, z2 = int(m.group(4)), int(m.group(5)), int(m.group(6))
        self.name = 'A' + str(Brick.brick_counter)
        Brick.brick_counter += 1
        self.start: Coord = (min(x1, x2), min(y1, y2), min(z1, z2))
        self.end: Coord = (max(x1, x2), max(y1, y2), max(z1, z2))
        self.length: int = abs((x1 + y1 + z1) - (x2 + y2 + z2))
        self.belows: Set[Brick] = set()
        self.aboves: Set[Brick] = set()

    def set_z(self, z: int):
        self.end = (self.end[0], self.end[1], self.end[2] - self.start[2] + z)
        self.start = (self.start[0], self.start[1], z)

    def get_xy_tiles(self) -> List[Tuple[int, int]]:
        return [(x, y)
                for x in range(self.start[0], self.end[0] + 1)
                for y in range(self.start[1], self.end[1] + 1)]

    def __lt__(self, other: 'Brick'):
        return self.start[::-1] < other.start[::-1]

    def __eq__(self, other: 'Brick'):
        return self.start == other.start and self.length == other.length

    def __hash__(self):
        return hash((self.start, self.length))

    def __str__(self):
        return f'Brick({self.name} {self.start}~{self.end}, length {self.length})'


class Advent22(Exercise):
    def __init__(self, input_file: str):
        super().__init__(22, input_file)
        self.bricks = sorted([Brick(x) for x in self.content.split('\n') if len(x) > 0])
        lowest: Dict[Tuple[int, int], Tuple[int, Brick]] = dict()
        for brick in self.bricks:
            xy_tiles = brick.get_xy_tiles()
            max_z = max([lowest[t][0] for t in xy_tiles if t in lowest] + [0])
            brick.belows = {lowest[t][1] for t in xy_tiles if t in lowest if lowest[t][0] == max_z}
            for below in brick.belows:
                below.aboves.add(brick)
            brick.set_z(max_z + 1)
            for xy_tile in xy_tiles:
                lowest[xy_tile] = (brick.end[2], brick)

    def part_one(self) -> int:
        safe: Dict[str, bool] = {x.name: True for x in self.bricks}
        for brick in self.bricks:
            if len(brick.belows) == 1:
                safe[list(brick.belows)[0].name] = False
        return len([x for x in safe.values() if x])

    def part_two(self) -> int:
        result = 0
        for brick in self.bricks:
            missing: Set[Brick] = {brick}
            todos = [brick]
            while len(todos) > 0:
                todo = todos.pop(0)
                for above in todo.aboves:
                    if len(above.belows.difference(missing)) == 0:
                        todos.append(above)
                        missing.add(above)
            result += len(missing) - 1
        return result


def main():
    exercise = Advent22('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent22('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
