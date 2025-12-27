from __future__ import annotations

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
        result += process_line(line)
    return result


def process_line(line):
    end_state = get_end_state(line)
    indicator_light_count = len(end_state)
    start_state = tuple([False for _ in range(indicator_light_count)])
    buttons = get_buttons(line)
    nodes = assemble_graph(indicator_light_count, buttons)
    start_node = [n for n in nodes if n.value == start_state][0]
    start_node.distance = 0
    end_node = [n for n in nodes if n.value == end_state][0]
    while True:
        node = get_min_unvisited_node(nodes)
        if node == end_node:
            return node.distance
        for neighbor in node.get_neighbors():
            if neighbor.distance is None or neighbor.distance > node.distance + 1:
                neighbor.distance = node.distance + 1
        node.visited = True


def get_end_state(line):
    match = re.search(r"\[([\.#]*)\]", line)
    return tuple([x == "#" for x in list(match.group(1))])


def get_buttons(line):
    match = re.findall(r"\(([0-9,]+)\)", line)
    result = []
    for item in match:
        result.append(tuple([int(x) for x in item.split(",")]))
    return result


def assemble_graph(size, buttons):
    state_dict = {
        combo: DijkstraNode(combo)
        for combo in itertools.product([True, False], repeat=size)
    }
    for state in state_dict.values():
        for button in buttons:
            new_state = state_dict[apply_button(state.value, button)]
            state.add_neighbor(new_state)
    return state_dict.values()


def apply_button(state, button):
    return tuple([not v if i in button else v for i, v in enumerate(state)])


def get_min_unvisited_node(nodes: list[DijkstraNode]):
    candidates = [n for n in nodes if not n.visited and n.distance is not None]
    candidates.sort(key=lambda x: x.distance)
    return candidates[0]
