import re
from typing import Dict, List


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent15(Exercise):
    def __init__(self, input_file: str):
        super().__init__(15, input_file)
        self.steps = self.content.split(',')

    def part_one(self) -> int:
        return sum([self.hash_function(step) for step in self.steps])

    def part_two(self) -> int:
        boxes: Dict[int, List[str]] = dict()
        values: Dict[str, int] = dict()
        for step in self.steps:
            match = re.match('(\\w+)(=(\\d+)|-)', step)
            label = match.group(1)
            box_number = self.hash_function(label)
            if match.group(3):
                value = match.group(3)
                box = boxes.setdefault(box_number, [])
                if label not in box:
                    box.append(label)
                values[label] = int(value)
            else:
                box = boxes.setdefault(box_number, [])
                if label in box:
                    box.remove(label)
        result = 0
        for box_number, box in boxes.items():
            for label_num, label in enumerate(box):
                val = (box_number + 1) * (label_num + 1) * values[label]
                result += val
        return result

    @staticmethod
    def hash_function(step: str) -> int:
        current = 0
        for letter in step:
            current += ord(letter)
            current *= 17
            current = current % 256
        return current


def main():
    exercise = Advent15('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent15('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
