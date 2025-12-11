import math


class Columns:
    """
    Accumulates rows of data and allows you to read the data back by column.
    """
    def __init__(self):
        self._rows = []

    def add_row(self, row):
        self._rows.append(row)

    def __getitem__(self, col):
        return [row[col] for row in self._rows]

    def __len__(self):
        return len(self._rows[0])


def run(lines):
    result = 0
    for problem in get_problems(lines):
        operator = problem[-1][0]
        numbers = extract_numbers(problem)
        temp = sum(numbers) if operator == '+' else math.prod(numbers)
        result += temp
    return result


def get_problems(lines):
    """
    The problems are written vertically not horizontally.
    The last line contains operators and their position indicates where to split the data vertically.
    """
    operators = lines[-1]
    column_dividers = [i for i, o in enumerate(operators) if o != ' '] + [len(lines[0]) + 1]
    for i in range(len(column_dividers) - 1):
        i1, i2 = column_dividers[i], column_dividers[i+1] - 1
        yield [line[i1:i2] for line in lines]


def extract_numbers(problem):
    """
    Read each column of data in the problem and convert it to an integer.
    """
    numbers = problem[:-1]
    columns = Columns()
    for row in numbers:
        columns.add_row(row)
    result = []
    for col in range(len(columns)):
        result.append(int(''.join(columns[col])))
    return result
