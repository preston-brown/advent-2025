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

    def __lt__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        if self._row != other._row:
            return self._row < other._row
        return self._col < other._col

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


class LineSegment:

    def __init__(self, p1: Point, p2: Point):
        assert p1.row == p2.row or p1.col == p2.col
        if p1.row == p2.row:
            self._orientation = Orientation.HORIZONTAL
        else:
            self._orientation = Orientation.VERTICAL
        self._start = min(p1, p2)
        self._end = max(p1, p2)

    def __repr__(self):
        return f"LineSegment({self._start}, {self._end})"

    @property
    def orientation(self):
        return self._orientation

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    def contains_point(self, point: Point):
        if self._orientation == Orientation.HORIZONTAL:
            return self._start.row == point.row and self._start.col <= point.col <= self._end.col
        else:
            return self._start.col == point.col and self._start.row <= point.row <= self._end.row

    def intersects(self, other: LineSegment):
        """
        Determine if this line segment intersects another. 
        Use different approaches if they have the same orientation or not. 
        """
        if self._orientation == other._orientation:
            if self._orientation == Orientation.HORIZONTAL:
                return self._start.row == other._start.row and self._start.col <= other._end.col and self._end.col >= other._start.col
            else:
                return self._rotate().intersects(other._rotate())
        elif self._orientation == Orientation.HORIZONTAL:
            return other._start.row <= self._start.row <= other._end.row and self._start.col <= other._start.col <= self._end.col
        else:
            return other.intersects(self)

    def _rotate(self):
        """
        Rotate a line segment 45 degrees.
        """
        return LineSegment(Point(self._start.col, self._start.row), Point(self._end.col, self._end.row))


class Polygon:

    def __init__(self, edges: list[LineSegment]):
        self._edges = list(edges)

    def iterate_edges(self):
        for edge in self._edges:
            yield edge

    def contains_point(self, point: Point):
        """
        Determine if the provided point is inside this polygon.
        If you find any edge that contains this point, then the point is inside the polygon. 
        If not, count how many horizontal edges a ray travelling north from the point toward infinity crosses. 
        If odd, the point is inside. 
        Note the less than in "point.col < edge.end.col". This is intentional. Hitting the right-most point of an edge doesn't count as crossing it.
        """
        cross_count = 0
        for edge in self._edges:
            if edge.contains_point(point):
                return True
            if edge.orientation == Orientation.HORIZONTAL and edge.start.row < point.row:
                if edge.start.col <= point.col < edge.end.col:
                    cross_count += 1
        return cross_count % 2 == 1


class Rectangle:

    def __init__(self, p1: Point, p2: Point):
        self._northwest = Point(min(p1.row, p2.row), min(p1.col, p2.col))
        self._southeast = Point(max(p1.row, p2.row), max(p1.col, p2.col))

    def __repr__(self):
        return f"Rectangle({self._northwest}, {self._southeast})"

    @property
    def area(self):
        width = self._southeast.col - self._northwest.col + 1
        height = self._southeast.row - self._northwest.row + 1
        return width * height

    @property
    def northwest(self):
        return self._northwest

    @property
    def southeast(self):
        return self._southeast

    def contains_point(self, point: Point) -> bool:
        """
        Determine if the provided point is inside this rectangle.
        """
        return (
            self._northwest.row <= point.row <= self._southeast.row
            and self._northwest.col <= point.col <= self._southeast.col
        )

    def iterate_edges(self):
        """
        Yield the four line segments that define this rectangle.
        """
        northeast = Point(self._northwest.row, self._southeast.col)
        southwest = Point(self._southeast.row, self._northwest.col)
        yield LineSegment(self._northwest, northeast)
        yield LineSegment(self._northwest, southwest)
        yield LineSegment(self._southeast, northeast)
        yield LineSegment(self._southeast, southwest)


def run(lines):
    points = get_points(lines)
    print(f"Points: {len(points)}")
    line_segments = build_line_segments(points)
    print(f"Line segments: {len(line_segments)}")
    polygon = Polygon(line_segments)
    boundaries = build_boundaries(polygon)
    print(f'Boundaries: {len(boundaries)}')
    rectangles = build_rectangles(points)
    print(f"Rectangles: {len(rectangles)}")
    for rectangle in sorted(rectangles, key=lambda r: r.area, reverse=True):
        if is_inside(rectangle, boundaries, polygon):
            return rectangle.area


def build_line_segments(points: list[Point]) -> list[LineSegment]:
    """
    Generate line segments for each consecutive pair of points in the input.
    """
    result = []
    for p1, p2 in zip(points, points[1:] + points[:1]):
        result.append(LineSegment(p1, p2))
    return result


def get_points(lines) -> list[Point]:
    """
    Extract points from the provided input.
    """
    result = []
    for line in lines:
        col, row = [int(x) for x in line.split(",")]
        result.append(Point(row, col))
    return result


def build_rectangles(points: list[Point]) -> list[Rectangle]:
    """
    Generate a rectangle for each pair of points in the provided list. 
    """
    result = []
    points = list(sorted(points))
    for i, p1 in enumerate(points):
        for p2 in points[i + 1:]:
            result.append(Rectangle(p1, p2))
    return result


def build_boundaries(polygon: Polygon) -> list[LineSegment]:
    """
    Build a list of line segments that "bound" the provided polygon.
    These are the line segments that contain all the points that are outside the polygon
    and also adjacent to the polygon's edges.
    """
    result = []
    for edge in polygon.iterate_edges():
        if edge.orientation == Orientation.HORIZONTAL:
            boundary_points = get_boundary_points(edge, Direction.NORTH, polygon)
            if not boundary_points:
                boundary_points = get_boundary_points(edge, Direction.SOUTH, polygon)
        else:
            boundary_points = get_boundary_points(edge, Direction.EAST, polygon)
            if not boundary_points:
                boundary_points = get_boundary_points(edge, Direction.WEST, polygon)
        p1, p2 = min(boundary_points), max(boundary_points)
        result.append(LineSegment(p1, p2))
    return result


def get_boundary_points(edge: LineSegment, direction: Direction, polygon: Polygon):
    """
    Return the min and max boundary points for the provided edge in the specified direction. 
    If the provided direction is _inside_ the provided polygon, then the method will return an empty list.

    We only need to check four point here: start, start + 1, end, end - 1. Consider this shape:

    X      X
    X      X
    XAAAAAAX  
    XXXXXXXX
    BBBBBBBB

    If the A segment is inside, then the boundary points run from start + 1 to end - 1.
    If the B segment is inside, then the boundary points run from start to end.
    """
    if edge.orientation == Orientation.HORIZONTAL:
        increasing, decreasing = Direction.EAST.value, Direction.WEST.value
    else:
        increasing, decreasing = Direction.SOUTH.value, Direction.NORTH.value
    edge_points = [edge.start, edge.start + increasing, edge.end + decreasing, edge.end]
    candidates = [p + direction.value for p in edge_points]
    candidates = [p for p in candidates if not polygon.contains_point(p)]
    return [min(candidates), max(candidates)] if candidates else []


def is_inside(rectangle: Rectangle, boundaries: list[LineSegment], polygon: Polygon):
    """
    Determine if the provided rectangle is fully within the provided boundaries.
    A lot of rectangles have ALL their internal points outside the polygon, so picking one internal point and testing it 
    can allow us to skip the slower check against all boundaries.
    """
    point = rectangle.northwest + Direction.EAST.value + Direction.SOUTH.value
    if not polygon.contains_point(point):
        return False
    for boundary in boundaries:
        for edge in rectangle.iterate_edges():
            if edge.intersects(boundary):
                return False
    return True
