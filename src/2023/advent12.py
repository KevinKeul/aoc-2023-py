import re
from typing import List


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class SpringRow:
    def __init__(self, row: str):
        match = re.match('^([.#?]+) ([\\d,]+)$', row)
        s = match.group(1)
        self.springs: str = f'{s}?{s}?{s}?{s}?{s}'
        self.length: int = len(self.springs)
        self.known_groups: List[str] = self.springs.split('?') + ['']
        bs = [int(x) for x in match.group(2).split(',')]
        self.broken_groups: List[int] = bs * 5
        self.num_broken_springs = sum(self.broken_groups)
        self.num_working_springs = len(self.springs) - self.num_broken_springs
        self.num_to_find_broken = self.num_broken_springs - self.springs.count('#')
        self.num_to_find_working = self.num_working_springs - self.springs.count('.')

    def count_arrangements(self, already: str, current_group: int,
                           remaining_broken: int, remaining_working: int) -> int:
        if remaining_broken < 0 or remaining_working < 0:
            return 0
        if already == '':
            print(f'Starting: {self.springs} {self.broken_groups}')
        current = already + self.known_groups[current_group]
        further = self.__decide_next(current)
        if further == '':
            return 0
        if len(current) == self.length:
            if current.count('#') != self.num_broken_springs:
                return 0
            return 1
        result = 0
        if further in ['#', '?'] and remaining_broken > 0:
            result += self.count_arrangements(current + '#', current_group + 1, remaining_broken - 1, remaining_working)
        if further in ['.', '?'] and remaining_working > 0:
            result += self.count_arrangements(current + '.', current_group + 1, remaining_broken, remaining_working - 1)
        return result

    def __decide_next(self, known: str) -> str:
        groups = [len(x) for x in known.split('.') if len(x) > 0]
        if len(groups) == 0:
            return '?'
        last_known_index = len(groups) - 1
        if last_known_index >= len(self.broken_groups):
            return ''
        for i in range(last_known_index):
            if groups[i] != self.broken_groups[i]:
                return ''
        if groups[last_known_index] > self.broken_groups[last_known_index]:
            return ''
        if groups[last_known_index] < self.broken_groups[last_known_index]:
            if known.endswith('.'):
                return ''
            return '#'
        if groups[last_known_index] == self.broken_groups[last_known_index]:
            if known.endswith('#'):
                return '.'
        return '?'

    def __still_possible(self, current: str) -> bool:
        match = re.match('^([.#]*)?', current)
        groups = [len(x) for x in match.group(1).split('.') if len(x) > 0]
        last_known_index = len(groups) - 1
        for i in range(last_known_index):
            if groups[i] != self.broken_groups[i]:
                return False
        if groups[last_known_index] > self.broken_groups[last_known_index]:
            return False
        return True


class Advent12(Exercise):
    def __init__(self, input_file: str):
        super().__init__(12, input_file)
        self.spring_rows = [SpringRow(x) for x in self.content.split('\n') if len(x) > 0]

    def part_one(self) -> int:
        rows_ = []
        for i, x in enumerate(self.spring_rows):
            print(i)
            rows_.append(x.count_arrangements('', 0, x.num_to_find_broken, x.num_to_find_working))
        return sum(rows_)

    def part_two(self) -> int:
        return super().part_two()


def main():
    exercise = Advent12('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent12('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
