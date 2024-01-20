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


def count_rest(chars: str, s: str) -> int:
    match = re.match(f'^([{chars}]+)', s)
    return len(match.group(1)) if match else 0


class SpringRow:
    def __init__(self, row: str, hardness):
        match = re.match('^([.#?]+) ([\\d,]+)$', row)
        s = '?'.join([(match.group(1))] * hardness)
        self.springs: str = s + ' '
        self.sub_broken: List[int] = [s[x:].count('#') for x in range(len(s))] + [0] * 2
        self.sub_unknown: List[int] = [s[x:].count('?') for x in range(len(s))] + [0]
        self.sub_cons_dots: List[int] = [count_rest('.', s[x:]) for x in range(len(s))]
        self.sub_cons_non_dots: List[int] = [count_rest('?#', s[x:]) for x in range(len(s))]
        self.broken_groups: List[int] = [int(x) for x in match.group(2).split(',')] * hardness
        self.broken_numbers: List[int] = [sum(self.broken_groups[x:]) for x in range(len(self.broken_groups))]
        self.min_necessary: List[int] = [sum(self.broken_groups[x:]) + len(self.broken_groups) - x - 1 for x in
                                         range(len(self.broken_groups))]

    def count_arrangements(self) -> int:
        # print(f'{self.springs} {self.broken_groups}')
        return self._count(0, 0)

    def _count(self, group_index: int, spring_index: int) -> int:
        if len(self.broken_groups) == group_index:
            return 1 if self.sub_broken[spring_index] == 0 else 0
        if self.broken_numbers[group_index] > self.sub_broken[spring_index] + self.sub_unknown[spring_index]:
            return 0
        if self.min_necessary[group_index] > (len(self.springs) - spring_index):
            return 0
        dots = self.sub_cons_dots[spring_index]
        if dots > 0:
            return self._count(group_index, spring_index + dots)
        result = 0
        if self.springs[spring_index] == '?':
            result += self._count(group_index, spring_index + 1)
        current_group = self.broken_groups[group_index]
        if self.sub_cons_non_dots[spring_index] >= current_group:
            if self.springs[spring_index + current_group] == '#':
                return result
            result += self._count(group_index + 1, spring_index + current_group + 1)
        return result


class Advent12(Exercise):
    def __init__(self, input_file: str):
        super().__init__(12, input_file)

    def part_one(self) -> int:
        spring_rows = [SpringRow(x, 1) for x in self.content.split('\n') if len(x) > 0]
        rows_ = [x.count_arrangements() for x in spring_rows]
        return sum(rows_)

    def part_two(self) -> int:
        spring_rows = [SpringRow(x, 5) for x in self.content.split('\n') if len(x) > 0]
        rows_ = [x.count_arrangements() for x in spring_rows]
        return sum(rows_)


def main():
    exercise = Advent12('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent12('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
