def run(lines):
    result = 0
    for line in lines:
        joltage = calculate_maximum_joltage(line)
        result += joltage
    return result


def calculate_maximum_joltage(line):
    """
    Find the maximum twelve-digit number you can create from `line` by dropping characters.
    Calculate stop_index so that we retain enough future candidates to finish padding out the 12-digit number.
    """
    battery_size = 12
    digits = [int(x) for x in list(line)]
    result, start_index = 0, 0

    for i in range(battery_size):
        stop_index = len(digits) - battery_size + i + 1 
        candidates = digits[start_index:stop_index]
        digit, index = get_max_digit(candidates)
        start_index = start_index + index + 1
        result = result * 10 + digit
    return result


def get_max_digit(digits: list[int]):
    """
    Find the max value in the provided list. 
    Return this value and its location/index.
    """

    result = (None, None)
    for idx, d in enumerate(digits):
        if result[0] is None or result[0] < d:
            result = (d, idx)
    return result

