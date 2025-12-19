def run(lines):
    points = get_points(lines)
    biggest_area = None
    for i, p1 in enumerate(points):
        for p2 in points[i + 1 :]:
            area = calculate_area(p1, p2)
            if biggest_area is None or biggest_area < area:
                biggest_area = area
    return biggest_area


def get_points(lines):
    result = []
    for line in lines:
        result.append(tuple([int(x) for x in line.split(",")]))
    result.sort()
    return result


def calculate_area(p1, p2):
    width = abs(p1[0] - p2[0]) + 1
    height = abs(p1[1] - p2[1]) + 1
    return width * height
