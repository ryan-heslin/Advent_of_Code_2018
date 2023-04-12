from collections import defaultdict
from collections import deque
from math import inf

GROUP_START = "("
GROUP_END = ")"
ALTERNATE = "|"

DIRECTIONS = {"N": -1j, "E": 1, "S": 1j, "W": -1, "": 0}


def traverse(string):
    string = string[1:-1]
    length = len(string)
    graph = defaultdict(set)

    def inner(string_i, start):
        position = start
        while string_i < length:
            current_char = string[string_i]
            if current_char == GROUP_START:
                # breakpoint()
                string_i = inner(string_i + 1, position)
            elif current_char == GROUP_END:
                return string_i + 1
            elif current_char == ALTERNATE:
                position = start
                string_i += 1
            else:
                new = position + DIRECTIONS[current_char]
                graph[position].add(new)
                graph[new].add(position)
                position = new
                string_i += 1

        return string_i

    inner(0, 0)
    return graph


def dijkstra(start, graph):

    dist = defaultdict(lambda: inf)
    dist[start] = furthest = 0
    visited = set()
    queue = deque([start])

    while queue:
        current = queue.popleft()
        current_dist = dist[current]
        furthest = max(current_dist, furthest)
        alt = current_dist + 1
        for neighbor in graph[current]:
            dist[neighbor] = min(dist[neighbor], alt)
            if neighbor not in visited:
                queue.appendleft(neighbor)
                visited.add(neighbor)

    return dist


with open("inputs/day20.txt") as f:
    raw_input = f.read().rstrip("\n")

graph = traverse(raw_input)
dist = dijkstra(0, graph)
part1 = max(dist.values())
print(part1)

part2 = sum(v > 999 for v in dist.values())
print(part2)
