from collections import defaultdict
from collections import deque

GROUP_START = "("
GROUP_END = ")"
SEPARATOR = "|"


def read_to_next_group(string):
    group_start = string.find(GROUP_START)
    group_end = string.find(GROUP_END)

    # End of string
    if group_start == -1 and group_end == -1:
        return len(string), ""
    elif group_start == -1 or group_end < group_start:
        return group_end, GROUP_END
    elif group_end == -1 or group_start < group_end:
        return group_start, GROUP_START
    else:
        raise ValueError


# If open group:


def build_tree(pattern):
    stop_type = None
    parts_found = 0
    parts = []
    tree = defaultdict(set)
    preceding = deque([])

    while pattern != "":
        end_char, stop_type = read_to_next_group(pattern)
        current = pattern[:end_char]
        pattern = pattern[end_char + 1 :]
        parts = current.split(SEPARATOR)
        current_preceding = preceding[-1] if len(preceding) else None

        for part in parts:
            id = parts_found
            parts_found += 1
            parts.append(part)
            if preceding:
                tree[current_preceding].add(id)

        if stop_type == GROUP_START:
            preceding.append(parts[-1])
        elif stop_type == GROUP_END:
            preceding.pop()

    return parts, tree


# Read pattern up to next group start/end
# Split into parts
# If parts
# Add each part to IDs
# Add
# If start, append tuple of parts to stack
# Else pop from stack
# For each part
# Append part to list
# In dict, map index to indices of children

# DO Dijkstra on returned reference and map
# Doors (edges) are bidirectional
