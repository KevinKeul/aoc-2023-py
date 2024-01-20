from typing import List


class Exercise:
    def __init__(self, advent: int, input_file: str):
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent9(Exercise):

    def __init__(self, input_file: str):
        super().__init__(9, input_file)
        input_lines = [x for x in self.content.split('\n') if len(x) > 0]
        self.lines: List[List[int]] = [[int(x) for x in line.split(' ')] for line in input_lines]

    def part_one(self) -> int:
        return sum([self.extrapolate(x) for x in self.lines])

    def part_two(self) -> int:
        i = [self.extrapolate_back(x) for x in self.lines]
        return sum(i)

    def extrapolate(self, values) -> int:
        sub = []
        for i in range(len(values) - 1):
            sub.append(values[i + 1] - values[i])
        return values[-1] + (sub[0] if len(set(sub)) == 1 else self.extrapolate(sub))

    def extrapolate_back(self, values) -> int:
        sub = []
        for i in range(len(values) - 1):
            sub.append(values[i + 1] - values[i])
        return values[0] - (sub[0] if len(set(sub)) == 1 else self.extrapolate_back(sub))


def main():
    exercise = Advent9('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent9('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
