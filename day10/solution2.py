from __future__ import annotations

import collections
import itertools
import re


class DijkstraNode:

    def __init__(self, value):
        self._value = value
        self._neighbors: list[DijkstraNode] = []
        self.distance = None
        self.visited = False

    @property
    def value(self):
        return self._value

    def add_neighbor(self, neighbor: DijkstraNode):
        self._neighbors.append(neighbor)

    def get_neighbors(self):
        return list(self._neighbors)


def run(lines):
    result = 0
    for line in lines:
        process_line(line)
        return
    return result


def process_line(line):
    buttons = extract_buttons(line)
    desired_joltage = extract_joltage(line)
    nodes = assemble_graph(buttons, desired_joltage)
    print(len(nodes))


def extract_buttons(line):
    match = re.findall(r"\(([0-9,]+)\)", line)
    result = []
    for item in match:
        result.append(tuple([int(x) for x in item.split(",")]))
    return result


def extract_joltage(line):
    match = re.search(r"\{([0-9,]+)\}", line)
    return tuple(int(x) for x in match.group(1).split(","))


def assemble_graph(buttons, desired_joltage):
    node_dict = {}
    joltage_width = len(desired_joltage)
    initial_counter = [0 for _ in range(joltage_width)]
    initial_node = DijkstraNode(initial_counter)
    work_queue = collections.deque([initial_node])
    while work_queue:
        node = work_queue.popleft()
        counter = node.value
        neighbor_counters = [apply_button(counter, button) for button in buttons]
        for neighbor_counter in neighbor_counters:
            if compare_joltage_counter(neighbor_counter, desired_joltage):
                if neighbor_counter not in node_dict:
                    neighbor_node = DijkstraNode(neighbor_counter)
                    node_dict[neighbor_counter] = neighbor_node
                    work_queue.append(neighbor_node)
                    print(neighbor_counter)
                node.add_neighbor(node_dict[neighbor_counter])
    return node_dict.values()


def compare_joltage_counter(lo, hi):
    for i in range(len(lo)):
        if lo[i] > hi[i]:
            return False
    return True


def apply_button(state, button):
    return tuple([v + 1 if i in button else v for i, v in enumerate(state)])


def get_min_unvisited_node(nodes: list[DijkstraNode]):
    candidates = [n for n in nodes if not n.visited and n.distance is not None]
    candidates.sort(key=lambda x: x.distance)
    return candidates[0]
