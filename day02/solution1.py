from itertools import count

def run(lines):
    result = 0
    ranges, max_value = get_ranges(lines)
    for i in count(1):
        candidate = int(f'{i}{i}')
        if candidate > max_value:
            break
        if any(candidate in r for r in ranges):
            result += candidate
    return result


def get_ranges(lines):
    ranges, max_value = [], 0
    for r in lines[0].split(','):
        a, b = r.split('-')
        a, b = int(a), int(b)
        ranges.append(range(a, b + 1))
        max_value = max(max_value, b)
    return ranges, max_value
