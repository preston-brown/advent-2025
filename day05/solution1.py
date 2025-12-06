from collections import defaultdict


def run(lines):
    result = 0
    ranges, ingredients = parse_input(lines)
    for i in ingredients:
        if any(i in r for r in ranges):
            result += 1
    return result


def parse_input(lines):
    mode, ranges, ingredients = 'ranges', [], []
    for line in lines:
        if line == '':
            mode = 'ingredients'
        else:
            if mode == 'ranges':
                start, end = line.split('-')
                start, end = int(start), int(end)
                ranges.append(range(start, end + 1))
            else:
                ingredients.append(int(line))
    return ranges, ingredients                
