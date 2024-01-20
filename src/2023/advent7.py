from typing import List


class Exercise:
    def __init__(self, advent: int, input_file: str):
        with open('data/advent{}.{}.txt'.format(advent, input_file)) as file:
            self.content = file.read()

    def part_one(self) -> int:
        return 0

    def part_two(self) -> int:
        return 0


class Value:
    vals: List[str] = list(reversed(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']))

    def __init__(self, val: str):
        self.val = val

    def __lt__(self, other):
        for i in range(len(self.val)):
            if self.val[i] != other.val[i]:
                return self.index(self.val[i]) < self.index(other.val[i])

    def index(self, v):
        for i in range(len(Value.vals)):
            if v == Value.vals[i]:
                return i


class Hand:
    def __init__(self, parts: List[str]):
        self.hand = parts[0]
        self.bid = int(parts[1])
        self.letters = sorted([len([y for y in self.hand if y == x]) for x in self.hand], reverse=True)
        most = 'J'
        count = 0
        for c in self.hand:
            if c == 'J':
                continue
            if self.hand.count(c) > count:
                count = self.hand.count(c)
                most = c
        hand_j = self.hand.replace('J', most)
        self.letters_j = sorted([len([y for y in hand_j if y == x]) for x in hand_j], reverse=True)
        self.type = self.__get_type(self.letters)
        self.type_j = self.__get_type(self.letters_j)
        self.val = Value(self.hand)

    def __get_type(self, letters):
        if letters[0] == 5:
            return 7
        if letters[0] == 4:
            return 6
        if letters[0] == 3 and letters[3] == 2:
            return 5
        if letters[0] == 3:
            return 4
        if letters[0] == 2 and letters[2] == 2:
            return 3
        if letters[0] == 2:
            return 2
        return 1

    def __str__(self):
        return f'{self.hand} {self.bid}'


class Advent7(Exercise):
    def __init__(self, input_file: str):
        super().__init__(7, input_file)
        lines = [x for x in self.content.split('\n') if len(x) > 0]
        self.hands = [Hand(line.split()) for line in lines]

    def part_one(self) -> int:
        Value.vals = list(reversed(['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']))
        sorted_hands = self.hands
        sorted_hands = sorted(sorted_hands, key=lambda h: h.val)
        sorted_hands = sorted(sorted_hands, key=lambda h: h.type)
        result = 0
        for i, hand in enumerate(sorted_hands):
            result += (i + 1) * hand.bid
        return result

    def part_two(self) -> int:
        Value.vals = list(reversed(['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']))
        sorted_hands = self.hands
        sorted_hands = sorted(sorted_hands, key=lambda h: h.val)
        sorted_hands = sorted(sorted_hands, key=lambda h: h.type_j)
        result = 0
        for i, hand in enumerate(sorted_hands):
            result += (i + 1) * hand.bid
        return result


def main():
    exercise = Advent7('input2')
    print('Test Solution for part 1: ' + str(exercise.part_one()))
    print('Test Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent7('input')
    print('Actual Solution for part 1: ' + str(exercise.part_one()))
    print('Actual Solution for part 2: ' + str(exercise.part_two()))
    exercise = Advent7('input3')
    print('Debug Solution for part 1: ' + str(exercise.part_one()))
    print('Debug Solution for part 2: ' + str(exercise.part_two()))


if __name__ == '__main__':
    main()
