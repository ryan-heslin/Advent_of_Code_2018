import itertools
from collections import defaultdict
from itertools import starmap
from itertools import zip_longest
from operator import attrgetter


def manhattan(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)


def to_complex(coord):
    return map(int, coord.split(", "))


def parse(coords):
    return starmap(complex, map(to_complex, coords))


def extremum(coords, fun, getter):
    return int(getter(fun(coords, key=getter)))


def bounds(coords):
    real = attrgetter("real")
    imag = attrgetter("imag")

    return (
        extremum(coords, min, real),
        extremum(coords, max, real),
        extremum(coords, min, imag),
        extremum(coords, max, imag),
    )


def find_closest(point, centers):
    distances = {center: manhattan(point, center) for center in centers}
    nearest = min(distances.values())
    return {center for center, dist in distances.items() if dist == nearest}


def infinite_area(coords, bounds):
    xmin, xmax, ymin, ymax = bounds
    left = zip_longest((xmin,), range(ymin, ymax + 1), fillvalue=xmin)
    right = zip_longest((xmax,), range(ymin, ymax + 1), fillvalue=xmax)
    top = zip_longest(range(xmin, xmax + 1), (ymax + 0,), fillvalue=ymax + 0)
    bottom = zip_longest(range(xmin - 0, xmax + 1), (ymin - 0,), fillvalue=ymin - 0)
    border = itertools.starmap(complex, itertools.chain(top, right, bottom, left))
    result = set()

    for point in border:
        closest = find_closest(point, coords)
        if len(closest) < 2:
            result.update(closest)

    return result


def make_grid(bounds):
    xmin, xmax, ymin, ymax = bounds
    return itertools.product(range(xmin + 1, xmax), range(ymin + 1, ymax))


def find_largest(centers, infinite, bounds):
    areas = defaultdict(lambda: 0)
    grid = make_grid(bounds)
    region = 0

    for x, y in grid:
        coord = complex(x, y)
        distances = {center: manhattan(coord, center) for center in centers}
        region += sum(distances.values()) < 10000

        nearest = min(distances.values())
        closest = {center for center, dist in distances.items() if dist == nearest}
        if len(closest) < 2:
            chosen = closest.pop()
            if chosen not in infinite:
                areas[chosen] += 1

    return max(areas.values()), region


def total_distance(centers, bounds):
    grid = make_grid(bounds)

    size = 0
    for x, y in grid:
        coord = complex(x, y)
        size += sum(manhattan(coord, center) for center in centers) < 10000

    return size


with open("inputs/day6.txt") as f:
    raw_input = f.read().splitlines()

coords = set(parse(raw_input))
extrema = bounds(coords)

infinite = infinite_area(coords, extrema)
part1, part2 = find_largest(coords, infinite, extrema)
print(part1)
print(part2)
