import re
from math import lcm
from typing import List, Dict, Tuple


class Exercise:
    def __init__(self, advent: int, input_file: str):
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent8(Exercise):

    def __init__(self, input_file: str):
        super().__init__(8, input_file)
        lines = [x for x in self.content.split('\n') if len(x) > 0]
        self.instructions = lines[0]
        self.l: Dict[str, str] = dict()
        self.r: Dict[str, str] = dict()
        for line in lines[1:]:
            match = re.match('(.+) = \\((.+), (.+)\\)', line)
            self.l[match.group(1)] = match.group(2)
            self.r[match.group(1)] = match.group(3)

    def part_one(self) -> int:
        current = 'AAA'
        current_instructions = ''
        result = 0
        while current != 'ZZZ':
            if len(current_instructions) == 0:
                current_instructions = self.instructions * 100
            inst = current_instructions[0]
            current_instructions = current_instructions[1:]
            current = self.l[current] if inst == 'L' else self.r[current]
            result += 1
        return result

    def part_two(self) -> int:
        currents = [x for x in self.l.keys() if x.endswith('A')]
        repititions = [dict() for _ in currents]
        rep_counts: List[Tuple[int, int]] = [(-1, -1) for _ in currents]
        ends: List[List[int]] = [[] for _ in currents]
        current_instructions = ''
        result = 0
        while (-1, -1) in rep_counts:
            if result % 1000000 == 0:
                print(f'{result}')
            if len(current_instructions) == 0:
                current_instructions = self.instructions
            inst = current_instructions[0]
            current_instructions = current_instructions[1:]
            currents = [self.l[x] if inst == 'L' else self.r[x] for x in currents]
            result += 1
            for i, current in enumerate(currents):
                if current[-1] == 'Z':
                    ends[i].append(result)
            for i, rep in enumerate(repititions):
                key = f'{currents[i]} {current_instructions}'
                if key in rep and rep_counts[i] == (-1, -1):
                    rep_counts[i] = (rep[key], result)
                    print(f'repitition: {i} - {rep_counts[i]} - {key}')
                rep[key] = result
        print(rep_counts)
        print(ends)
        print(lcm(*[x[0] for x in ends]))
        return result


def main():
    exercise = Advent8('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    exercise = Advent8('input3')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    exercise = Advent8('input4')
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent8('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
