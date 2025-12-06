import math

class Columns:

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
    columns = Columns()
    for line in lines:
        columns.add_row(line.split())
    for col in range(len(columns)):
        column = columns[col]
        operator = column[-1]
        numbers = [int(x) for x in column[:-1]]
        temp = sum(numbers) if operator == '+' else math.prod(numbers)
        result += temp
    return result
