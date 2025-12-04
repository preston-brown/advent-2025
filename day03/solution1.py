def run(lines):
    result = 0
    for line in lines:
        joltage = calculate_maximum_joltage(line)
        result += joltage
    return result


def calculate_maximum_joltage(line):
    """
    Find the maximum two-digit number you can create from `line` by dropping all but two characters.
    """
    digits = [int(x) for x in list(line)]
    first_digit = max(digits[:-1])
    index = digits.index(first_digit) + 1
    second_digit = max(digits[index:])
    return first_digit * 10 + second_digit
