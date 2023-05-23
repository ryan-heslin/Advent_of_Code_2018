def parse(line):
    return tuple(map(int, line.split(",")))


def manhattan(x, y):
    return sum(abs(x - y) for x, y in zip(x, y))


def solve(stars):
    result = 0
    while stars:
        current = {stars.pop(min(stars.keys()))}
        result += 1
        while current:
            removals = set()
            for i, neighbor in stars.items():
                if any(manhattan(known, neighbor) < 4 for known in current):
                    removals.add(i)

            current = {stars.pop(i) for i in removals}

    return result


with open("inputs/day25.txt") as f:
    raw_input = f.read().splitlines()

stars = dict(zip(range(len(raw_input)), map(parse, raw_input)))
part1 = solve(stars)
print(part1)
