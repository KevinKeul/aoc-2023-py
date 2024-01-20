import time
from typing import List, Tuple, Dict, Set


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()


class Advent21(Exercise):
    def __init__(self, input_file: str):
        super().__init__(21, input_file)
        lines = [x for x in self.content.split('\n') if len(x) > 0]
        self.h = len(lines)
        self.w = len(lines[0])
        self.fields: Dict[Tuple[int, int], str] = {(x, y): cell
                                                   for y, line in enumerate(lines)
                                                   for x, cell in enumerate(line)}
        self.start: Tuple[int, int] = [coord for coord, cell in self.fields.items() if cell == 'S'][0]

    def part_one(self, duration) -> int:
        oe: List[Set[Tuple[int, int]]] = [{self.start}, set()]
        for i in range(duration):
            oe[(i + 1) % 2].update([y for x in oe[i % 2] for y in self.neighbours(x) if self.fields[y] != '#'])
        return len(oe[0])

    def neighbours(self, current: Tuple[int, int]) -> List[Tuple[int, int]]:
        x, y = current
        return [c for c in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
                if 0 <= c[0] < self.w and 0 <= c[1] < self.h]

    def part_two(self, duration) -> int:
        half = self.start[0]
        full = self.w
        reach_full_e = self.calc_possibilities_single_field(1000, self.start)
        reach_full_o = self.calc_possibilities_single_field(1001, self.start)
        reach_quarter_e_ne = self.calc_possibilities_single_field(half - 1, (0, self.h - 1))
        reach_quarter_e_nw = self.calc_possibilities_single_field(half - 1, (self.w - 1, self.h - 1))
        reach_quarter_e_se = self.calc_possibilities_single_field(half - 1, (0, 0))
        reach_quarter_e_sw = self.calc_possibilities_single_field(half - 1, (self.w - 1, 0))
        reach_three_quarter_o_ne = self.calc_possibilities_single_field(full + half - 1, (0, self.h - 1))
        reach_three_quarter_o_nw = self.calc_possibilities_single_field(full + half - 1, (self.w - 1, self.h - 1))
        reach_three_quarter_o_se = self.calc_possibilities_single_field(full + half - 1, (0, 0))
        reach_three_quarter_o_sw = self.calc_possibilities_single_field(full + half - 1, (self.w - 1, 0))
        reach_side_o_n = self.calc_possibilities_single_field(full - 1, (half, self.h - 1))
        reach_side_o_e = self.calc_possibilities_single_field(full - 1, (0, half), True)
        reach_side_o_s = self.calc_possibilities_single_field(full - 1, (half, 0))
        reach_side_o_w = self.calc_possibilities_single_field(full - 1, (self.w - 1, half))
        num_center_side = self.start[0]
        num_remaining_side = duration - num_center_side
        num_full_fields_side = int(num_remaining_side / self.w)
        num_remaining_last_side = num_remaining_side % self.w

        n = num_full_fields_side
        return ((n - 1) * (n - 1) * reach_full_o +
                n * n * reach_full_e +
                n * (reach_quarter_e_ne + reach_quarter_e_nw + reach_quarter_e_se + reach_quarter_e_sw) +
                (n - 1) * (
                        reach_three_quarter_o_ne + reach_three_quarter_o_nw + reach_three_quarter_o_se + reach_three_quarter_o_sw) +
                reach_side_o_n + reach_side_o_e + reach_side_o_s + reach_side_o_w)

    def calc_possibilities_single_field(self, duration, start, draw=False):
        oe: List[Set[Tuple[int, int]]] = [{start}, set()]
        total: List[Set[Tuple[int, int]]] = [{start}, set()]
        for i in range(duration):
            pre = i % 2
            now = 1 - pre
            oe[now] = set([y for x in oe[pre] for y in self.neighbours(x) if self.fields[y] != '#']).difference(oe[now])
            total[now].update(oe[now])
        if draw:
            self.draw_fields(total[duration % 2])
        return len(total[duration % 2])

    def draw_fields(self, fields):
        print('\n'.join([''.join(['O' if (x, y) in fields else self.fields[(x, y)] for x in range(self.w)])
                         for y in range(self.h)]))


def main():
    start = time.time()
    # exercise = Advent21('input2')
    # print('Test Solution 2 for part 1: ' + str(exercise.part_one(6)))
    # print('Test Solution 2 for part 2: ' + str(exercise.part_two(6)))
    exercise = Advent21('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one(64)))
    print('Actual Solution for part 2: ' + str(exercise.part_two(26501365)))
    # exercise.calc_possibilities_single_field(131, (exercise.w - 1, exercise.start[1]), True)
    print(f'Elapsed time: {time.time() - start}')


if __name__ == '__main__':
    main()
