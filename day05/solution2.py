class Range:

    """
    min and max on native python ranges are too slow so created this class instead.
    """

    def __init__(self, start, stop):
        self._start = start
        self._stop = stop
    
    @property
    def start(self):
        return self._start
    
    @property
    def stop(self):
        return self._stop
    
    def overlaps(self, other):
        if self._start > other._start:
            return other.overlaps(self)
        return self._stop + 1 >= other._start
    
    def merge(self, other):
        start = min(self._start, other._start)
        stop = max(self._stop, other._stop)
        return Range(start, stop)


def run(lines):
    ranges = parse_input(lines)
    ranges = consolidate_ranges(ranges)
    result = 0
    for r in ranges:
        result += (r.stop - r.start + 1)
    return result


def parse_input(lines):
    result = []
    for line in lines:
        if line == '':
            break
        start, end = line.split('-')
        start, end = int(start), int(end)
        result.append(Range(start, end))
    return result


def consolidate_ranges(ranges):
    """
    Merge overlapping ranges until no overlapping ranges remain.
    """
    any_changes = True
    while any_changes:
        any_changes = False
        r1_idx, r2_idx = find_overlap(ranges)
        if r1_idx is not None:
            r1, r2 = ranges[r1_idx], ranges[r2_idx]
            ranges = [r for idx, r in enumerate(ranges) if idx not in (r1_idx, r2_idx)]
            ranges.append(r1.merge(r2))
            any_changes = True
    return ranges


def find_overlap(ranges):
    """
    Find the indexes of any two overlapping ranges. 
    """
    for i in range(len(ranges)):
        for j in range(i + 1, len(ranges)):
            if ranges[i].overlaps(ranges[j]):
                return i, j
    return None, None
