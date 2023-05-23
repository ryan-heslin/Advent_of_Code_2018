from collections import defaultdict
from itertools import product


def parse_claims(claims):
    result = {}
    for claim in claims:
        id, rhs = claim.split(" @ ")
        coord, dim = rhs.split(": ")
        x, y = coord.split(",")
        coord = complex(int(x), int(y))
        width, height = dim.split("x")
        id = int(id.lstrip("#"))
        result[id] = {"coord": coord, "dim": (int(width), int(height))}

    return result


def get_coords(coord, width, height):
    x = int(coord.real)
    y = int(coord.imag)
    return product(range(x, x + width), range(y, y + height))


def count_claims(claims):
    counts = defaultdict(lambda: 0)

    for claim in claims.values():
        tiles = get_coords(claim["coord"], *claim["dim"])
        for pair in tiles:
            counts[complex(*pair)] += 1

    return counts


def find_island(claims, counts):
    for id, claim in claims.items():
        tiles = get_coords(claim["coord"], *claim["dim"])
        if all(counts[complex(*tile)] == 1 for tile in tiles):
            return id


with open("inputs/day3.txt") as f:
    raw_input = f.read().splitlines()

claims = parse_claims(raw_input)
counts = count_claims(claims)
part1 = sum(num > 1 for num in counts.values())
print(part1)

part2 = find_island(claims, counts)
print(part2)
