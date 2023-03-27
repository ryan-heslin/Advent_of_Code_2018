def parse_nodes(numbers, total=0):

    n_children, n_metadata = numbers[:2]
    del numbers[:2]
    for _ in range(n_children):
        total, numbers = parse_nodes(numbers, total)

    total += sum(numbers[:n_metadata])
    del numbers[:n_metadata]
    return total, numbers


with open("inputs/day8.txt") as f:
    raw_input = f.read().rstrip("\n").split(" ")

numbers = list(map(int, raw_input))
part1, _ = parse_nodes(numbers)
print(part1)
