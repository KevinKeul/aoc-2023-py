class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Field:
    def __init__(self, input_field: str):
        self.rows = input_field.split('\n')
        self.columns = [''.join([row[i] for row in self.rows]) for i in range(len(self.rows[0]))]

    def horizontal_reflection(self, errors: int = 0) -> int:
        for mirror in range(1, len(self.rows)):
            if self.test_mirror(mirror, self.rows) == errors:
                return mirror
        return 0

    def vertical_reflection(self, errors: int = 0) -> int:
        for mirror in range(1, len(self.columns)):
            if self.test_mirror(mirror, self.columns) == errors:
                return mirror
        return 0

    @staticmethod
    def test_mirror(mirror, lines):
        return sum([Field.distance(lines[i], lines[mirror * 2 - 1 - i]) for i in range(mirror) if
                    mirror * 2 - 1 - i < len(lines)])

    @staticmethod
    def distance(l1, l2):
        return sum([1 for i in range(len(l1)) if l1[i] != l2[i]])


class Advent13(Exercise):
    def __init__(self, input_file: str):
        super().__init__(13, input_file)
        self.fields = [Field(x) for x in self.content.split('\n\n') if len(x) > 0]

    def part_one(self) -> int:
        return (sum([x.vertical_reflection() for x in self.fields])
                + sum([x.horizontal_reflection() for x in self.fields]) * 100)

    def part_two(self) -> int:
        return (sum([x.vertical_reflection(1) for x in self.fields])
                + sum([x.horizontal_reflection(1) for x in self.fields]) * 100)


def main():
    exercise = Advent13('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent13('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
