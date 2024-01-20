from typing import List, Dict

MAX = 1000000000


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent14(Exercise):
    def __init__(self, input_file: str):
        super().__init__(14, input_file)
        self.rows: List[str] = [x for x in self.content.split('\n') if len(x) > 0]
        self.columns: List[str] = [''.join([x[i] for x in self.rows]) for i in range(len(self.rows[0]))]

    def part_one(self) -> int:
        northed = self.northening(self.columns)
        return sum([self.count(s) for s in northed])

    def part_two(self) -> int:
        current = self.columns
        memory: Dict[str, int] = dict()
        n = 0
        for i in range(MAX):
            print(n)
            if n == MAX:
                break
            self.print_field(current)

            k = ''.join(current)
            if k in memory and n < int(MAX / 10):
                print(f'{memory[k]} -> {i}')
                n = i
                diff = i - memory[k]
                n += int((MAX - i) / diff) * diff
            memory[k] = i

            current = self.northening(current)
            current = self.rotate(current)
            current = self.northening(current)
            current = self.rotate(current)
            current = self.northening(current)
            current = self.rotate(current)
            current = self.northening(current)
            current = self.rotate(current)
            n += 1
        return sum([self.count(s) for s in current])

    @staticmethod
    def northening(columns: List[str]) -> List[str]:
        result: List[str] = []
        for column in columns:
            parts = [''.join(reversed(sorted(x))) for x in (column.split('#'))]
            result.append('#'.join(parts))
        return result

    @staticmethod
    def count(s: str) -> int:
        return sum([i + 1 for i, x in enumerate(reversed(s)) if x == 'O'])

    @staticmethod
    def rotate(lines: List[str]) -> List[str]:
        width = len(lines[0])
        return [''.join([x[width - i - 1] for x in lines]) for i in range(width)]

    @staticmethod
    def print_field(current: List[str]):
        result = ''
        for i in range(len(current[0])):
            result += ''.join([x[i] for x in current]) + '\n'
        print(result)


def main():
    exercise = Advent14('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent14('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
