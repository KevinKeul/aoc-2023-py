class Exercise:
    def __init__(self, advent: int, input_file: str):
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent6(Exercise):
    def __init__(self, input_file: str):
        super().__init__(6, input_file)
        lines = self.content.split('\n')
        self.times = [int(x.strip()) for x in lines[0][6:].split(' ') if len(x) > 0]
        self.distances = [int(x.strip()) for x in lines[1][10:].split(' ') if len(x) > 0]

    def part_one(self) -> int:
        result = 1
        for i in range(len(self.times)):
            time = self.times[i]
            compare_dist = self.distances[i]
            result *= len([x for x in self.calc_races(time) if x > compare_dist])
        return result

    def part_two(self) -> int:
        time = int(''.join([str(x) for x in self.times]))
        compare_dist = int(''.join([str(x) for x in self.distances]))
        return len([x for x in self.calc_races(time) if x > compare_dist])

    def calc_races(self, time: int):
        for i in range(time):
            yield i * (time - i)


def main():
    exercise = Advent6('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent6('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
