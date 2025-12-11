from __future__ import annotations

from collections import defaultdict, deque


class Node:

    def __init__(self, row, col):
        self._row, self._col = row, col
        self._parents, self._children = [], []
        self._entry_point_count = None

    def __repr__(self):
        return f'Node({self._row}, {self._col})'

    @property
    def row(self):
        return self._row

    @property
    def col(self):
        return self._col

    @property
    def children(self):
        return list(self._children)

    @property
    def parents(self):
        return list(self._parents)

    def add_child(self, child: Node):
        child._parents.append(self)
        self._children.append(child)

    def count_entry_points(self):
        """
        The number of ways into a node is equal to the sum of the number of ways into its parents.
        Cache the result so we don't recalculate it. 
        A node with no parents has no entry points.
        """
        if self._entry_point_count is None:
            if self._parents:
                self._entry_point_count = sum(p.count_entry_points() for p in self._parents)
            else:
                self._entry_point_count = 0
        return self._entry_point_count

    def initialize_entry_points(self, value):
        """
        Here you can set a specific numbre of entry points for nodes that don't derive
        this value from their parents (i.e. the starting node).
        """
        self._entry_point_count = value


def run(lines):
    starting_node, nodes, max_row = build_graph(lines)
    starting_node.initialize_entry_points(1)
    result = sum(n.count_entry_points() for n in nodes if n.row == max_row)
    return result


def build_graph(lines):
    """
    Build a graph containing a node for every splitter in the manifold. 
    Also include a node for every point in the last row, which we'll use to 
    count how many exit points there are. 
    Link each node to its children (at most two). 
    """
    start_position, splitters, max_row, max_col = parse_input(lines)
    nodes = [Node(*splitter) for splitter in splitters] + [Node(max_row, col) for col in range(max_col + 1)]
    for node in nodes:
        left_child, right_child = find_child(nodes, node, 'left'), find_child(nodes, node, 'right')
        if left_child:
            node.add_child(left_child)
        if right_child:
            node.add_child(right_child)
    candidates = [n for n in nodes if n.row > start_position[0] and n.col == start_position[1]]
    candidates.sort(key=lambda x: x.row)
    return candidates[0], nodes, max_row


def parse_input(lines):
    """
    Deteremine the location of all the splitters. 
    """
    start_position, splitters = None, []
    max_row, max_col = 0, 0
    for row, line in enumerate(lines):
        max_row = max(max_row, row)
        for col, char in enumerate(list(line)):
            max_col = max(max_col, col)
            if char == '^':
                splitters.append((row, col))
            elif char == 'S':
                start_position = (row, col)
    return start_position, splitters, max_row, max_col


def find_child(nodes: list[Node], node: Node, direction):
    """
    For the provided node, find the closest node below it in the column
    to its left or right.
    """
    col = node.col + (1 if direction == 'right' else -1)
    nodes = [n for n in nodes if n.col == col and n.row > node.row]
    nodes.sort(key=lambda x: x.row)
    return nodes[0] if nodes else None


def count_exits(node: Node):
    """
    Look at every splitter in the tree and count how many rays they emit that exit the manifold. 
    That is to say, how many don't hit another splitter.
    """
    result, work_queue = 0, deque([node])
    while work_queue:
        node = work_queue.popleft()
        children = node.children
        work_queue.extend(children)
        if len(children) == 0:
            result += 2
        elif len(children) == 1:
            result += 1
    return result
