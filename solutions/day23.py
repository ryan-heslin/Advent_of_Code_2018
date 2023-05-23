import functools
import itertools
import math
import operator
import re
from operator import attrgetter
from queue import PriorityQueue


def max_extent(vertices):
    vertices = functools.reduce(operator.add, vertices)
    return max(map(abs, vertices))


def unit_cube(unit):
    # Subtract 1 because all sides are inclusive
    return (
        (-unit, -unit, -unit),
        (unit, -unit, -unit),
        (unit, unit, -unit),
        (-unit, unit, -unit),
        (-unit, -unit, unit),
        (unit, -unit, unit),
        (unit, unit, unit),
        (-unit, unit, unit),
    )


def find_absmax(bots):
    return max(max_extent(bot.vertices) for bot in bots)


@functools.cache
def manhattan(x, y=(0, 0, 0)):
    assert len(x) == len(y)
    return sum(abs(xi - yi) for xi, yi in zip(x, y, strict=True))


def clamp(x, low, high):
    return min(max(x, low), high)


def add_tuples(x, y):
    return tuple(xi + yi for xi, yi in zip(x, y))


class Cube:
    def __init__(self, vertices):
        vertices = sorted(vertices)

        # Min and max coord for each dimension
        data = tuple(zip(*vertices))
        self.mins = list(map(min, data))
        self.maxes = list(map(max, data))

        if len(vertices) == 1:
            self.edges = None
            self.length = 0
            self.single = True
        else:
            self.edges = self._set_edges(vertices)
            # Since first pair is up-down
            self.length = abs(self.edges[0][0][2] - self.edges[0][1][2])
            self.single = False

        self.vertices = vertices
        # Vertices nearest origin (may not be unique)
        self.min_distance = min(map(manhattan, self.vertices))

    # Return start-end pairs for all 12 edges
    @staticmethod
    def _set_edges(vertices):
        # Can hard-code because we know order of vertices
        return (
            (vertices[0], vertices[1]),
            (vertices[0], vertices[2]),
            (vertices[0], vertices[4]),
            (vertices[1], vertices[3]),
            (vertices[1], vertices[5]),
            (vertices[2], vertices[3]),
            (vertices[2], vertices[6]),
            (vertices[3], vertices[7]),
            (vertices[4], vertices[5]),
            (vertices[4], vertices[6]),
            (vertices[5], vertices[7]),
            (vertices[6], vertices[7]),
        )

    def vertex_inside(self, vertex):
        return all(self.mins[i] <= vertex[i] <= self.maxes[i] for i in range(3))

    def subdivide(self):
        # Start from left face; since vertices sorted, first four compose it
        # x: left-right y: front/rear z: up/down
        # Since cube inclusive, second partition BEGINS with the coordinate
        # this far from first partition
        # Base case
        if self.length == 1:
            return (Cube((vertex,)) for vertex in self.vertices)
        half = self.length // 2

        # Left/rear/down:
        # In standard vertex order for each
        additions = (
            # Left/rear/down
            (
                (0, 0, half),
                (0, half, 0),
                (0, half, half),
                (half, 0, 0),
                (half, 0, half),
                (half, half, 0),
                (half, half, half),
            ),
            (
                (0, 0, -half),
                (0, half, -half),
                (0, half, 0),
                (half, 0, -half),
                (half, 0, 0),
                (half, half, -half),
                (half, half, 0),
            ),
            # Left/front/down
            (
                (0, -half, 0),
                (0, -half, half),
                (0, 0, half),
                (half, -half, 0),
                (half, -half, half),
                (half, 0, 0),
                (half, 0, half),
            ),
            # Left/front/ up
            (
                (0, -half, -half),
                (0, -half, 0),
                (0, 0, -half),
                (half, -half, -half),
                (half, -half, 0),
                (half, 0, -half),
                (half, 0, 0),
            ),
            # Right/rear/down
            (
                (-half, 0, 0),
                (-half, 0, half),
                (-half, half, 0),
                (-half, half, half),
                (0, 0, half),
                (0, half, 0),
                (0, half, half),
            ),
            # Right/rear/up
            (
                (-half, 0, -half),
                (-half, 0, 0),
                (-half, half, -half),
                (-half, half, 0),
                (0, 0, -half),
                (0, half, -half),
                (0, half, 0),
            ),
            # Right/front/down
            (
                (-half, -half, 0),
                (-half, -half, half),
                (-half, 0, 0),
                (-half, 0, half),
                (0, -half, 0),
                (0, -half, half),
                (0, 0, half),
            ),
            # Right/front/up
            (
                (-half, -half, -half),
                (-half, -half, 0),
                (-half, 0, -half),
                (-half, 0, 0),
                (0, -half, -half),
                (0, -half, 0),
                (0, 0, -half),
            ),
        )
        cls = type(self)
        return (
            cls((vertex,) + tuple(add_tuples(shift, vertex) for shift in addition))
            for vertex, addition in zip(self.vertices, additions)
        )

    @functools.cached_property
    def center(self):
        half = self.length // 2
        return (
            self.vertices[0][0] + half,
            self.vertices[0][1] + half,
            self.vertices[0][2] + half,
        )

    def __repr__(self):
        return self.vertices.__repr__()

    def __lt__(self, other):
        return manhattan(self.center) < manhattan(other.center)


