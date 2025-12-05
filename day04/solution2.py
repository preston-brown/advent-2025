from collections import defaultdict


def run(lines):
    result = 0
    locations = get_paper_roll_locations(lines)
    adjacent_count = count_adjacent_rolls(locations)
    any_changes = True
    while any_changes:
        any_changes, remaining_locations = False, set()
        for location in locations:
            if adjacent_count[location] < 4:
                result += 1
                any_changes = True
                decrement_neighbors(location, adjacent_count)
            else:
                remaining_locations.add(location)
        locations = remaining_locations
    return result


def get_paper_roll_locations(lines):
    result = set()
    for row, line in enumerate(lines):
        for col, item in enumerate(list(line)):
            if item == '@':
                result.add((row, col))
    return result


def count_adjacent_rolls(locations):
    result = defaultdict(int)
    for location in locations:
        for neighbor in get_neighbors(*location):
            result[neighbor] += 1
    return result


def get_neighbors(row, col):
    result = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            result.add((row + i, col + j))
    result.remove((row, col))
    return result


def decrement_neighbors(location, totals):
    for neighbor in get_neighbors(*location):
        totals[neighbor] -= 1
