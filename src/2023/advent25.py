import re
import time
from random import randrange
from typing import List, Tuple, Dict, Set


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Advent25(Exercise):
    def __init__(self, input_file: str):
        super().__init__(25, input_file)
        lines = [line for line in self.content.split('\n') if len(line) > 0]
        self.conns: Dict[str, Set[str]] = dict()
        for line in lines:
            match = re.match('^(\\w+): (.+)$', line)
            left = match.group(1)
            for right in match.group(2).split(' '):
                self.conns.setdefault(left, set()).add(right)
                self.conns.setdefault(right, set()).add(left)
        self.comps: List[str] = [x for x in self.conns.keys()]

    def part_one(self) -> int:
        n = 10000
        counts: Dict[Tuple[str, str], int] = dict()
        for i in range(n):
            c1 = self.comps[randrange(0, len(self.comps))]
            c2 = self.comps[randrange(0, len(self.comps))]
            path: List[Tuple[str, str]] = self.calc_path(c1, c2)
            for s, e in path:
                key = (s, e) if s < e else (e, s)
                counts[key] = counts[key] + 1 if key in counts else 1
        counts_list: List[Tuple[Tuple[str, str], int]] = [(k, v) for k, v in counts.items()]
        counts_list.sort(key=lambda x: (-x[1], x[0]))
        x1, x2 = '', ''
        for i in range(3):
            x1, x2 = counts_list[i][0]
            self.conns[x1].remove(x2)
            self.conns[x2].remove(x1)
        left = self.count_connecting(x1)
        right = self.count_connecting(x2)
        return left * right

    def calc_path(self, c1: str, c2: str) -> List[Tuple[str, str]]:
        nexts: Dict[str, str] = dict()
        todos: List[str] = [c2]
        while len(todos) > 0:
            current = todos.pop(0)
            if current == c1:
                break
            for pre in self.conns[current]:
                if pre not in nexts:
                    nexts[pre] = current
                    todos.append(pre)
                    if pre == c1:
                        todos.clear()
                        break
        result: List[Tuple[str, str]] = []
        to_add = c1
        while to_add != c2:
            result.append((to_add, nexts[to_add]))
            to_add = nexts[to_add]
        return result

    def count_connecting(self, x: str) -> int:
        all_: Set[str] = set()
        already: Set[str] = set()
        todos: List[str] = [x]
        while len(todos) > 0:
            current = todos.pop(0)
            all_.update(self.conns[current])
            already.add(current)
            todos += [n for n in self.conns[current] if n not in already]
        return len(all_)

    def part_two(self) -> int:
        return super().part_two()


def main():
    start = time.time()
    exercise = Advent25('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent25('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))
    print(f'Elapsed time: {time.time() - start}')


if __name__ == '__main__':
    main()
