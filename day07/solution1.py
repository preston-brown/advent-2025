from collections import deque


def run(lines):
    start_position, splitters, last_row = parse_input(lines)
    to_process, splitters_hit, already_processed = deque([start_position]), set(), set()
    while to_process:
        ray = to_process.pop()
        south = (ray[0] + 1, ray[1])
        if south[0] > last_row:
            continue
        if south not in already_processed:
            already_processed.add(south)
            if south in splitters:
                splitters_hit.add(south)
                southeast, southwest = (south[0], south[1] + 1), (south[0], south[1] - 1)
                to_process.extend([southeast, southwest])
            else:
                to_process.append(south)
    return len(splitters_hit)


def parse_input(lines):
    start_position, splitters, last_row = None, set(), 0
    for row, line in enumerate(lines):
        last_row = row
        for col, char in enumerate(list(line)):
            if char == '^':
                splitters.add((row, col))
            elif char == 'S':
                start_position = (row, col)
    return start_position, splitters, last_row