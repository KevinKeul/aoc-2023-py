import datetime
import heapq
import re
from functools import total_ordering
from typing import Dict, List, Tuple


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


OPPOSITE = {'>': '<', 'v': '^', '<': '>', '^': 'v'}


class Coordinate:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def add(self, other: 'Coordinate') -> 'Coordinate':
        return Coordinate(self.x + other.x, self.y + other.y)

    def multiply(self, value: int) -> 'Coordinate':
        return Coordinate(self.x * value, self.y * value)

    def in_bounds(self, max_x: int, max_y: int):
        return 0 <= self.x < max_x and 0 <= self.y < max_y

    def distance(self, other: 'Coordinate') -> int:
        return abs(other.x - self.x) + abs(other.y - self.y)

    def as_tuple(self):
        return self.x, self.y

    def betweens(self, other: 'Coordinate') -> List['Coordinate']:
        start_x = self.x if self.x < other.x else other.x
        start_y = self.y if self.y < other.y else other.y
        end_x = self.x + other.x - start_x
        end_y = self.y + other.y - start_y
        return [Coordinate(x, y)
                for x in range(start_x, end_x + 1)
                for y in range(start_y, end_y + 1)
                if (x != start_x and x != end_x) or (y != start_y and y != end_y)]

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __eq__(self, other: 'Coordinate'):
        return self.x == other.x and self.y == other.y


@total_ordering
class Path:
    def __init__(self, coord: Coordinate, way: str, cost: int):
        self.coordinate = coord
        self.way = way
        self.cost = cost
        self.order_key = (self.way[::-1]
                          .replace('>', 'a')
                          .replace('v', 'b')
                          .replace('<', 'c')
                          .replace('^', 'd'))

    def __str__(self):
        return f'{self.coordinate} - {self.way} - {self.cost}'

    def __lt__(self, other: 'Path'):
        return self.order_key < other.order_key

    def __eq__(self, other: 'Path'):
        return self.order_key == other.order_key


class Advent17(Exercise):

    def __init__(self, input_file: str):
        super().__init__(17, input_file)
        self.rows = [x for x in self.content.split('\n') if len(x) > 0]
        self.width = len(self.rows[0])
        self.height = len(self.rows)
        self.weights = {(x, y): int(cell) for y, row in enumerate(self.rows) for x, cell in enumerate(row)}

    @staticmethod
    def next_steps(way: str) -> str:
        if len(way) == 0:
            return '>v'
        if len(way) < 3:
            return '>v<^'.replace(OPPOSITE[way[-1]], '')
        if len({x for x in way[-3:]}) == 1:
            return '>v<^'.replace(OPPOSITE[way[-1]], '').replace(way[-1], '')
        return '>v<^'.replace(OPPOSITE[way[-1]], '')

    @staticmethod
    def next_steps_2(way: str) -> str:
        if len(way) == 0:
            return '>v'
        post = re.match('.*?(>+|v+|<+|\\^+)$', way).group(1)
        if len(post) < 4:
            return way[-1]
        if len(post) == 10:
            return '>v<^'.replace(OPPOSITE[way[-1]], '').replace(way[-1], '')
        return '>v<^'.replace(OPPOSITE[way[-1]], '')

    @staticmethod
    def get_move(move: str) -> Coordinate:
        if move == '>':
            return Coordinate(1, 0)
        if move == 'v':
            return Coordinate(0, 1)
        if move == '<':
            return Coordinate(-1, 0)
        if move == '^':
            return Coordinate(0, -1)
        return Coordinate(0, 0)

    def part_one(self) -> int:
        start = Coordinate(0, 0)
        end = Coordinate(self.width - 1, self.height - 1)

        frontier: List[Tuple[int, Path]] = []
        heapq.heappush(frontier, (0, Path(start, '', 0)))
        memory: Dict[str, int] = dict()

        head: Path
        while frontier:
            head = heapq.heappop(frontier)[1]
            if head.coordinate == end:
                break
            for next_step in self.next_steps(head.way):
                next_coordinate: Coordinate = head.coordinate.add(self.get_move(next_step))
                if next_coordinate.in_bounds(self.width, self.height):
                    next_way = head.way + next_step
                    next_cost = head.cost + self.weights[next_coordinate.as_tuple()]
                    memory_key = self.get_memory_key_part_1(next_way, next_coordinate)
                    if memory_key not in memory or next_cost < memory[memory_key]:
                        memory[memory_key] = next_cost
                        estimate = next_cost + end.distance(next_coordinate)
                        heapq.heappush(frontier, (estimate, Path(next_coordinate, next_way, next_cost)))
        print(head)
        return head.cost

    def part_two(self) -> int:
        start_time = datetime.datetime.now()
        start = Coordinate(0, 0)
        end = Coordinate(self.width - 1, self.height - 1)

        frontier: List[Tuple[int, Path]] = []
        heapq.heappush(frontier, (0, Path(start, '', 0)))
        memory: Dict[str, int] = dict()

        head: Path
        while frontier:
            head = heapq.heappop(frontier)[1]
            if head.coordinate == end:
                break
            for next_step in self.next_steps_2(head.way):
                direction_change_factor = 4 if len(head.way) == 0 or next_step != head.way[-1] else 1
                move = self.get_move(next_step).multiply(direction_change_factor)
                next_coordinate: Coordinate = head.coordinate.add(move)
                if next_coordinate.in_bounds(self.width, self.height):
                    next_way = head.way + next_step * direction_change_factor
                    next_cost = head.cost + self.weights[next_coordinate.as_tuple()]
                    if direction_change_factor > 1:
                        next_cost += sum(
                            [self.weights[x.as_tuple()] for x in next_coordinate.betweens(head.coordinate)])
                    memory_key = self.get_memory_key_part_2(next_way, next_coordinate)
                    if memory_key not in memory or next_cost < memory[memory_key]:
                        memory[memory_key] = next_cost
                        estimate = next_cost + end.distance(next_coordinate)
                        heapq.heappush(frontier, (estimate, Path(next_coordinate, next_way, next_cost)))
        print(head)
        elapsed = datetime.datetime.now() - start_time
        print(str(elapsed.total_seconds()))
        return head.cost

    def get_memory_key_part_1(self, next_way: str, next_coordinate: Coordinate):
        return str(next_coordinate) + (next_way if len(next_way) <= 3 else next_way[-3:])

    def get_memory_key_part_2(self, next_way: str, next_coordinate: Coordinate):
        return str(next_coordinate) + (next_way if len(next_way) <= 10 else next_way[-10:])


def main():
    exercise = Advent17('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent17('input')
    # print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
