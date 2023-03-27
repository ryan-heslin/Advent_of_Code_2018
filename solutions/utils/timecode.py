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
            registers[c] = operation(a, registers.get(b))
            return registers

    elif second_literal:

        def result(a, b, c, registers):
            registers[c] = operation(registers[a], b)
            return registers

    else:

        def result(a, b, c, registers):
            registers[c] = operation(registers[a], registers.get(b))
            return registers

    return result


def greater(a, b):
    return int(a > b)


def equal(a, b):
    return int(a == b)


def identity(a, _):
    return a


operations = dict(
    mulr=make_operation(operator.mul, False, False),
    muli=make_operation(operator.mul, False, True),
    addr=make_operation(operator.add, False, False),
    addi=make_operation(operator.add, False, True),
    banr=make_operation(operator.and_, False, False),
    bani=make_operation(operator.and_, False, True),
    borr=make_operation(operator.or_, False, False),
    bori=make_operation(operator.or_, False, True),
    setr=make_operation(identity, False, False),
    seti=make_operation(identity, True, False),
    gtir=make_operation(greater, True, False),
    gtrr=make_operation(greater, False, False),
    gtri=make_operation(greater, False, True),
    eqir=make_operation(equal, True, False),
    eqri=make_operation(equal, False, True),
    eqrr=make_operation(equal, False, False),
)


class Program:
    operations = operations

    def __init__(self, n_registers):
        self.registers = dict(zip(range(n_registers), [0] * n_registers))

    # Convert each instruction line into one-argument function
    @classmethod
    def parse_line(cls, line):
        parts = line.split(" ")
        args = list(map(int, parts[1:]))
        instruction = cls.operations[parts[0]]
        return lambda registers: instruction(*args, registers)

    def compile(self, code):
        raw = list(code)
        self.instruction_register = int(raw.pop(0).split(" ")[1])
        self.code = [type(self).parse_line(line) for line in raw]

    def reset(self):
        self.registers = {k: 0 for k in self.registers.keys()}

    def exec(self, stop_val=None):
        # breakpoint()
        pointer = 0
        stop = len(self.code)
        instruction_register = self.instruction_register

        while 0 <= pointer < stop and pointer != stop_val:
            self.registers[self.instruction_register] = pointer
            self.registers = self.code[pointer](self.registers)
            pointer = self.registers[instruction_register] + 1
