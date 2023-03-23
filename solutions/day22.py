from collections import defaultdict
from enum import Enum
from functools import cache
from math import inf
from queue import PriorityQueue

# from collections import deque


class Region(Enum):
    ROCKY = 0
    WET = 1
    NARROW = 2


REGIONS = list(Region)


class Tool(Enum):
    TORCH = 0
    GEAR = 1
    NEITHER = 2


class State:
    def __init__(self, position, tool, target):
        self.position = position
        self.tool = tool
        self.dist = manhattan(self.position, target)
        self.estimate = self.dist + (7 * (self.tool != Tool.TORCH))

    def __lt__(self, other):
        return self.estimate < other.estimate

    def __hash__(self):
        return hash((self.position, self.tool.value))

    def __eq__(self, other):
        return self.position == other.position and self.tool == other.tool

    def __repr__(self):
        return (self.position, self.tool).__repr__()


@cache
def manhattan(x, y):
    return abs(x.real - y.real) + abs(x.imag - y.imag)


def parse(lines):
    depth = int(lines[0].split(" ")[1])
    target = complex(*map(int, lines[1].split(" ")[1].split(",")))
    return depth, target


def erosion_level(index, depth):
    return (index + depth) % 20183


@cache
def neighbors(coord):
    result = set()
    if coord.real > 0:
        result.add(coord - 1)
    if coord.imag > 0:
        result.add(coord - 1j)
    result.update({coord + 1, coord + 1j})
    return frozenset(result)


# Create new row in place
def create_row(y, xmax, cave, erosion):
    coord = complex(0, y)
    first = int(erosion_level(y * 48271, depth))
    erosion[coord] = first
    cave[coord] = REGIONS[first % 3]

    for _ in range(xmax):
        # coord = complex(x, y)
        coord += 1
        value = int(erosion_level(erosion[coord - 1] * erosion[coord - 1j], depth))
        erosion[coord] = value
        cave[coord] = REGIONS[value % 3]
    return cave, erosion


def create_col(x, ymax, cave, erosion):
    coord = x
    first = int(erosion_level(x * 16807, depth))
    erosion[coord] = first
    cave[coord] = REGIONS[first % 3]
    for _ in range(ymax):
        coord += 1j
        value = int(erosion_level(erosion[coord - 1] * erosion[coord - 1j], depth))
        erosion[coord] = value
        cave[coord] = REGIONS[value % 3]
    return cave, erosion


# Risk level: sum of numeric codes for each type
def create_map(depth, target):
    origin = 0
    xrange = int(target.real - origin.real)
    yrange = int(target.imag - origin.imag)
    y_mult = 16807
    x_mult = 48271

    result = {}

    for y in range(yrange + 1):
        for x in range(xrange + 1):
            coord = complex(x, y)
            if y == 0:
                geo_index = x * y_mult
            elif x == 0:
                geo_index = y * x_mult
            elif coord == target:
                geo_index = 0
            else:
                geo_index = result[coord - 1] * result[coord - 1j]
            result[coord] = erosion_level(geo_index, depth)

    return result


def sum_values(erosion):
    result = 0
    cave = {}
    # Dict has actual enum type, not raw value
    for coord, eros in erosion.items():
        region = eros % 3
        result += region
        cave[coord] = REGIONS[region]
    return cave, result


def find_path(origin, target, cave, xmax, ymax, erosion):

    # Legal tool-region combinations
    xmax = int(xmax)
    ymax = int(ymax)
    valid = {
        Region.ROCKY: {Tool.TORCH, Tool.GEAR},
        Region.WET: {Tool.NEITHER, Tool.GEAR},
        Region.NARROW: {Tool.NEITHER, Tool.TORCH},
    }
    source = State(origin, Tool.TORCH, target)
    dist = defaultdict(lambda: inf)
    dist[source] = 0
    best = inf
    visited = set()

    goal = State(target, Tool.TORCH, target)
    queue = PriorityQueue()
    queue.put(source, block=False)

    while queue.qsize():
        current = queue.get(block=False)
        if current == goal:
            best = dist[current]
            # return best
            continue
        current_dist = dist[current]
        if current_dist + current.estimate >= best:
            continue
        this_neighbors = neighbors(current.position)
        alt = current_dist + 1

        for neighbor in this_neighbors:
            if neighbor.real > xmax:
                cave, erosion = create_col(neighbor.real, ymax, cave, erosion)
                xmax += 1
            elif neighbor.imag > ymax:
                cave, erosion = create_row(neighbor.imag, xmax, cave, erosion)
                ymax += 1

            neighbor_region = cave[neighbor]

            # Bail if attempting illegal move
            if not current.tool in valid[neighbor_region]:
                continue
            instance = State(neighbor, current.tool, target)
            if alt < dist[instance]:
                dist[instance] = alt
                queue.put(instance, block=False)
            elif instance not in visited:
                visited.add(instance)
                queue.put(instance, block=False)
        current_region = cave[current.position]

        # Now try tool swapping
        alt = current_dist + 7
        for tool in Tool:
            if tool != current.tool and tool in valid[current_region]:
                instance = State(current.position, tool, target)
                if alt < dist[instance]:
                    dist[instance] = alt
                    queue.put(instance, block=False)
                elif instance not in visited:
                    visited.add(instance)
                    queue.put(instance, block=False)

    return best


with open("inputs/day22.txt") as f:
    raw_input = f.read().splitlines()

depth, target = parse(raw_input)
# depth = 510
# target = 10 + 10j
erosion = create_map(depth, target)
cave, part1 = sum_values(erosion)
print(part1)

part2 = find_path(0, target, cave, target.real, target.imag, erosion)
print(part2)
