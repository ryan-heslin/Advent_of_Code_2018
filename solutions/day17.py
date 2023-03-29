def parse(lines):
    result = {}
    for line in lines:
        parts = line.split(", ")
        first = int(parts[0].split("=")[-1])
        second = map(int, parts[1][2:].split(".."))
        if parts[0][0] == "x":
