from typing import List, Tuple


class Board:
    def __init__(self, board: str):
        lines: List[str] = board.split()
        size = [len(lines[0]), len(lines)]

        fields: List[List[int]] = [[0 for _ in range(size[0] + 2)] for _ in range(size[1] + 2)]
        self.numbers: List[List[int]] = [[-1 for _ in range(size[0] + 2)]]
        self.parts: List[List[int]] = [[0 for _ in range(size[0] + 2)]]
        self.numbers_list: List[int] = []
        self.parts_coordinates: List[Tuple[int, int]] = []
        self.possible_gear_coordinates: List[Tuple[int, int]] = []
        current_numbers = [-1]
        current_parts = [0]
        for y, l in enumerate(lines):
            line = l + '.'
            current_num = 0
            for x, char in enumerate(line):
                if char in '0123456789':
                    current_num = current_num * 10 + int(char)
                    current_numbers.append(len(self.numbers_list))
                    current_parts.append(0)
                else:
                    if current_num > 0:
                        self.numbers_list.append(current_num)
                        current_num = 0
                    current_numbers.append(-1)
                    if char in '.':
                        current_parts.append(0)
                    else:
                        current_parts.append(1)
                        self.parts_coordinates.append((x + 1, y + 1))
                        if char in '*':
                            self.possible_gear_coordinates.append((x + 1, y + 1))
            current_numbers.append(-1)
            self.numbers.append(current_numbers)
            current_numbers = [-1]
            current_parts.append(0)
            self.parts.append(current_parts)
            current_parts = [0]
        self.numbers.append([-1 for _ in range(size[0] + 2)])
        self.parts.append([0 for _ in range(size[0] + 2)])
        print()

    def first_part(self):
        relevants = set()
        for x, y in self.parts_coordinates:
            relevants.add(self.numbers[y - 1][x - 1])
            relevants.add(self.numbers[y - 1][x])
            relevants.add(self.numbers[y - 1][x + 1])
            relevants.add(self.numbers[y][x - 1])
            relevants.add(self.numbers[y][x])
            relevants.add(self.numbers[y][x + 1])
            relevants.add(self.numbers[y + 1][x - 1])
            relevants.add(self.numbers[y + 1][x])
            relevants.add(self.numbers[y + 1][x + 1])
        sum = 0
        for relevant in relevants:
            if relevant >= 0:
                sum += self.numbers_list[relevant]
        return sum

    def seconed_part(self):
        sum = 0
        for x, y in self.possible_gear_coordinates:
            relevants = set()
            relevants.add(self.numbers[y - 1][x - 1])
            relevants.add(self.numbers[y - 1][x])
            relevants.add(self.numbers[y - 1][x + 1])
            relevants.add(self.numbers[y][x - 1])
            relevants.add(self.numbers[y][x])
            relevants.add(self.numbers[y][x + 1])
            relevants.add(self.numbers[y + 1][x - 1])
            relevants.add(self.numbers[y + 1][x])
            relevants.add(self.numbers[y + 1][x + 1])
            relevants.remove(-1)
            if len(relevants) == 2:
                gear_parts = list(relevants)
                sum += self.numbers_list[gear_parts[0]] * self.numbers_list[gear_parts[1]]
        return sum


def main():
    result = 0
    with open('data/advent3.input.txt') as file:
        board = Board(file.read())
        result = board.first_part()
        result = board.seconed_part()
    print(result)


if __name__ == '__main__':
    main()
