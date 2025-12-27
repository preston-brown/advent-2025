from __future__ import annotations

from collections import defaultdict
from enum import Enum


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Point:

    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self._row == other._row and self._col == other._col

    def __hash__(self):
        return hash((self._row, self._col))

    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        if self._row != other._row:
            return self._row < other._row
        return self._col < other._col

    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return Point(self._row + other._row, self._col + other._col)

    def __repr__(self):
        return f"Point({self._row}, {self._col})"

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col


class Direction(Enum):
    NORTH = Point(-1, 0)
    SOUTH = Point(1, 0)
    EAST = Point(0, 1)
    WEST = Point(0, -1)


class Edge:

    def __init__(self, p1: Point, p2: Point):
        assert p1 != p2
        assert p1.row == p2.row or p1.col == p2.col
        if p1.row == p2.row:
            self._orientation = Orientation.HORIZONTAL
        else:
            self._orientation = Orientation.VERTICAL
        self._p1 = min(p1, p2)
        self._p2 = max(p1, p2)

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self._p1 == other._p1 and self._p2 == other._p2

    def __hash__(self):
        return hash((self._p1, self._p2))

    def __lt__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self._p1 < other._p1

    def __repr__(self):
        return f"Edge({self._p1}, {self._p2})"

    @property
    def orientation(self):
        return self._orientation

    @property
    def row(self):
        assert self._orientation == Orientation.HORIZONTAL
        return self._p1.row

    @property
    def col(self):
        assert self._orientation == Orientation.VERTICAL
        return self._p1.col

    def contains_point(self, point: Point):
        if self._orientation == Orientation.HORIZONTAL:
            return (
                self._p1.row == point.row and self._p1.col <= point.col <= self._p2.col
            )
        else:
            return (
                self._p1.col == point.col and self._p1.row <= point.row <= self._p2.row
            )

    def get_point(self, direction: Direction):
        if direction in (Direction.EAST, Direction.WEST):
            assert self._orientation == Orientation.HORIZONTAL
            return self._p1 if direction == Direction.WEST else self._p2
        if direction in (Direction.NORTH, Direction.SOUTH):
            assert self._orientation == Orientation.VERTICAL
            return self._p1 if direction == Direction.NORTH else self._p2

    def iterate_points(self):
        if self._orientation == Orientation.HORIZONTAL:
            increment = Direction.EAST.value
        else:
            increment = Direction.SOUTH.value
        node = self._p1
        while node <= self._p2:
            yield node
            node += increment


class Shape:

    def __init__(self, edges: list[Edge]):
        self._edges = list(edges)

    def __len__(self):
        return len(self._edges)

    def iterate_edges(self):
        for edge in self._edges:
            yield edge

    def contains_point(self, point: Point):
        cross_count = 0
        for edge in self._edges:
            if edge.contains_point(point):
                return True
            if edge.orientation == Orientation.HORIZONTAL and edge.row < point.row:
                west = edge.get_point(Direction.WEST)
                east = edge.get_point(Direction.EAST)
                if west.col <= point.col < east.col:
                    cross_count += 1
        return cross_count % 2 == 1


class Rectangle:

    def __init__(self, p1: Point, p2: Point):
        assert p1 != p2
        p3 = Point(p1.row, p2.col)
        p4 = Point(p2.row, p1.col)
        self._p1, _, _, self._p2 = list(sorted([p1, p2, p3, p4]))

    def __eq__(self, other):
        if not isinstance(other, Rectangle):
            return NotImplemented
        return (self._p1, self._p2) == (other._p1, other._p2)

    def __hash__(self):
        return hash((self._p1, self._p2))

    def __repr__(self):
        return f"Rectangle({self._p1}, {self._p2})"

    @property
    def area(self):
        width = self._p2.col - self._p1.col + 1
        height = self._p2.row - self._p1.row + 1
        return width * height

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    def contains_point(self, point: Point):
        return (
            self._p1.row <= point.row <= self._p2.row
            and self._p1.col <= point.col <= self._p2.col
        )


def run(lines):
    points = get_points(lines)
    print(f"Points: {len(points)}")
    edges = get_edges(points)
    print(f"Edges: {len(edges)}")
    shape = Shape(edges)
    print(f"Shape: {len(shape)}")
    rectangles = get_rectangles(points)
    print(f"Rectangles: {len(rectangles)}")
    outside_points_by_row, outside_points_by_col = defaultdict(set), defaultdict(set)
    outside_point_count = 0
    for p in get_points_outside_shape(shape):
        outside_point_count += 1
        outside_points_by_row[p.row].add(p)
        outside_points_by_col[p.col].add(p)
    print(f"Outside points: {outside_point_count}")
    max_area = 0
    for rectangle in sorted(rectangles, key=lambda x: x.area, reverse=True):
        if max_area < rectangle.area and check_rectangle(
            rectangle, outside_points_by_row, outside_points_by_col
        ):
            max_area = rectangle.area
            print(f"{rectangle} | {rectangle.area:,}")
    return max_area


def get_points(lines) -> list[Point]:
    result = []
    for line in lines:
        col, row = [int(x) for x in line.split(",")]
        result.append(Point(row, col))
    return result


def get_edges(points: list[Point]) -> list[Edge]:
    result = []
    for p1, p2 in zip(points, points[1:] + points[:1]):
        result.append(Edge(p1, p2))
    return result


def get_rectangles(points: list[Point]) -> list[Rectangle]:
    result = []
    points = list(sorted(points))
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            result.append(Rectangle(p1, p2))
    return result


def get_points_outside_shape(shape: Shape):
    for edge in shape.iterate_edges():
        for point in get_points_outside_edge(edge, shape):
            yield point


def get_points_outside_edge(edge: Edge, shape: Shape):
    if edge.orientation == Orientation.HORIZONTAL:
        directions = (Direction.NORTH.value, Direction.SOUTH.value)
    else:
        directions = (Direction.EAST.value, Direction.WEST.value)
    for point in edge.iterate_points():
        for direction in directions:
            candidate = point + direction
            if not shape.contains_point(candidate):
                yield candidate


def check_rectangle(rectangle: Rectangle, outside_points_by_row, outside_points_by_col):
    for row in range(rectangle.p1.row, rectangle.p2.row + 1):
        for point in outside_points_by_row[row]:
            if rectangle.contains_point(point):
                return False
    for col in range(rectangle.p1.col, rectangle.p2.col + 1):
        for point in outside_points_by_col[col]:
            if rectangle.contains_point(point):
                return False
    return True
