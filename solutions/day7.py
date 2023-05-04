from collections import defaultdict
from math import inf
from operator import itemgetter


ASCII_A = ord("A")


def parse(lines):
    parents = defaultdict(set)
    children = defaultdict(set)

    for line in lines:
        parts = line.split(" ")
        parent = parts[1]
        child = parts[7]
        children[parent].add(child)
        parents[child].add(parent)

    return parents, children


def find_roots(parents, children):
    return set(children.keys()) - set(parents.keys())


def order(parents, children, roots):
    # Multiple firsts possible
    result = [min(roots)]
    unexplored = roots - set(result) | children[result[0]]

    # breakpoint()
    while unexplored:
        found = False
        for node in sorted(unexplored):
            if node in result:
                continue
            this_parents = parents[node]
            for parent in this_parents:  # Check all prerquisites done before adding
                if parent not in result:  # Don't repeat nodes
                    break
            else:
                found = True
                break
        if found:
            result.append(node)
            unexplored.update(children[node])
            unexplored.remove(node)
            unexplored.difference_update(set(result))

    return "".join(result)


def completion_time(task, baseline=60):
    return baseline + ord(task) - ASCII_A + 1


def complete_tasks(parents, children, roots, n_workers=5):

    minutes = 0
    workers = []
    done = set()
    n_tasks = len(children)
    open = roots
    second = itemgetter(1)

    while len(done) < n_tasks:
        n_free = n_workers - len(workers)
        if n_free > 0:
            available = sorted(filter(lambda t: len(parents[t] - done) == 0, open))
            # End early if out of tasks
            for _ in range(n_free):
                if not available:
                    break
                task = available.pop(0)
                open.remove(task)
                workers.append([task, completion_time(task)])

        workers.sort(reverse=True, key=second)
        shortest = workers[-1][1]
        minutes += shortest
        cutoff = None

        # Subtract closest increment from all workers
        for i, worker in enumerate(workers):
            worker[1] -= shortest
            if worker[1] == 0:
                if cutoff is None:
                    cutoff = i
                task = worker[0]
                done.add(task)
                open.update(children[task])
        # Remove completed workers
        del workers[cutoff:]
    return minutes


with open("inputs/day7.txt") as f:
    raw_input = f.read().splitlines()

parents, children = parse(raw_input)
roots = find_roots(parents, children)
part1 = order(parents, children, roots)
print(part1)

part2 = complete_tasks(parents, children, roots, 5)
print(part2)
