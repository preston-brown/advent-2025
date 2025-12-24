from __future__ import annotations

from collections import defaultdict
from enum import Enum
import functools
import heapq


class Orientation(Enum):
    HORIZONTAL = 1
    VERTICAL = 2


class Side(Enum):
    LEFT = 1
    RIGHT = 2


class Point:

    def __init__(self, row: int, col: int):
        self._row = row
        self._col = col

    def __eq__(self, other):
        return self._row == other._row and self._col == other._col

    def __hash__(self):
        return hash((self._row, self._col))

    def __lt__(self, other):
        if self._row != other._row:
            return self._row < other._row
        return self._col < other._col

    def __le__(self, other):
        return self < other or self == other

    def __add__(self, other):
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

    def __init__(self, start: Point, end: Point):
        assert start != end
        assert start.row == end.row or start.col == end.col
        if start.row == end.row:
            self._orientation = Orientation.HORIZONTAL
        elif start.col == end.col:
            self._orientation = Orientation.VERTICAL
        self._start = start
        self._end = end

    def __str__(self):
        return f"{self._start} {self.direction} to {self._end}"

    @property
    def orientation(self):
        return self._orientation

    @property
    def row(self):
        assert self._orientation == Orientation.HORIZONTAL
        return self._start.row

    @property
    def col(self):
        assert self._orientation == Orientation.VERTICAL
        return self._start.row

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def direction(self):
        if self._orientation == Orientation.HORIZONTAL:
            return Direction.EAST if self._start.col < self._end.col else Direction.WEST
        else:
            return (
                Direction.SOUTH if self._start.row < self._end.row else Direction.NORTH
            )

    def contains_point(self, p: Point):
        if self._orientation == Orientation.HORIZONTAL:
            min_col, max_col = min(self._start.col, self._end.col), max(
                self._start.col, self._end.col
            )
            return self._start.row == p.row and min_col <= p.col <= max_col
        else:
            min_row, max_row = min(self._start.row, self._end.row), max(
                self._start.row, self._end.row
            )
            return self._start.col == p.col and min_row <= p.row <= max_row

    def iterate_points(self):
        point = self._start
        increasing = self.direction in (Direction.EAST, Direction.SOUTH)
        while (increasing and point <= self._end) or (
            not increasing and point >= self._end
        ):
            yield point
            point = point + self.direction.value


class Shape:

    def __init__(self):
        self._edges: list[Edge] = []

    def __len__(self):
        return len(self._edges)

    def add_edge(self, edge: Edge):
        self._edges.append(edge)

    def get_outside(self):
        for edge in self._edges:
            if edge.direction == Direction.EAST:
                edges_north = [
                    e
                    for e in self._edges
                    if e.orientation == Orientation.HORIZONTAL and e.row < edge.row
                ]
                if not edges_north:
                    return Side.LEFT
                edges_south = [
                    e
                    for e in self._edges
                    if e.orientation == Orientation.HORIZONTAL and e.row > edge.row
                ]
                if not edges_south:
                    return Side.RIGHT
        raise Exception("Bad algorithm")

    def iterate_edges(self):
        for i, edge in enumerate(self._edges):
            prior = self._edges[i - 1]
            next = self._edges[(i + 1) % len(self._edges)]
            yield edge, prior, next


class Rectangle:

    def __init__(self, p1: Point, p2: Point):
        assert p1 != p2
        p3 = Point(p1.row, p2.col)
        p4 = Point(p2.row, p1.col)
        self._p1, _, _, self._p2 = list(sorted([p1, p2, p3, p4]))

    def __eq__(self, other):
        return (self._p1, self._p2) == (other._p1, other._p2)

    def __hash__(self):
        return hash((self._p1, self._p2))

    def __lt__(self, other):
        return self.area < other.area

    def __repr__(self):
        return f"Rectangle({self._p1}, {self._p2})"

    @property
    def p1(self):
        return self._p1

    @property
    def p2(self):
        return self._p2

    @property
    def area(self):
        width = self._p2.col - self._p1.col + 1
        height = self._p2.row - self._p1.row + 1
        return width * height

    def contains(self, point: Point):
        return (
            self._p1.row <= point.row <= self._p2.row
            and self._p1.col <= point.col <= self._p2.col
        )


def run(lines):
    points = get_points(lines)
    print(f"Points: {len(points)}")
    rectangles = set(get_rectangles(points))
    print(f"Rectangles: {len(rectangles)}")
    shape = get_shape(points)
    print(f"Edges: {len(shape)}")
    for p in get_points_outside_shape(shape):
        remove = set()
        for rectangle in rectangles:
            if rectangle.contains(p):
                remove.add(rectangle)
        if remove:
            rectangles -= remove
            print(f'{p} removed {len(remove)} rectangles leaving {len(rectangles)} rectangles')
    return max([r.area for r in rectangles])


def get_points_outside_shape(shape: Shape):
    outside = shape.get_outside()
    last_yield = None
    for edge, prev, next in shape.iterate_edges():
        outside_direction = turn_map[(edge.direction, outside)]
        points = [p + outside_direction.value for p in edge.iterate_points()]
        for point in points:
            if (
                not prev.contains_point(point)
                and not next.contains_point(point)
                and (last_yield is None or last_yield != point)
            ):
                last_yield = point
                yield point


turn_map = {
    (Direction.NORTH, Side.LEFT): Direction.WEST,
    (Direction.NORTH, Side.RIGHT): Direction.EAST,
    (Direction.SOUTH, Side.LEFT): Direction.EAST,
    (Direction.SOUTH, Side.RIGHT): Direction.WEST,
    (Direction.EAST, Side.LEFT): Direction.NORTH,
    (Direction.EAST, Side.RIGHT): Direction.SOUTH,
    (Direction.WEST, Side.LEFT): Direction.SOUTH,
    (Direction.WEST, Side.RIGHT): Direction.NORTH,
}


def get_points(lines) -> list[Point]:
    result = []
    for line in lines:
        col, row = [int(x) for x in line.split(",")]
        result.append(Point(row, col))
    return result


def get_shape(points: list[Point]):
    result = Shape()
    for p1, p2 in zip(points, points[1:] + points[:1]):
        result.add_edge(Edge(p1, p2))
    return result


def get_rectangles(points: list[Point]):
    result = []
    points = list(sorted(points))
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            result.append(Rectangle(p1, p2))
    return result


def categorize_rectangles(rectangles: list[Rectangle]):
    by_rows, by_cols = defaultdict(set), defaultdict(set)
    for rectangle in rectangles:
        by_rows[rectangle.p1.row].add(rectangle)
        by_rows[rectangle.p2.row].add(rectangle)
        by_cols[rectangle.p1.col].add(rectangle)
        by_cols[rectangle.p2.col].add(rectangle)
    return by_rows, by_cols
