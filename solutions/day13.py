from operator import attrgetter

# All ASCII codes
ORIENTATIONS = {60: -1, 62: 1, 94: -1j, 118: 1j}
TRACKS = {43: "intersection", 47: "right", 92: "left", 45: "straight", 124: "straight"}
SPACE = 32
imag = attrgetter("imag")


def display(x):
    return f"{int(x.real)},{int(x.imag)}"


def compare_complex(x):
    return (x.imag, x.real)
    # if x.imag < y.imag:
    #     return True
    # elif x.imag == y.imag:
    #     return x.imag < y.imag
    # else:
    #     return False


def identity(x):
    return x


def left90(x):
    return complex(x.imag, -x.real)


def right90(x):
    return complex(-x.imag, x.real)


class Minecart:
    intersections = (left90, identity, right90)
    n_intersections = len(intersections)
    rotations = {
        ("left", 0 + 1j): left90,
        ("left", 0 - 1j): left90,
        ("left", -1): right90,
        ("left", 1): right90,
        ("right", 0 + 1j): right90,
        ("right", 0 - 1j): right90,
        ("right", -1): left90,
        ("right", 1): left90,
    }

    def __init__(self, position, orientation) -> None:
        self.__position = position
        self.orientation = orientation
        self.intersection = 0
        self.track = 45 if orientation.imag == 0 else 124

    def move(self):
        self.turn()
        self.__position += self.orientation

    def turn(self):
        track = TRACKS[self.track]
        if track == "intersection":
            self.orientation = self.__class__.intersections[self.intersection](
                self.orientation
            )
            self.intersection = (self.intersection + 1) % self.__class__.n_intersections
        # Both directions switch if going left-right instead of up/down
        elif track in ("left", "right"):
            self.orientation = self.__class__.rotations[(track, self.orientation)](
                self.orientation
            )
        # elif (
        #     track == "right"
        # ):  # / Right if going up/down, left going down, etc. (down is 1j)
        #     # rotator = (left90, right90)[self.__position.imag == 1]
        #     self.orientation = (
        #         -1 * abs(self.orientation.real) * right90(self.orientation)
        #     )
        # elif track == "left":  # \
        #     self.orientation = (
        #         -1 * abs(self.orientation.real) * left90(self.orientation)
        #     )
        # If straight, keep orientation

    @property
    def position(self):
        return self.__position


def parse(lines):
    layout = {}
    minecarts = {}
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            code = ord(char)
            coord = complex(x, y)
            if orientation := ORIENTATIONS.get(code):
                minecarts[coord] = Minecart(coord, orientation)
                code = 45 if orientation.imag == 0 else 124
            if code != SPACE:
                layout[coord] = code

    return layout, minecarts


def run(minecarts, layout):
    crashed = False
    part1 = None

    while len(minecarts) > 1:
        order = sorted(minecarts.keys(), key=compare_complex)
        for position in order:
            # Don't know why this works, but it does...
            if position not in minecarts:
                continue
            cart = minecarts.pop(position)
            cart.move()
            new = cart.position
            cart.track = layout[new]
            # Crash
            if new in minecarts:
                if not crashed:
                    part1 = cart.position
                    crashed = True
                minecarts.pop(new)
                # order.remove(position)
            else:
                minecarts[new] = cart
    return part1, next(iter(minecarts.keys()))


with open("inputs/day13.txt") as f:
    raw_input = f.read().splitlines()

layout, minecarts = parse(raw_input)
part1, part2 = run(minecarts, layout)
print(display(part1))
print(display(part2))
