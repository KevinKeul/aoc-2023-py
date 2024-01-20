import re
from typing import List, Tuple, Dict


class Exercise:
    def __init__(self, advent: int, input_file: str):
        self.input_file = input_file
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


Range = Tuple[int, int]


class Rule:
    PART_INDEX = {'x': 0, 'm': 1, 'a': 2, 's': 3}

    def __init__(self, rule: str):
        match = re.match('([xmas])([<>])(\\d+):(\\w+)', rule)
        if match:
            self.part = match.group(1)
            self.compare = match.group(2)
            self.value = int(match.group(3))
            self.target = match.group(4)
        else:
            self.part = None
            self.compare = None
            self.value = None
            self.target = rule

    def part_index(self):
        return Rule.PART_INDEX[self.part]

    def __str__(self):
        if not self.part:
            return f'{self.target}'
        return f'{self.part}{self.compare}{self.value}:{self.target}'

    def evaluate(self, part: 'Part') -> str:
        if not self.part:
            return self.target
        v = int(getattr(part, self.part))
        return self.target if (v > self.value if self.compare == '>' else v < self.value) else ''


class RuleSet:
    def __init__(self, line: str):
        match = re.match('(\\w+)\\{(.+)}', line)
        self.name = match.group(1)
        self.rules = [Rule(x) for x in match.group(2).split(',')]
        self.trivial = False

    def __str__(self):
        return f'{self.name}{{{",".join(str(x) for x in self.rules)}}}'

    def evaluate(self, part: 'Part') -> str:
        for rule in self.rules:
            rule_result = rule.evaluate(part)
            if len(rule_result) > 0:
                return rule_result
        return ''

    def simplify(self):
        if len({x.target for x in self.rules}) == 1:
            # print(f'Make triviel: {self}')
            self.rules = [Rule(self.rules[0].target)]
            self.trivial = True

    def replace_target(self, old, new):
        for rule in self.rules:
            if rule.target == old:
                rule.target = new


class Part:
    def __init__(self, line: str):
        match = re.match('\\{x=(\\d+),m=(\\d+),a=(\\d+),s=(\\d+)}', line)
        self.x = int(match.group(1))
        self.m = int(match.group(2))
        self.a = int(match.group(3))
        self.s = int(match.group(4))

    def value(self):
        return self.x + self.m + self.a + self.s

    def __str__(self):
        return f'{{x={self.x},m={self.m},a={self.a},s={self.s}}}'


class Advent19(Exercise):

    def __init__(self, input_file: str):
        super().__init__(19, input_file)
        text = self.content.split('\n\n')
        rules: List[RuleSet] = [RuleSet(x) for x in text[0].split('\n') if len(x) > 0]
        self.rule_sets: Dict[str, RuleSet] = {x.name: x for x in rules}
        self.parts: List[Part] = [Part(x) for x in text[1].split('\n') if len(x) > 0]

    def part_one(self) -> int:
        result = 0
        for part in self.parts:
            current_rule_set = 'in'
            while current_rule_set not in ['R', 'A']:
                current_rule_set = self.rule_sets[current_rule_set].evaluate(part)
            if current_rule_set == 'A':
                result += part.value()
        return result

    def part_two(self) -> int:
        # self.remove_trivials()
        # self.remove_trivials()
        # self.remove_trivials()
        return self.count_possibilities(((1, 4000), (1, 4000), (1, 4000), (1, 4000)))

    def count_possibilities(self, current: Tuple[Range, Range, Range, Range], rule_set_name: str = 'in') -> int:
        if rule_set_name == 'ntr':
            print()
        if current[0][0] > current[0][1] or current[1][0] > current[1][1] or current[2][0] > current[2][1] or \
                current[3][0] > current[3][1]:
            return 0
        if rule_set_name == 'A':
            return self.count(current)
        if rule_set_name == 'R':
            return 0
        rule_set = self.rule_sets[rule_set_name]
        result = 0
        temp = list(current)
        for rule in rule_set.rules:
            if not rule.part:
                result += self.count_possibilities(tuple(temp), rule.target)
            if rule.part:
                part = temp[rule.part_index()]
                if rule.compare == '>':
                    temp[rule.part_index()] = (max(rule.value + 1, part[0]), part[1])
                    result += self.count_possibilities(tuple(temp), rule.target)
                    temp[rule.part_index()] = (part[0], min(rule.value, part[1]))
                else:
                    temp[rule.part_index()] = (part[0], min(rule.value - 1, part[1]))
                    result += self.count_possibilities(tuple(temp), rule.target)
                    temp[rule.part_index()] = (max(rule.value, part[0]), part[1])
        print(f'{rule_set_name} {result}')
        return result

    def count(self, current: Tuple[Range, Range, Range, Range]) -> int:
        return ((current[0][1] + 1 - current[0][0]) *
                (current[1][1] + 1 - current[1][0]) *
                (current[2][1] + 1 - current[2][0]) *
                (current[3][1] + 1 - current[3][0]))

    def remove_trivials(self):
        for rule_set in self.rule_sets.values():
            rule_set.simplify()
        trivials = [x for x in self.rule_sets.values() if x.trivial]
        # print(f'# trivial RuleSets = {len(trivials)}')
        for trivial in trivials:
            for rule_set in self.rule_sets.values():
                rule_set.replace_target(trivial.name, trivial.rules[0].target)
            self.rule_sets.pop(trivial.name)


def main():
    exercise = Advent19('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent19('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
