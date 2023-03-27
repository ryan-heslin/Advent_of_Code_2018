def parse_nodes(numbers, total=0):

    n_children, n_metadata = numbers[:2]
    del numbers[:2]
    for _ in range(n_children):
        total, numbers = parse_nodes(numbers, total)

    total += sum(numbers[:n_metadata])
    del numbers[:n_metadata]
    return total, numbers


def sum_indices(l, indices):
    s = 0
    bound = len(l)
    for i in indices:
        i -= 1
        if 0 <= i < bound:
            s += l[i]
    return s


def sum_nodes(numbers):

    n_children, n_metadata = numbers[:2]
    del numbers[:2]
    children = []

    for _ in range(n_children):
        value, numbers = sum_nodes(numbers)
        children.append(value)

    metadata = numbers[:n_metadata]
    del numbers[:n_metadata]

    if n_children:
        total = sum_indices(children, metadata)
    else:
        total = sum(metadata)

    return total, numbers


with open("inputs/day8.txt") as f:
    raw_input = f.read().rstrip("\n").split(" ")

numbers = list(map(int, raw_input))
part1, _ = parse_nodes(list(numbers))
print(part1)

part2, _ = sum_nodes(numbers)
print(part2)
