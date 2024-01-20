import regex


def first_part(line):
    match_first = regex.match('^\\D*(\\d)', line)
    match_second = regex.match('^.*(\\d)\\D*$', line)
    current = int(match_first.group(1)) * 10 + int(match_second.group(1))
    print(current)
    return current


def second_part(line):
    matches = regex.findall('(\\d|one|two|three|four|five|six|seven|eight|nine)', line, overlapped=True)
    current = int(get_num(matches[0])) * 10 + int(get_num(matches[-1]))
    print(current)
    return current


def get_num(num) -> int:
    nums = {
        'one': 1,
        'two': 2,
        'three': 3,
        'four': 4,
        'five': 5,
        'six': 6,
        'seven': 7,
        'eight': 8,
        'nine': 9,
    }
    if num in nums:
        return nums.get(num)
    return int(num)


def main():
    result = 0
    with open('data/advent1.input.txt') as file:
        for line in file.readlines():
            result += second_part(line)
    print(result)


if __name__ == '__main__':
    main()
