from operator import itemgetter
import math

def load_coordinate_pairs(file_name):
    with open(file_name) as file:
        return [tuple(map(int, i.split(' '))) for i in file]


def y_sort(points):
    return sorted(points, key=itemgetter(1))


def distance(pi, pj):
    """
    :param tuple pi: first point, tuple of (x,y)
    :param tuple pj: second point, tuple of (x,y)
    :return float: distance between pi and pj
    """
    return math.sqrt(((pi[0] - pj[0]) ** 2) + ((pi[1] - pj[1]) ** 2))


def min_distance(points):
    """
    :param list points: list of tuples(x,y) of coordinate points
    :return float d: minimum distance between points
    :return tuple (d, pair): (float, ((x,y),(x,y))) with min distance and corresponding cooredinates
    """
    # Default minimum distance: distance between first two points
    d = distance(points[0], points[1])
    pair = points[0], points[1]

    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            if distance(points[i], points[j]) < d:
                d = distance(points[i], points[j])
                pair = points[i], points[j]

    return d, pair


def strip_min_distance(strip, d):
    """
    :param list strip: list of tuples(x,y) of y-sorted coordinate points within 2d of line
    :param tuple d: tuple(float, ((x,y),(x,y))) with current min distance and corresponding coordinates
                    from recursive closest_pair() calls
    :return tuple (min_d, pair): (float, ((x,y),(x,y))) with min distance and corresponding coordinates
    """
    # Default to current min distance and pair
    min_d = d[0]
    pair = d[1]

    # i+j specifies index that strip[i] is being compared to
    # If i+j > len(strip), then comparison index is out of range
    # strip[i] will be compared to next 7 points OR to remaining points in strip, whichever is shorter
    for i in range(len(strip)):
        for j in range(1, 8):
            if i + j < len(strip) and distance(strip[i], strip[i + j]) < min_d:
                min_d = (distance(strip[i], strip[i + j]))
                pair = strip[i], strip[i + j]
    return min_d, pair


def closest(x, y):
    """
    :param list x: list of tuples(x,y) of x-sorted coordinate points
    :param list y: list of tuples(x,y) of y-sorted coordinate points
    :return tuple min_d: (float, ((x,y),(x,y))) with final min distance and corresponding coordinates
    """
    if len(x) <= 3:
        return min_distance(x)

    middle = math.ceil(len(x) / 2)

    # Partitioned x and y lists
    xl = x[:middle]
    xr = x[middle:]
    yl = []
    yr = []

    # Creates partitioned y lists
    for point in y:
        if point in xl:
            yl.append(point)
        else:
            yr.append(point)

    dl = closest(xl, yl)
    dr = closest(xr, yr)

    min_d = min(dl, dr)

    # Define strip
    strip = []

    # Appends coordinate if within d of vertical line
    for point in y:
        if abs(point[0] - x[middle][0]) < min_d[0]:
            strip.append(point)

    min_d = min(min_d, strip_min_distance(strip, min_d))

    return min_d


if __name__ == '__main__':

    test_files = ['10points.txt', '100points.txt', '1000points.txt']
    coordinate_planes = [load_coordinate_pairs(file) for file in test_files]

    # Sort coordinate_planes by x coordinate in-place
    [plane.sort() for plane in coordinate_planes]
    y_sorted = [y_sort(plane) for plane in coordinate_planes]

    solutions = [closest(x_sorted_plane, y_sorted_plane) for x_sorted_plane, y_sorted_plane in zip(coordinate_planes, y_sorted)]
    for i in range(len(solutions)):
        print('\nThe minimum distance in {0} is:\n{1:.10f}: {2}<--->{3}\n'.format(test_files[i], solutions[i][0], 
                                                                                    solutions[i][1][0], solutions[i][1][1]))
