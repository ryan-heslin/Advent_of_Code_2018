import itertools
import re
from collections import defaultdict
from collections import deque
from functools import cache
from functools import cached_property
from math import ceil
from math import inf
from operator import attrgetter


@cache
def manhattan(x, y=(0, 0, 0)):
    return sum(abs(xi - yi) for xi, yi in zip(x, y, strict=True))

def clamp(x, low, high):
    return min(max(x, low), high)

class Prism():

    def __init__(self, vertices):
        vertices = tuple(sorted(vertices))
        # One-coord cube
        if len(set(vertices)) == 1:
            self.vertices = (vertices[0],)
            self.single = True
        else:
            self.vertices = vertices
            self.single = False
        closest = []
        min_vertex = self.vertices[0]
        for vertex in self.vertices:
            if vertex == min_vertex:
                closest.append(vertex)
            else:
                break

        self.closest = tuple(closest)

    # Return start-end pairs for all 12 edges
    @cached_property
    def edges(self):
        result = set()
        for start in self.vertices:
            for end in self.vertices:
                if start != end and (start[0] == end[0] or start[1] == end[1] or start[2] == end[2]):
                    result.add(tuple(sorted((start, end))))

        return result

    def vertex_inside(self, vertex):
        return self.xmin <= vertex[0] <= self.xmax and self.ymin <= vertex[1] <= self.xmax and self.zmin <= zertex <= self.zmax


    def subdivide(self):
        pass
        # Break into 8 subcubes

class Nanobot:
    def __init__(self, position, radius) -> None:
        self.position = position
        self.radius = radius

    def in_range(self, position):
        return self.radius >= manhattan(self.position, position)

    @cached_property
    def vertices(self):
        return tuple(itertools.chain((coord + self.radius, coord - self.radius) for coord in self.position))

    def __repr__(self) -> str:
        return (self.position, self.radius).__repr__()

    def edge_in_range(self, edge):
        for i in range(3):
            if edge[0][i] != edge[1][i]:
                dimension = i
                break
        else:
            raise ValueError

        # Find closest point on edge to center and check if it is in range
        closest = clamp(*sorted((edge[0][dimension], edge[1][dimension])), self.position[dimension])
        candidate = tuple(edge[0][i] if i != dimension else closest for i in range(3))
        return self.in_range(candidate)

    @classmethod
    def parse(cls, line):
        parts = [int(x) for x in re.findall(r"-?\d+", line)]
        return cls(tuple(parts[:3]), parts[-1])


def find_most_in_range(nanobots):
    longest = max(nanobots, key=attrgetter("radius"))
    return sum(longest.in_range(bot.position) for bot in nanobots)


def find_clusters(bots):
    result = {i: {i} for i in range(len(nanobots))}
    combos = itertools.combinations(range(len(nanobots)), r=2)
    for i, j in combos:
        reading = bots[i].in_range(bots[j].position) and bots[j].in_range(
            bots[i].position
        )
        if reading:
            result[i].add(j)
            result[j].add(i)

    return max(result.values(), key=len)


def minimize_distance(points):
    points = sorted(points)
    middle = len(points) // 2
    return points[middle - 1 : middle + 1]


def find_intervals(nanobots):
    # For each pair, all points for which
    #  sum(abs(c1) -p) <= r1
    #  sum(abs(c2) -p) <= r2
    for bot in nanobots:
        pass



def sweep(cluster, center=(0, 0, 0)):
    # TODO:
        # Start with bounding box containing all bots
        # Get biggest cluster of mutually in range bots
        # Use octree to divide and conquer
        # While queue
        # Subdivided into  8 cubes


        queue = # Bounding box of all regions's vertices
        best = inf

        for cube in queue:
            if manhattan(cube.min_vertex) >= best:
                continue
            for bot in cluster:
                # Only subdivide if each bot's region has at least one point overlapping
                # the cube
                if not ((any(cube.inside(vertex) for vertex in bot.vertices)
                or any(bot.in_range(vertex) for vertex in cube.vertices )
                or any (bot.in_range(edge) for edge in cube.edges))):
                    break
            else:
                    # Base case: single candidate point
                    if cube.single:
                        best = min(best, manhattan(cube.vertices[0]))
                    else:
                        queue.appendleft(cube.subdivide())

        return best



        # For each cube:
            # If any vertex of diamond inside cube:
                # Add cube to queue
            # Find octant of possible overlap (relative to cube) (unsure if this necessary)
                # Left, behind, below
                # Left, behind, above
                # Right, behind, below
                # Right, behind, above
                # Left, before, below
                # Left, before, above
                # Right, before, below
                # Right, before, above
                # Find faces of cube of intersection
            # Check if each vertex of cube in diamond region (doesn't cover all cases)
            # ELse check if each cube side in region
            #
            # If cube intersects every bot in cluster: <-- the hard part
                # Add to queu


with open("inputs/day23.txt") as f:
    raw_input = f.read().splitlines()

nanobots = list(map(Nanobot.parse, raw_input))
part1 = find_most_in_range(nanobots)
print(part1)

# Find biggest cluster of nanobots that are mutually in range
# Find minimal point in shared region

positions = list(map(attrgetter("position"), nanobots))
dimensions = list(zip(*positions))
box = list(map(minimize_distance, dimensions))

# grid = product(*(range(x[0], x[1] + 1) for x in box))
cluster = find_clusters(nanobots)
# 130576687 too high

result = sweep(nanobots)
print(result)
