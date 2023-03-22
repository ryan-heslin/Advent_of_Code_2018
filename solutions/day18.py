from collections import Counter
from enum import Enum
from functools import cache


class Acre(Enum):
    OPEN = 0
    FOREST = 1
    YARD = 2


CODES = {".": Acre.OPEN, "|": Acre.FOREST, "#": Acre.YARD}


def parse(lines):
    result = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            result[complex(x, y)] = CODES[char]
    return result


def neighbor_maker(xmin, xmax, ymin, ymax):
    # From top clockwise
    shifts = (-1j, 1 - 1j, 1, 1 + 1j, 1j, -1 + 1j, -1, -1 - 1j)

    def valid(coord):
        return (xmin <= coord.real <= xmax) and (ymin <= coord.imag <= ymax)

    @cache
    def inner(coord):
        if not valid(coord):
            raise ValueError("Coordinate outside range")
        result = set()

        for shift in shifts:
            candidate = coord + shift
            if valid(candidate):
                result.add(candidate)
        return frozenset(result)

    return inner


def simulate(grid):

    new = None
    i = 0
    seen = {tuple(grid.values()): i}

    while True:
        new = {}
        for coord, acre in grid.items():
            counts = Counter(grid[a] for a in neighbors(coord))
            if acre == Acre.OPEN:
                if counts[Acre.FOREST] > 2:
                    new[coord] = Acre.FOREST
                else:
                    new[coord] = Acre.OPEN
            elif acre == Acre.FOREST:
                if counts[Acre.YARD] > 2:
                    new[coord] = Acre.YARD
                else:
                    new[coord] = Acre.FOREST
            else:
                if counts[Acre.FOREST] > 0 and counts[Acre.YARD] > 0:
                    new[coord] = Acre.YARD
                else:
                    new[coord] = Acre.OPEN

        i += 1
        store = tuple(new.values())
        if (previous := seen.get(store)) is not None:
            return previous, i, seen
        seen[store] = i
        grid = new


def resource_value(grid):
    counts = Counter(grid)
    return counts[Acre.FOREST] * counts[Acre.YARD]


with open("inputs/day18.txt") as f:
    raw_input = f.read().splitlines()

iterations = 10
neighbors = neighbor_maker(0, len(raw_input[0]) - 1, 0, len(raw_input) - 1)
grid = parse(raw_input)
cycle_start, cycle_end, cycles = simulate(grid.copy())


# Cycle detection, as usual
target = 1000000000
repetitions = target - cycle_end
last = repetitions % (cycle_end - cycle_start)
part1 = part2 = None

for data, i in cycles.items():
    if part1 is not None and part2 is not None:
        break
    if i == iterations:
        part1 = resource_value(data)
    elif i == last + cycle_start:
        part2 = resource_value(data)

print(part1)
print(part2)
