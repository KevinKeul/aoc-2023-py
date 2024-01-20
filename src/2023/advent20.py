import re
import time
from functools import reduce
from typing import List, Tuple, Dict, Match, Set


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent20(Exercise):

    def __init__(self, input_file: str):
        super().__init__(20, input_file)
        lines: List[Match] = [re.match('(.+) -> (.+)', x) for x in self.content.split('\n') if len(x) > 0]
        all_modules: Dict[str, List[str]] = {x.group(1): x.group(2).split(', ') for x in lines}
        self.destinations: Dict[str, List[str]] = {k.replace('%', '').replace('&', ''): v for k, v in
                                                   all_modules.items()}
        self.flips_states: Dict[str, bool] = {x[1:]: False for x in all_modules.keys() if x.startswith('%')}
        self.conjunction_states: Dict[str, Dict[str, int]] = {
            k[1:]: {f: 0 for f, t in self.destinations.items() if k[1:] in t}
            for k in all_modules.keys() if k.startswith('&')}
        self.counter = 0
        self.temp: Set[Tuple[int, str]] = set()

    def part_one(self) -> int:
        pulses = [self.push_button() for _ in range(1000)]
        lows = reduce(lambda v, nums: v + nums[0], pulses, 0)
        highs = reduce(lambda v, nums: v + nums[1], pulses, 0)
        return highs * lows

    def push_button(self):
        nums = [1, 0]
        remaining: List[Tuple[int, str, str]] = [(0, 'broadcaster', x) for x in self.destinations['broadcaster']]
        while len(remaining) > 0:
            pulse, previous, current = remaining.pop(0)
            if previous in ['mf', 'kb', 'fd', 'nh'] and pulse == 0:
                self.temp.add((self.counter, previous))
                # print(f'{self.counter}: {previous} -{"low" if pulse == 0 else "high"}-> {current}')
            nums[pulse] += 1
            if current in self.flips_states:
                if pulse == 0:
                    self.flips_states[current] = not self.flips_states[current]
                    for destination in self.destinations[current]:
                        remaining.append((1 if self.flips_states[current] else 0, current, destination))
            if current in self.conjunction_states:
                self.conjunction_states[current][previous] = pulse
                next_pulse = 0 if all(self.conjunction_states[current].values()) else 1
                for destination in self.destinations[current]:
                    remaining.append((next_pulse, current, destination))
        return nums[0], nums[1]

    def part_two(self) -> int:
        start = time.time()
        self.flips_states['rx'] = False
        while not self.flips_states['rx'] and self.counter < pow(2, 12):
            self.counter += 1
            self.push_button()
        print(f'Elapsed time: {time.time() - start}')
        return reduce(lambda x, y: x * y, [c for c, x in self.temp], 1)


def main():
    # exercise = Advent20('input2')
    # print('Test Solution 2 for part 1: ' + str(exercise.part_one()))
    # print('Test Solution 2 for part 2: ' + str(exercise.part_two()))
    # exercise = Advent20('input3')
    # print('Test Solution 3 for part 1: ' + str(exercise.part_one()))
    # print('Test Solution 3 for part 2: ' + str(exercise.part_two()))
    exercise = Advent20('input')
    # print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
