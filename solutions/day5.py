import re
from math import inf

ASCII_OFFSET = 32
ASCII_A = ord("A")
LETTERS = 26


def reduce(polymer):
    while True:
        for i in range(len(polymer) - 1):
            if abs(polymer[i] - polymer[i + 1]) == ASCII_OFFSET:
                del polymer[i : i + 2]
                break
        else:
            return polymer


def optimize(polymer):
    best = inf

    for pair in zip(
        range(ASCII_A, ASCII_A + LETTERS),
        range(ASCII_A + ASCII_OFFSET, ASCII_A + ASCII_OFFSET + LETTERS),
    ):
        lower, upper = pair
        filtered = list(filter(lambda x: not (x == lower or x == upper), polymer))
        best = min(best, len(reduce(filtered)))
    return best


with open("inputs/day5.txt") as f:
    polymer = f.read().rstrip("\n")

codes = list(map(ord, polymer))
reduced = reduce(codes)
part1 = len(reduced)
print(part1)

part2 = optimize(codes)
print(part2)
