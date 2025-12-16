import heapq
import uuid


def run(lines):
    junction_boxes = get_junction_boxes(lines)
    jb1, jb2 = get_last_connection(junction_boxes)
    return jb1[0] * jb2[0]


def get_last_connection(junction_boxes):
    """
    Connect circuits until there is just one single circuit. 
    Return the pair of junction boxes that triggered this last connection.
    """
    circuits = {str(uuid.uuid4()): set([jb]) for jb in junction_boxes}
    iterator = get_closest_pair_iterator(junction_boxes)
    while len(circuits) > 1:
        jb1, jb2 = next(iterator)
        matching_circuits = list({k for k, v in circuits.items() if jb1 in v or jb2 in v})
        if len(matching_circuits) == 1:
            # No action needed, the junction boxes are on the same circuit
            pass
        elif len(matching_circuits) == 2:
            # Combine the two circuits together
            id1, id2 = matching_circuits[0], matching_circuits[1]
            c1, c2 = circuits[id1], circuits[id2]
            del circuits[id1]
            del circuits[id2]
            id3, c3 = str(uuid.uuid4()), c1 | c2
            circuits[id3] = c3
            if len(circuits) == 1:
                return jb1, jb2
        else:
            raise Exception(f'Unexpected number of circuits: {len(matching_circuits)}')


def get_closest_pair_iterator(junction_boxes):
    """
    Iterate over pairs of junction boxes in order by increasing distance between them.
    """
    heap = []
    for jb1 in junction_boxes:
        for jb2 in junction_boxes:
            if jb1 < jb2:
                distance_squared = sum([(x - y) ** 2 for x, y in zip(jb1, jb2)])
                heapq.heappush(heap, (distance_squared, jb1, jb2))
    while heap:
        _, jb1, jb2 = heapq.heappop(heap)
        yield jb1, jb2


def get_junction_boxes(lines):
    """
    Convert the input into a list of junction boxes,
    which are just 3-tuples containing an x, y, and z coordinate.
    """
    result = []
    for line in lines:
        junction_box = tuple([int(x) for x in line.split(",")])
        result.append(junction_box)
    return result
