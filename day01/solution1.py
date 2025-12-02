import re

rotation_pattern = re.compile(r"""
    ([LR])          # direction, left or right
    ([1-9][0-9]*)   # number of clicks
""", re.VERBOSE)


def run(lines):
    result = 0
    position = 50
    for line in lines:
        match = rotation_pattern.fullmatch(line)
        direction, clicks = match.group(1), int(match.group(2))
        position = (position + ((1 if direction == 'R' else -1) * clicks)) % 100
        if position == 0:
            result += 1
    return result