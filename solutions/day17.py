from collections import defaultdict
from enum import Enum
from itertools import starmap
from itertools import zip_longest
from operator import attrgetter


class Ground(Enum):
    SAND = 0
    CLAY = 1
    WATER = 2


def flow(start, tops, source):
    # Somehow move next block to previous space occupied
    # Store, reverse sequence of horizontal moves?

    # Once bottom reached, follow different behavior: flow until hitting next
    # water tile
    # Don't go to side if hitting pillar of water
    # while not bottom
        # while not blocked
        # If above air:
            # Move to highest space below
                # If bottom:
                    # bottom = True
                    #blocked = True
                    # break
        # Else
            # If can move left:
                # Move left
            # Else if can move right
            # Move 1 right
            # Else
                # blocked = true

    # while

def xrange(data):
    real = attrgetter("real")
    return int(min(data, key=real).real), int(max(data, key=real).real)


def display(data, ymax):
    xmin, xmax = xrange(data)
    mapping = {Ground.SAND.value: ".", Ground.CLAY.value: "#", Ground.WATER.value: "~"}

    return "\n".join(
        "".join(mapping[data[complex(x, y)]] for x in range(xmin, xmax + 1))
        for y in range(0, ymax + 1)
    )


def topmost(data):
    xmin, xmax = xrange(data)
    ymax = int(max(data.keys(), key=attrgetter("imag")).imag)
    result = {}
    for x in range(xmin, xmax + 1):
        for y in range(ymax + 1):
            coord = complex(x, y)
            if data[coord] == Ground.CLAY.value:
                value = coord
                break
        else:
            value = None
        result[x] = value

    return result


def parse(lines):
    result = defaultdict(lambda: 0)
    coords = []

    for line in lines:
        parts = line.split(", ")
        first = int(parts[0].split("=")[-1])
        second = tuple(map(int, parts[1][2:].split("..")))
        pairs = list(
            zip_longest((first,), range(second[0], second[1] + 1), fillvalue=first)
        )

        if parts[0][0] == "y":
            pairs[0], pairs[1] = pairs[1], pairs[0]
        coords.extend(starmap(complex, pairs))

    result.update(dict(zip_longest(coords, [], fillvalue=Ground.CLAY.value)))
    return result


with open("inputs/day17.txt") as f:
    raw_input = f.read().splitlines()

source = 500
underground = parse(raw_input)
ymax = int(max(underground.keys(), key=attrgetter("imag")).imag)
# print(display(underground, ymax))
tops = topmost(underground)
