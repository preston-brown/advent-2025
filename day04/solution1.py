from collections import defaultdict


def run(lines):
    result = 0
    locations = get_paper_roll_locations(lines)
    adjacent_count = count_adjacent_rolls(locations)
    for location in locations:
        if adjacent_count[location] < 4:
            result += 1
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
        neighbors = get_neighbors(*location)
        for neighbor in neighbors:
            result[neighbor] += 1
    return result


def get_neighbors(row, col):
    result = set()
    for i in range(-1, 2):
        for j in range(-1, 2):
            result.add((row + i, col + j))
    result.remove((row, col))
    return result
