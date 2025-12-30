from __future__ import annotations

import functools
import itertools
import re


class Node:

    def __init__(self, id):
        self._id = id
        self._parents = []
        self._children = []

    @property
    def id(self):
        return self._id

    def add_child(self, child: Node):
        self._children.append(child)
        child._parents.append(self)

    @functools.cache
    def count_paths(self):
        if self._id == 'you':
            return 1
        elif self._parents:
            return sum(p.count_paths() for p in self._parents)
        else:
            return 0


input_pattern = re.compile(r"""
    ([a-z]{3})    # device name
    :             # colon
    \s            # space
    (.*)          # outputs
""", re.VERBOSE)


def run(lines):
    final_node = build_nodes(lines)
    return final_node.count_paths()

def build_nodes(lines):
    nodes = {'out': Node('out')}
    for line in lines:
        match = input_pattern.fullmatch(line)
        device = match.group(1)
        nodes[device] = Node(device)
    for line in lines:
        match = input_pattern.fullmatch(line)
        device = match.group(1)
        outputs = match.group(2).split()
        for output in outputs:
            nodes[device].add_child(nodes[output])
    return nodes['out']


def process_line(line):
    match = input_pattern.fullmatch(line)
    device = match.group(1)
    outputs = match.group(2).split()
    print(device, outputs)
