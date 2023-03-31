from collections import defaultdict
from collections import deque
from functools import cache
from itertools import chain
from math import inf
from operator import attrgetter


class Unit:
    def __init__(self, allegiance, hp=200, attack=3) -> None:
        self.allegiance = allegiance
        self.hp = hp
        self.attack = attack

    def strike(self, target):
        target.hp -= self.attack

    def __bool__(self):
        return self.hp > 0

    def __repr__(self) -> str:
        return (self.allegiance, self.hp, self.attack).__repr__()


def display(state):
    xmax = len(raw_input[0])
    ymax = len(raw_input)

    result = []
    for y in range(ymax + 1):
        result.append("")
        for x in range(xmax + 1):
            val = state.get(complex(x, y), "#")
            if val != "#":
                val = val.allegiance[0] if val else "."
            result[-1] += val

    return "\n".join(result)


def make_neighbors(coords):
    # Reading order
    shifts = (-1j, -1, 1, 1j)

    # Ignores if units in neighbors
    @cache
    def result(x):
        return set(x + shift for shift in shifts if x + shift in coords)

    return result


def parse(lines):

    result = {}
    allegiances = {"E": "Elves", "G": "Goblins"}

    for j, line in enumerate(lines):
        for i, char in enumerate(line):
            if char != "#":
                coord = complex(i, j)
                if char in allegiances:
                    result[coord] = Unit(allegiance=allegiances[char])
                else:
                    result[coord] = None

    return result


def targets(position, mapping):
    return (mapping[k] for k in neighbors(position) if mapping[k])


# reading order
def less(x, y):
    return (x.imag, x.real) < (y.imag, y.real)


def reading_order(coords):
    # Top/down bottom/left
    return sorted(coords, key=lambda coord: (coord.imag, coord.real))


def turn_order(mapping):
    return reading_order(coord for coord, el in mapping.items() if el)


def choose_motion(position, targets, mapping):
    # Already in range, so don't move
    for neighbor in neighbors(position):
        if neighbor in targets:
            return position

    # All empty spaces adjacent to enemies
    # breakpoint()
    adjacencies = set(
        neighbor
        for target in targets
        for neighbor in neighbors(target)
        if not mapping[neighbor]
    )

    paths, destination = all_paths(position, adjacencies, mapping)

    # No positions found
    if destination:
        options = find_initial_steps(paths, destination, position)
        return min(options, key=lambda p: (p.imag, p.real))
    return position


def choose_target(position, allegiance, mapping):

    choices = neighbors(position)
    # breakpoint()
    possible = [
        choice
        for choice in choices
        if mapping[choice] and mapping[choice].allegiance != allegiance
    ]
    if possible:
        return sorted(
            possible, key=lambda coord: (mapping[coord].hp, coord.imag, coord.real)
        )[0]


def adjacent(x, y):
    return abs(x) - abs(y) == 1


def simulate(state):
    round = 0
    forces = defaultdict(set)
    for pos, val in state.items():
        if val:
            forces[val.allegiance].add(pos)

    names = tuple(forces.keys())
    opponents = {names[0]: names[1], names[1]: names[0]}

    # breakpoint()
    while True:

        # Have to update positions when units move
        posititions = forces[names[0]] | forces[names[1]]
        order = deque(reading_order(posititions))
        updates = {}
        print(round)
        print(display(state), "\n")
        # if len(forces["Elves"]) == 2:
        #     breakpoint()
        while order:
            # sum(range(1000000))
            current = order.popleft()
            current = updates.get(current, current)
            if unit := state.get(current):
                friendly = unit.allegiance
                enemy = opponents[friendly]
                possible_targets = forces[enemy]

                # One army dead, game over
                if not possible_targets:
                    return round * sum(state[k].hp for k in forces[friendly])

                new_position = choose_motion(current, possible_targets, state)
                updates[current] = new_position
                forces[friendly].remove(current)
                forces[friendly].add(new_position)
                state.pop(current)
                state[current] = None
                state[new_position] = unit

                # Attack if next to hostile
                if target := choose_target(new_position, friendly, state):
                    hostile = state[target]
                    unit.strike(hostile)

                    # Remove dead unit
                    if not hostile:
                        state[target] = None
                        forces[enemy].remove(target)
                        updates.pop(target, None)

            # Units die instantly

        round += 1


# Turn order: units in reading order (top down, left to right)
# In range: adjacent to enemy unit in cardinal direction
# Turn:
# If not in range:
# Find all spaces in range that are reachable by fewest steps
# If tie, choose first in reading order
# Move one step along whichever of the shortest paths has earliest first step in reading order

# Attack
# If in range:
# Select target in range with fewest hitpoints (tiebreaker: reading ordre)
# Deal attack power damaage to target (dies instantly if below 1 hp)
# 3 attack power, 200 hp

# Number of full rounds played * sum of survivors' hp


def all_paths(source, targets, mapping):
    dist = defaultdict(lambda: inf)
    dist[source] = 0

    # Store options in prev, recover original by reverse iteration?
    prev = defaultdict(set)
    shortest_dist = inf
    nearest_target = complex(inf, inf)
    queue = deque([source])
    visited = set()

    while queue:
        current = queue.pop()
        current_dist = dist[current]

        # if current in targets:
        #     if source == 3 + 4j:
        #         breakpoint()
        #     if current_dist < shortest_dist:
        #         nearest_target = current
        #         shortest_dist = current_dist
        #     elif current_dist == shortest_dist and less(current, nearest_target):
        #         nearest_target = current
        # continue

        # No chance of finding best path, so abort
        # if current_dist > shortest_dist:
        #     continue
        alt = current_dist + 1

        for neighbor in neighbors(current):
            if not mapping[neighbor]:
                if alt < dist[neighbor]:
                    prev[neighbor] = {current}
                    dist[neighbor] = alt
                # Alternate path found
                elif alt == dist[neighbor]:
                    prev[neighbor].add(current)
                # assert alt < dist[neighbor]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.appendleft(neighbor)

    reached = set(dist.keys()) & targets
    if reached:
        nearest_target = min(reached, key=lambda k: (dist[k], k.imag, k.real))
        # print(nearest_target)
        return prev, nearest_target
    return None, None


# Find the first steps of all possible shortest paths to a target
def find_initial_steps(prev, endpoint, origin):

    queue = deque([endpoint])
    result = set()
    # if origin == 4 + 4j:
    #     breakpoint()

    while queue:
        next = queue.popleft()
        before = prev[next]
        for node in before:
            if node == origin:
                result.add(next)
            else:
                queue.appendleft(node)

    return result
    # Find shortest paths to all targets
    # Just need first steps of each possible path, since first in reading order chosen
    # Then read backward, expanding each with branches


def find_min_attack(start):

    defeat = True
    high = 200


with open("inputs/day15.txt") as f:
    raw_input = f.read().splitlines()

state = parse(raw_input)
neighbors = make_neighbors(state)
part1 = simulate(dict(state))
print(part1)
