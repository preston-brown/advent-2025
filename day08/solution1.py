import heapq
import math
import uuid


def run(lines):
    """
    a junction box is an (x, y, z) tuple
    a circuit is a set of junction boxes
    """
    junction_boxes = get_junction_boxes(lines)
    circuits = {str(uuid.uuid4()): set([jb]) for jb in junction_boxes}
    iterator = get_distance_iterator(junction_boxes)
    for _ in range(1000):
        jb1, jb2 = next(iterator)
        matching_circuits = list({k for k, v in circuits.items() if jb1 in v or jb2 in v})
        if len(matching_circuits) == 0:
            id = str(uuid.uuid4())
            circuits[id] = set([jb1, jb2])
        elif len(matching_circuits) == 1:
            id = matching_circuits[0]
            circuits[id].update([jb1, jb2])
        elif len(matching_circuits) == 2:
            id1, id2 = matching_circuits[0], matching_circuits[1]
            c1, c2 = circuits[id1], circuits[id2]
            del circuits[id1]
            del circuits[id2]
            id3, c3 = str(uuid.uuid4()), c1 | c2
            circuits[id3] = c3
        else:
            raise Exception(f'Too many circuits found: {matching_circuits}')
    lengths = [len(v) for k, v in circuits.items()]
    largest_lengths = heapq.nlargest(3, lengths)
    return math.prod(largest_lengths)


def get_distance_iterator(junction_boxes):
    """
    Returns pairs of junction boxes in order by smallest distance between them
    """
    distances = get_distances(junction_boxes)
    heapq.heapify(distances)
    while distances:
        _, jb1, jb2 = heapq.heappop(distances)
        yield jb1, jb2


def get_distances(junction_boxes):
    result = []
    for jb1 in junction_boxes:
        for jb2 in junction_boxes:
            if jb1 < jb2:
                distance_squared = sum([(x - y) ** 2 for x, y in zip(jb1, jb2)])
                result.append((distance_squared, jb1, jb2))
    return result


def get_junction_boxes(lines):
    result = []
    for line in lines:
        junction_box = tuple([int(x) for x in line.split(",")])
        result.append(junction_box)
    return result