class Nanobot:
    def __init__(self, position, radius) -> None:
        self.position = position
        self.radius = radius

    def in_range(self, position):
        return self.radius >= manhattan(self.position, position)

    @functools.cached_property
    def vertices(self):
        return (
            (self.position[0] + self.radius, self.position[1], self.position[2]),
            (self.position[0] - self.radius, self.position[1], self.position[2]),
            (self.position[0], self.position[1] - self.radius, self.position[2]),
            (self.position[0], self.position[1] + self.radius, self.position[2]),
            (self.position[0], self.position[1], self.position[2] + self.radius),
            (self.position[0], self.position[1], self.position[2] - self.radius),
        )

    def __repr__(self) -> str:
        return (self.position, self.radius).__repr__()

    # Is any point of cube edge in scanner radius?
    def edge_in_range(self, edge):
        for i in range(3):
            if edge[0][i] != edge[1][i]:
                dimension = i
                break
        else:
            raise ValueError

        # Find closest point on edge to center and check if it is in range

        target = self.position[dimension]
        bounds = sorted((edge[0][dimension], edge[1][dimension]))
        closest = (
            bounds[0]
            if target < bounds[0]
            else bounds[1]
            if target > bounds[1]
            else target
        )
        candidate = tuple(edge[0][i] if i != dimension else closest for i in range(3))
        return self.in_range(candidate)

    @classmethod
    def parse(cls, line):
        parts = [int(x) for x in re.findall(r"-?\d+", line)]
        return cls(tuple(parts[:3]), parts[-1])


def find_most_in_range(nanobots):
    longest = max(nanobots, key=attrgetter("radius"))
    return sum(longest.in_range(bot.position) for bot in nanobots)


def count_bots_in_range(cube, bots):
    return sum(
        any(cube.vertex_inside(vertex) for vertex in bot.vertices)
        or any(bot.in_range(vertex) for vertex in cube.vertices)
        or (
            not cube.single
            and (
                any(bot.edge_in_range(edge) for edge in cube.edges)
                # or bot.in_range(cube.center)
            )
        )
        for bot in bots
    )


def octary_search(nanobots, box):
    closest_distance = math.inf
    most_bots = max(sum(b.in_range(a.position) for a in nanobots) for b in nanobots)

    queue = PriorityQueue()
    queue.put((-len(nanobots), Cube(box)))

    while queue.qsize():
        possible_bots, cube = queue.get(block=False)
        possible_bots *= -1
        if possible_bots < most_bots:
            continue

        # Closest distance with the most mots
        new_cubes = cube.subdivide()
        for neighbor in new_cubes:
            if neighbor.single:
                final_bots = count_bots_in_range(neighbor, nanobots)
                if final_bots > most_bots:
                    most_bots = final_bots
                    closest_distance = neighbor.min_distance
                elif final_bots == most_bots:
                    closest_distance = min(closest_distance, neighbor.min_distance)
            else:
                this_bots = count_bots_in_range(neighbor, nanobots)
                if this_bots > most_bots or (
                    this_bots == most_bots and neighbor.min_distance < closest_distance
                ):
                    queue.put((-this_bots, neighbor), block=False)

    return closest_distance


with open("inputs/day23.txt") as f:
    raw_input = f.read().splitlines()

nanobots = list(map(Nanobot.parse, raw_input))
part1 = find_most_in_range(nanobots)
print(part1)

positions = list(map(attrgetter("position"), nanobots))
dimensions = list(zip(*positions))

extent = find_absmax(nanobots)
power = math.ceil(math.log2(extent))
box = unit_cube(2**power)
part2 = octary_search(nanobots, box)
print(part2)
