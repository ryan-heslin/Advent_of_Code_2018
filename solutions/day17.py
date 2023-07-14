from collections import defaultdict
from collections import deque
from enum import Enum
from itertools import starmap
from itertools import zip_longest
from operator import attrgetter


class Ground(Enum):
    SAND = 0
    CLAY = 1
    WATER = 2


def flow(state, source, reservoirs):
    # Water can flow beyond x-bounds
    imag = attrgetter("imag")
    sand = Ground.SAND.value
    clay = Ground.CLAY.value
    water = Ground.WATER.value
    flowed = permanent = 0

    clay_veins = {k for k, v in state.items() if v == clay}
    ymin = int(min(clay_veins, key=imag).imag)
    ymax = int(max(clay_veins, key=imag).imag)
    prev = deque([source])
    done = set()

    def flow_until_obstruction(position):
        nonlocal flowed
        nonlocal permanent

        # Always append new block, because its possible directions not yet known
        while True:
            if state[new := position + 1j] == sand:
                if new.imag > ymax:
                    done.add(position)
                    return position
            elif state[new] == water and new not in reservoirs:
                done.add(position)
                return position
            elif state[new := position - 1] == sand:
                pass
            elif state[new := position + 1] == sand:
                done.add(position)
                # No point appending, since no other movement possible from here
            else:
                done.add(position)
                return position

            # Can only flow on top of flowing water
            position = new
            prev.appendleft(position)
            state[position] = water
            # Don't count beyond y bounds
            permanent += position in reservoirs
            flowed += ymin <= position.imag <= ymax

    # If tile above water, only flow from it if in reservoir; otherwise skip
    flow_until_obstruction(source)
    while prev:
        current = prev.pop()
        if current in done:
            continue
        flow_until_obstruction(current)
        prev.appendleft(current)

    return flowed, permanent


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


def mark_reservoirs(xranges, underground):
    clay = Ground.CLAY.value
    result = set()

    for xrange, floor in xranges:
        left, right = xrange
        y = floor - 1
        while floor >= 0:
            left_sealed = underground[complex(left, y)] == clay
            right_sealed = underground[complex(right, y)] == clay

            # Annoying edge case of overlapping reservoirs
            if not (left_sealed or right_sealed):
                break
            if left_sealed and not right_sealed:
                for new_right in range(left + 2, right):
                    if underground[complex(new_right, y)] == clay:
                        right = new_right
                        break
                else:
                    break
            elif right_sealed and not left_sealed:
                for new_left in range(right - 2, left - 1, -1):
                    if underground[complex(new_left, y)] == clay:
                        left = new_left
                        break
                else:
                    break
            result.update(
                starmap(complex, zip_longest(range(left, right + 1), (y,), fillvalue=y))
            )
            y -= 1

    return result


def parse(lines):
    result = defaultdict(lambda: 0)
    coords = []
    bases = set()

    for line in lines:
        parts = line.split(", ")
        first = int(parts[0].split("=")[-1])
        second = tuple(map(int, parts[1][2:].split("..")))

        if parts[0][0] == "x":
            pairs = list(
                zip_longest((first,), range(second[0], second[1] + 1), fillvalue=first)
            )
        else:
            bases.add((second, first))
            pairs = list(
                zip_longest(range(second[0], second[1] + 1), (first,), fillvalue=first)
            )

        coords.extend(starmap(complex, pairs))

    result.update(dict(zip_longest(coords, [], fillvalue=Ground.CLAY.value)))
    return result, bases


with open("inputs/day17.txt") as f:
    raw_input = f.read().splitlines()

source = 500
underground, bases = parse(raw_input)
reservoirs = mark_reservoirs(bases, underground)

ymax = int(max(underground.keys(), key=attrgetter("imag")).imag)
part1, part2 = flow(underground, source, reservoirs)
print(part1)
print(part2)
