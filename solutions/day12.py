from collections import defaultdict

REPLACEMENTS = {"#": True, ".": False}
WINDOW = 5


def false_dict():
    return defaultdict(lambda: False)


def parse_state(state):
    di = false_dict()
    di.update(dict((i, REPLACEMENTS[char]) for i, char in enumerate(state)))
    return di


def parse_rules(rules):
    result = {}
    for line in rules:
        pattern, output = line.split(" => ")
        result[tuple(REPLACEMENTS[char] for char in pattern)] = REPLACEMENTS[output]

    return result


def display(state):
    return (
        " ".join(map(str, state.keys()))
        + "\n"
        + " ".join("#" if v else "." for v in state.values())
    )


def true_sum(di):
    return sum(k for k, v in di.items() if v)


def simulate(state, rules, n_generations=1000):
    edge = WINDOW // 2
    old_difference = part1 = None
    part1_done = False

    for i in range(n_generations):
        left = min(k for k, v in state.items() if v) - WINDOW + 1
        middle = left + edge
        greatest = max(state.keys())
        new = false_dict()
        window = [state[i] for i in range(left, left + WINDOW)]
        if rules.get(tuple(window)):
            new[middle] = True

        while left < greatest:
            left += 1
            middle += 1
            window.pop(0)
            window.append(state[left + WINDOW - 1])
            if rules.get(tuple(window)):
                new[middle] = True

        if not part1_done and i == 20:
            part1 = true_sum(state)
            part1_done = True
        difference = true_sum(new) - true_sum(state)
        if difference == old_difference:
            return part1, {
                "difference": difference,
                "baseline": true_sum(state),
                "iteration": i,
            }

        state = new
        old_difference = difference


with open("inputs/day12.txt") as f:
    start, rules = f.read().split("\n\n")

state = parse_state(start.split(": ")[1])
rules = rules.splitlines()
rules = parse_rules(rules)

baseline = true_sum(state)
part1, data = simulate(state, rules)
print(part1)

part2 = data["baseline"] + (data["difference"] * (50000000000 - data["iteration"]))
print(part2)
