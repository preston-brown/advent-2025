from itertools import count


def run(lines):
    ranges, max_value = get_ranges(lines)
    invalid_ids = set()
    for repeat in count(2):
        if get_candidate(1, repeat) > max_value:
            break
        for value in count(1):
            candidate = get_candidate(value, repeat)
            if candidate > max_value:
                break
            if any(candidate in r for r in ranges):
                invalid_ids.add(candidate)
    return sum(invalid_ids)


def get_ranges(lines):
    ranges, max_value = [], 0
    for r in lines[0].split(','):
        a, b = r.split('-')
        a, b = int(a), int(b)
        ranges.append(range(a, b + 1))
        max_value = max(max_value, b)
    return ranges, max_value


def get_candidate(value, repeat):
    return int(str(value) * repeat)
