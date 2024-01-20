from typing import Tuple, List


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent11(Exercise):
    age = 2

    def __init__(self, input_file: str):
        super().__init__(11, input_file)
        self.lines = [[cell for cell in line] for line in self.content.split('\n')]
        self.xs = [i for i in range(len(self.lines[0]))]
        self.ys = [i for i in range(len(self.lines))]
        self.galaxies: List[Tuple[int, int]] = []
        for y, line in enumerate(self.lines):
            for x, cell in enumerate(line):
                if cell == '#':
                    if x in self.xs:
                        self.xs.remove(x)
                    if y in self.ys:
                        self.ys.remove(y)
                    self.galaxies.append((x, y))

    def calc_values(self, age):
        values = []
        for y, line in enumerate(self.lines):
            values_line = []
            for x, cell in enumerate(line):
                values_line.append(age if x in self.xs else 1)
            values.append([age if y in self.ys else x for x in values_line])
        return values

    def calc_distances(self, values):
        result = 0
        for g1 in self.galaxies:
            for g2 in self.galaxies:
                if g1 == g2:
                    continue
                dir_x = 1 if g2[0] > g1[0] else -1
                dir_y = 1 if g2[1] > g1[1] else -1
                for i in range(g1[0], g2[0] + dir_x, dir_x):
                    result += values[g1[1]][i]
                for j in range(g1[1], g2[1] + dir_y, dir_y):
                    result += values[j][g2[0]]
                result -= 2
        return result

    def part_one(self) -> int:
        values = self.calc_values(2)
        result = self.calc_distances(values)
        return int(result / 2)

    def part_two(self) -> int:
        values = self.calc_values(1000000)
        result = self.calc_distances(values)
        return int(result / 2)


def main():
    exercise = Advent11('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent11('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
