from typing import List, Dict, Tuple


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent10(Exercise):
    def __init__(self, input_file: str):
        super().__init__(10, input_file)
        init = [' ' + x.replace('.', ' ') + ' ' for x in self.content.split('\n') if len(x) > 0]
        init.insert(0, ' ' * len(init[1]))
        init.append(' ' * len(init[0]))
        self.field1 = [[x for x in line] for line in init]
        # self.field2 = [[x for x in line] for line in init]
        self.size = (len(self.field1[0]), len(self.field1))
        self.symbols: Dict[str, List[Tuple[int, int]]] = dict()
        self.symbols['|'] = [(0, 1), (0, -1)]
        self.symbols['-'] = [(1, 0), (-1, 0)]
        self.symbols['7'] = [(-1, 0), (0, 1)]
        self.symbols['J'] = [(-1, 0), (0, -1)]
        self.symbols['F'] = [(1, 0), (0, 1)]
        self.symbols['L'] = [(1, 0), (0, -1)]
        self.symbols['S'] = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def part_one(self) -> int:
        count = 1
        start = (-1, -1)
        while count > 0:
            count = 0
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    field = self.field1[y][x]
                    if field == 'S':
                        start = (x, y)
                    if field == ' ' or field == 'S':
                        continue
                    directions = self.symbols[field]
                    for di in directions:
                        other = self.field1[y + di[1]][x + di[0]]
                        if other == ' ' or (-di[0], -di[1]) not in self.symbols[other]:
                            self.field1[y][x] = ' '
                            count += 1

        temp = [[-1 for _ in self.field1[0]] for _ in self.field1]
        temp[start[1]][start[0]] = 0
        solution_1 = -1
        count = 1
        while count > 0:
            count = 0
            solution_1 += 1
            for x in range(self.size[0]):
                for y in range(self.size[1]):
                    field = self.field1[y][x]
                    val = temp[y][x]
                    if val >= 0:
                        continue
                    if field == ' ':
                        continue
                    directions = self.symbols[field]
                    for di in directions:
                        other_val = temp[y + di[1]][x + di[0]]
                        if other_val == solution_1:
                            temp[y][x] = other_val + 1
                            count += 1
        self.field1[start[1]][start[0]] = 'L'
        solution_2 = 0
        for y in range(self.size[1]):
            inside = False
            up = False
            down = False
            fields = self.field1[y]
            temps = temp[y]
            for x in range(self.size[0]):
                t = temps[x]
                if t == -1:
                    if inside:
                        solution_2 += 1
                    continue
                field = fields[x]
                directions = self.symbols[field]
                for di in directions:
                    if di[1] == 1:
                        up = False if up else True
                    if di[1] == -1:
                        down = False if down else True
                if up and down:
                    inside = True
                if not up and not down:
                    inside = False

        print(self.input_file + ' Solution for part 1: ' + str(solution_1))
        print(self.input_file + ' Solution for part 2: ' + str(solution_2))
        return solution_1

    def part_two(self) -> int:
        return super().part_two()


def main():
    Advent10('input2').part_one()
    Advent10('input3').part_one()
    Advent10('input').part_one()


if __name__ == '__main__':
    main()
