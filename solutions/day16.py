import operator
import re
from collections import defaultdict


def make_operation(operation, first_literal, second_literal):

    if first_literal and second_literal:

        def result(a, b, c, registers):
            registers[c] = operation(a, b)
            return registers

    elif first_literal:

        def result(a, b, c, registers):
            registers[c] = operation(a, registers[b])
            return registers

    elif second_literal:

        def result(a, b, c, registers):
            registers[c] = operation(registers[a], b)
            return registers

    else:

        def result(a, b, c, registers):
            registers[c] = operation(registers[a], registers[b])
            return registers

    return result


def greater(a, b):
    return int(a > b)


def equal(a, b):
    return int(a == b)


def identity(a, _):
    return a


class Program:

    mulr = make_operation(operator.mul, False, False)
    muli = make_operation(operator.mul, False, True)
    addr = make_operation(operator.add, False, False)
    addi = make_operation(operator.add, False, True)
    banr = make_operation(operator.and_, False, False)
    bani = make_operation(operator.and_, False, True)
    borr = make_operation(operator.or_, False, False)
    bori = make_operation(operator.or_, False, True)
    setr = make_operation(identity, False, False)
    seti = make_operation(identity, True, False)
    gtir = make_operation(greater, True, False)
    gtrr = make_operation(greater, False, False)
    gtri = make_operation(greater, False, True)
    eqir = make_operation(equal, True, False)
    eqri = make_operation(equal, False, True)
    eqrr = make_operation(equal, False, False)
    operations = list(
        map(
            staticmethod,
            [
                mulr,
                muli,
                addr,
                addi,
                banr,
                bani,
                borr,
                bori,
                setr,
                seti,
                gtir,
                gtrr,
                gtri,
                eqir,
                eqri,
                eqrr,
            ],
        )
    )

    def __init__(self, code, translation, n_registers=4):
        self.registers = dict(zip(range(n_registers), [0] * 4))
        self.code = code
        self.translation = dict(translation)

    def exec(self):
        position = 0
        cls = type(self)
        while position < len(self.code):
            line = self.code[position]
            opcode = line[0]
            self.registers = cls.operations[self.translation[opcode]](
                *line[1:], self.registers
            )
            position += 1


def extract_numbers(line):
    cleaned = re.sub(r"[^0-9\s]+", "", line).rstrip(" ").lstrip(" ").split(" ")
    return list(map(int, cleaned))


def parse_sample(lines):
    return [extract_numbers(line) for line in lines.splitlines()]


def try_opcodes(samples):
    three_or_more = count = 0
    opcodes = defaultdict(lambda: set(range(16)))

    for triplet in samples:
        before, input, after = triplet
        original = list(before)
        opcode = input[0]
        count = 0

        for i, operation in enumerate(Program.operations):
            result = operation(*input[1:], list(original))
            if result == after:
                count += 1
            else:
                opcodes[opcode].discard(i)
        three_or_more += count > 2

    return three_or_more, opcodes


# Maps indices of actual opcodes to possible outcodes in program (my) ordering
def deduce_opcodes(mapping):
    translation = {}
    found = set()

    while len(mapping):
        for their_opcode, possibilities in sorted(
            mapping.items(), key=lambda x: len(x[1])
        ):
            if len(possibilities) == 1:
                true_opcode = mapping.pop(their_opcode).pop()
                translation[their_opcode] = true_opcode
                found.add(true_opcode)
            else:
                mapping[their_opcode].difference_update(set(translation.values()))
    return translation


with open("inputs/day16.txt") as f:
    raw_input = f.read().rstrip("\n")

samples, program = raw_input.split("\n\n\n")

processed = list(map(parse_sample, samples.split("\n\n")))
part1, opcodes = try_opcodes(processed)
print(part1)

translation = deduce_opcodes(opcodes)
code = list(map(extract_numbers, program.splitlines()[1:]))
program = Program(code, translation, 4)
program.exec()
part2 = program.registers[0]
print(part2)
